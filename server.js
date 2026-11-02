const express = require('express');
const cors = require('cors');
const fs = require('fs');
const path = require('path');

const app = express();
const PORT = process.env.PORT || 3000;
const DB_PATH = path.join(__dirname, 'db.json');
const DB_SEED_PATH = path.join(__dirname, 'db.example.json');

// Middleware
app.use(cors());
app.use(express.json());
app.use(express.urlencoded({ extended: true }));
app.use(express.static(path.join(__dirname, 'public')));

// Database helper functions with fallback
const readDB = () => {
  try {
    if (!fs.existsSync(DB_PATH)) {
      const initial = JSON.parse(fs.readFileSync(DB_SEED_PATH, 'utf-8'));
      fs.writeFileSync(DB_PATH, JSON.stringify(initial, null, 2));
      return initial;
    }
    const raw = fs.readFileSync(DB_PATH, 'utf-8');
    return JSON.parse(raw);
  } catch (err) {
    console.error('Error reading database:', err);
    return { jobs: [], applications: [] };
  }
};

const writeDB = (data) => {
  try {
    fs.writeFileSync(DB_PATH, JSON.stringify(data, null, 2), 'utf-8');
    return true;
  } catch (err) {
    console.error('Error writing to database:', err);
    return false;
  }
};

// ─── VALIDATION HELPERS ───────────────────────────────────────────────────────
const isValidEmail = (email) => {
  const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return re.test(String(email).toLowerCase());
};

const isValidIndianPhone = (phone) => {
  const re = /^[6-9]\d{9}$/;
  return re.test(String(phone).trim());
};

const isValidUrl = (urlStr) => {
  if (!urlStr || urlStr.trim() === '') return true; // Optional
  try {
    const parsed = new URL(urlStr);
    return parsed.protocol === 'http:' || parsed.protocol === 'https:';
  } catch {
    return false;
  }
};

// ─── REST API ROUTES ─────────────────────────────────────────────────────────

// 1. GET /api/stats — Summary metrics for portal dashboard
app.get('/api/stats', (req, res) => {
  const db = readDB();
  const jobs = db.jobs || [];
  const applications = db.applications || [];

  const shortlistedCount = applications.filter(a => a.status === 'Shortlisted').length;
  const pendingCount = applications.filter(a => a.status === 'Pending').length;
  const underReviewCount = applications.filter(a => a.status === 'Under Review').length;

  const categories = {};
  jobs.forEach(j => {
    const cat = j.category || 'General';
    categories[cat] = (categories[cat] || 0) + 1;
  });

  res.json({
    totalJobs: jobs.length,
    totalApplications: applications.length,
    shortlistedCount,
    pendingCount,
    underReviewCount,
    categories
  });
});

// 2. GET /api/jobs — List jobs with search, category, type, and location filters
app.get('/api/jobs', (req, res) => {
  const { search, type, category, location } = req.query;
  const db = readDB();
  let jobs = db.jobs || [];

  if (search && search.trim() !== '') {
    const q = search.trim().toLowerCase();
    jobs = jobs.filter(j =>
      (j.title && j.title.toLowerCase().includes(q)) ||
      (j.company && j.company.toLowerCase().includes(q)) ||
      (j.location && j.location.toLowerCase().includes(q)) ||
      (j.skills && Array.isArray(j.skills) && j.skills.some(s => s.toLowerCase().includes(q)))
    );
  }

  if (type && type.trim() !== '') {
    jobs = jobs.filter(j => j.type && j.type.toLowerCase() === type.trim().toLowerCase());
  }

  if (category && category.trim() !== '') {
    jobs = jobs.filter(j => j.category && j.category.toLowerCase() === category.trim().toLowerCase());
  }

  if (location && location.trim() !== '') {
    jobs = jobs.filter(j => j.location && j.location.toLowerCase().includes(location.trim().toLowerCase()));
  }

  res.json(jobs);
});

// 3. GET /api/jobs/:id — Single job details
app.get('/api/jobs/:id', (req, res) => {
  const db = readDB();
  const job = (db.jobs || []).find(j => String(j.id) === String(req.params.id));
  if (!job) {
    return res.status(404).json({ success: false, error: 'Job posting not found' });
  }
  res.json({ success: true, job });
});

// 4. POST /api/jobs — Create a new job posting with server-side validation
app.post('/api/jobs', (req, res) => {
  const { title, company, category, location, type, salary, experience, skills, description, requirements } = req.body;
  const errors = {};

  if (!title || title.trim().length < 3) errors.title = 'Title must be at least 3 characters long.';
  if (!company || company.trim().length < 2) errors.company = 'Company name is required.';
  if (!location || location.trim().length < 2) errors.location = 'Job location is required.';
  if (!type || type.trim() === '') errors.type = 'Please select a valid job type.';
  if (!description || description.trim().length < 15) errors.description = 'Description must be at least 15 characters.';
  if (!requirements || requirements.trim().length < 10) errors.requirements = 'Requirements must be at least 10 characters.';

  if (Object.keys(errors).length > 0) {
    return res.status(400).json({ success: false, errors });
  }

  const db = readDB();
  const newJob = {
    id: 'job_' + Date.now(),
    title: title.trim(),
    company: company.trim(),
    category: category && category.trim() !== '' ? category.trim() : 'Engineering',
    location: location.trim(),
    type: type.trim(),
    salary: salary && salary.trim() !== '' ? salary.trim() : 'Competitive / Negotiable',
    experience: experience && experience.trim() !== '' ? experience.trim() : 'Not specified',
    skills: Array.isArray(skills) ? skills : (skills ? skills.split(',').map(s => s.trim()).filter(Boolean) : []),
    description: description.trim(),
    requirements: requirements.trim(),
    postedAt: new Date().toISOString().split('T')[0]
  };

  db.jobs = db.jobs || [];
  db.jobs.unshift(newJob);
  writeDB(db);

  res.status(201).json({ success: true, message: 'Job posted successfully!', job: newJob });
});

// 5. DELETE /api/jobs/:id — Delete a job and its applications
app.delete('/api/jobs/:id', (req, res) => {
  const db = readDB();
  const initialLength = (db.jobs || []).length;
  db.jobs = (db.jobs || []).filter(j => String(j.id) !== String(req.params.id));

  if (db.jobs.length === initialLength) {
    return res.status(404).json({ success: false, error: 'Job not found' });
  }

  // Also remove applications associated with this job
  db.applications = (db.applications || []).filter(a => String(a.jobId) !== String(req.params.id));
  writeDB(db);

  res.json({ success: true, message: 'Job and associated applications deleted successfully!' });
});

// 6. POST /api/apply — Submit candidate application with strict validation
app.post('/api/apply', (req, res) => {
  const { jobId, name, email, phone, experience, qualification, resumeUrl, coverLetter } = req.body;
  const errors = {};

  if (!jobId) errors.jobId = 'Target Job ID is required.';
  if (!name || name.trim().length < 3) errors.name = 'Full name must contain at least 3 characters.';
  if (!email || !isValidEmail(email)) errors.email = 'Please provide a valid email address.';
  if (!phone || !isValidIndianPhone(phone)) errors.phone = 'Enter a valid 10-digit Indian phone number (starting 6-9).';
  if (!qualification || qualification.trim().length < 2) errors.qualification = 'Please select or enter your qualification.';
  if (resumeUrl && !isValidUrl(resumeUrl)) errors.resumeUrl = 'Resume URL must start with http:// or https://';

  if (Object.keys(errors).length > 0) {
    return res.status(400).json({ success: false, errors });
  }

  const db = readDB();
  const targetJob = (db.jobs || []).find(j => String(j.id) === String(jobId));
  if (!targetJob) {
    return res.status(404).json({ success: false, error: 'Job listing does not exist' });
  }

  const newApplication = {
    id: 'app_' + Date.now(),
    jobId: String(jobId),
    jobTitle: targetJob.title,
    company: targetJob.company,
    name: name.trim(),
    email: email.trim().toLowerCase(),
    phone: phone.trim(),
    experience: experience ? String(experience).trim() : '0',
    qualification: qualification.trim(),
    resumeUrl: resumeUrl ? resumeUrl.trim() : '',
    coverLetter: coverLetter ? coverLetter.trim() : 'No cover letter provided.',
    status: 'Pending',
    appliedAt: new Date().toISOString().split('T')[0]
  };

  db.applications = db.applications || [];
  db.applications.unshift(newApplication);
  writeDB(db);

  res.status(201).json({
    success: true,
    message: 'Application submitted successfully! Recruiter has been notified.',
    application: newApplication
  });
});

// 7. GET /api/applications — List all candidate applications (optionally filter by jobId or status)
app.get('/api/applications', (req, res) => {
  const { jobId, status, search } = req.query;
  const db = readDB();
  let apps = db.applications || [];

  if (jobId) {
    apps = apps.filter(a => String(a.jobId) === String(jobId));
  }
  if (status && status !== 'All') {
    apps = apps.filter(a => a.status && a.status.toLowerCase() === status.toLowerCase());
  }
  if (search && search.trim() !== '') {
    const q = search.trim().toLowerCase();
    apps = apps.filter(a =>
      (a.name && a.name.toLowerCase().includes(q)) ||
      (a.email && a.email.toLowerCase().includes(q)) ||
      (a.jobTitle && a.jobTitle.toLowerCase().includes(q)) ||
      (a.company && a.company.toLowerCase().includes(q))
    );
  }

  res.json(apps);
});

// 8. PATCH /api/applications/:id/status — Recruiter updates candidate application status
app.patch('/api/applications/:id/status', (req, res) => {
  const { status } = req.body;
  const allowedStatuses = ['Pending', 'Under Review', 'Shortlisted', 'Rejected', 'Offered'];

  if (!status || !allowedStatuses.includes(status)) {
    return res.status(400).json({
      success: false,
      error: `Invalid status. Must be one of: ${allowedStatuses.join(', ')}`
    });
  }

  const db = readDB();
  const appIndex = (db.applications || []).findIndex(a => String(a.id) === String(req.params.id));
  if (appIndex === -1) {
    return res.status(404).json({ success: false, error: 'Application record not found' });
  }

  db.applications[appIndex].status = status;
  db.applications[appIndex].updatedAt = new Date().toISOString().split('T')[0];
  writeDB(db);

  res.json({
    success: true,
    message: `Application status updated to "${status}"`,
    application: db.applications[appIndex]
  });
});

// 9. DELETE /api/applications/:id — Delete an application
app.delete('/api/applications/:id', (req, res) => {
  const db = readDB();
  const initialLength = (db.applications || []).length;
  db.applications = (db.applications || []).filter(a => String(a.id) !== String(req.params.id));

  if (db.applications.length === initialLength) {
    return res.status(404).json({ success: false, error: 'Application not found' });
  }

  writeDB(db);
  res.json({ success: true, message: 'Application deleted successfully' });
});

// Start server
app.listen(PORT, () => {
  console.log(`=======================================================`);
  console.log(`  JobConnect Full-Stack Server Running!`);
  console.log(`  Local URL: http://localhost:${PORT}`);
  console.log(`=======================================================`);
});
