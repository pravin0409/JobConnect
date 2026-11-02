import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
import os

doc = docx.Document()

# Set standard margins (1 inch all around)
for section in doc.sections:
    section.top_margin = Inches(1)
    section.bottom_margin = Inches(1)
    section.left_margin = Inches(1)
    section.right_margin = Inches(1)

def add_title(text, size=18, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=12):
    p = doc.add_paragraph()
    p.alignment = align
    p.paragraph_format.space_after = Pt(space_after)
    run = p.add_run(text)
    run.font.name = 'Times New Roman'
    run.font.size = Pt(size)
    run.font.bold = bold
    return p

def add_heading(text, level=1):
    h = doc.add_heading(text, level=level)
    h.paragraph_format.space_before = Pt(14)
    h.paragraph_format.space_after = Pt(6)
    for run in h.runs:
        run.font.name = 'Times New Roman'
        run.font.color.rgb = RGBColor(15, 23, 42)
    return h

def add_p(text, bold_prefix='', space_after=6):
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.line_spacing = 1.15
    if bold_prefix:
        r_b = p.add_run(bold_prefix)
        r_b.font.name = 'Times New Roman'
        r_b.font.size = Pt(12)
        r_b.font.bold = True
    r = p.add_run(text)
    r.font.name = 'Times New Roman'
    r.font.size = Pt(12)
    return p

# ─── COVER PAGE ───────────────────────────────────────────────────────────────
for _ in range(2): 
    doc.add_paragraph()

add_title('MIT ACADEMY OF ENGINEERING', size=16, bold=True, space_after=4)
add_title('ALANDI, PUNE', size=13, bold=True, space_after=24)
add_title('DEPARTMENT OF SOFTWARE ENGINEERING', size=13, bold=True, space_after=6)
add_title('WEB TECHNOLOGY LABORATORY (WT LAB)', size=14, bold=True, space_after=6)
add_title('CA ACTIVITY 2 – PROJECT-BASED ACTIVITY', size=15, bold=True, space_after=32)

add_title('Full-Stack Mini-Project:', size=12, bold=False, space_after=6)
add_title('JOBCONNECT', size=20, bold=True, space_after=4)
add_title('FULL-STACK JOB PORTAL & RECRUITMENT MANAGEMENT SYSTEM', size=12, bold=True, space_after=40)

# Student Meta Table
table = doc.add_table(rows=5, cols=2)
table.alignment = WD_TABLE_ALIGNMENT.CENTER
meta_data = [
    ('Student Name:', 'Pravin Machhindra Thombare'),
    ('PRN:', '202401100022'),
    ('Branch:', 'Software Engineering'),
    ('Division:', 'A'),
    ('Academic Year:', '2026 – 2027')
]
for idx, (label, val) in enumerate(meta_data):
    row = table.rows[idx]
    row.cells[0].paragraphs[0].add_run(label).font.bold = True
    row.cells[1].paragraphs[0].add_run(val)
    for cell in row.cells:
        cell.paragraphs[0].runs[0].font.name = 'Times New Roman'
        cell.paragraphs[0].runs[0].font.size = Pt(11)

for _ in range(3): 
    doc.add_paragraph()

add_p('Full-Stack (Node.js, Express.js REST API, JSON Database, Responsive Client)', bold_prefix='Project Architecture: ')
add_p('http://localhost:3000 (Local Full-Stack Server)', bold_prefix='Execution Environment: ')

doc.add_page_break()

# ─── BODY ─────────────────────────────────────────────────────────────────────

add_heading('1. AIM', level=1)
add_p('To design, develop and demonstrate an individual full-stack web application named JobConnect — Full-Stack Job Portal & Recruitment Management System based on a real-world recruitment problem, demonstrating front-end user interaction, asynchronous RESTful API design using Node.js and Express.js, persistent database operations, dual-layer client/server validation, and recruiter pipeline management.')

add_heading('2. PROBLEM STATEMENT', level=1)
add_p('Modern career platforms often present high friction for both applicants and hiring teams. Job seekers need a clean interface to search positions, view detailed role prerequisites, and submit validated applications with immediate feedback. Conversely, hiring managers need a structured dashboard to review submissions, inspect candidate resumes and statements, update applicant lifecycle statuses (Pending, Under Review, Shortlisted, Rejected), and publish new openings without backend complexity.')
add_p('JobConnect satisfies these real-world requirements as a complete full-stack web application. It connects candidate discovery with recruiter operations through a Node.js/Express REST API and a persistent JSON database.')

add_heading('3. OBJECTIVES', level=1)
objs = [
    'Develop an individual, responsive full-stack mini-project addressing employment workflows.',
    'Implement a robust Node.js and Express RESTful API with structured routing and middleware.',
    'Establish a persistent, schema-driven database layer using structured JSON storage (db.json).',
    'Implement dual-layer validation: client-side on-blur feedback and server-side HTTP 400 enforcement.',
    'Provide candidate search, keyword filtering, category selection, and employment type filtering.',
    'Build an interactive direct application workflow with candidate details, experience, and resume links.',
    'Implement an interactive Recruiter Dashboard with live platform metrics, status transitions, and modals.',
    'Provide one-click demo data population to facilitate individual project presentation and evaluation.'
]
for o in objs:
    p = doc.add_paragraph(style='List Bullet')
    r = p.add_run(o)
    r.font.name = 'Times New Roman'
    r.font.size = Pt(11.5)

add_heading('4. SYSTEM ARCHITECTURE & DATA FLOW', level=1)
add_p('The application adopts a decoupled full-stack architecture where the front-end client communicates with the Express backend strictly through asynchronous JSON HTTP requests (REST API).')
add_p('1. Client Layer: Single-page views built with HTML5, modern CSS custom properties, and vanilla JavaScript (ES6+). Uses asynchronous fetch() calls to query endpoints without full page reloads.')
add_p('2. Server Layer: Node.js runtime executing an Express.js application listening on port 3000. It handles JSON body parsing, CORS headers, route handling, and input validation.')
add_p('3. Database Layer: Persistent file-backed JSON storage (db.json) maintaining distinct collections for jobs and applications, with automated file creation and atomic serialization.')

add_heading('5. TECHNOLOGIES USED', level=1)
tech_table = doc.add_table(rows=1, cols=2)
tech_table.alignment = WD_TABLE_ALIGNMENT.CENTER
hdr = tech_table.rows[0].cells
hdr[0].paragraphs[0].add_run('Technology / Tool').font.bold = True
hdr[1].paragraphs[0].add_run('Role & Purpose in Project').font.bold = True
for c in hdr:
    c.paragraphs[0].runs[0].font.name = 'Times New Roman'

technologies = [
    ('Node.js (v22)', 'Asynchronous JavaScript runtime executing the backend server environment.'),
    ('Express.js (v5)', 'Back-end web framework managing REST routes, middleware, and request validation.'),
    ('JSON File Database (db.json)', 'Persistent file-backed database storing jobs and candidate application collections.'),
    ('HTML5 & Vanilla JavaScript', 'Semantic markup and client-side logic handling dynamic rendering, fetch, and DOM updates.'),
    ('CSS3 (Modern Design System)', 'Responsive design with CSS custom property tokens, card grid, and media queries.'),
    ('CORS & Body-Parser', 'Cross-origin resource sharing enablement and incoming JSON payload parsing.'),
    ('VS Code & Git', 'Development environment, code formatting, and source-code version control.')
]
for t, p in technologies:
    row = tech_table.add_row().cells
    r0 = row[0].paragraphs[0].add_run(t)
    r1 = row[1].paragraphs[0].add_run(p)
    r0.font.name = 'Times New Roman'
    r1.font.name = 'Times New Roman'
    r0.font.size = Pt(10)
    r1.font.size = Pt(10)

add_heading('6. DATABASE SCHEMA & DATA MODELS', level=1)
add_p('JobConnect maintains two primary collections inside db.json:')
add_p('• jobs Collection: Contains job records with fields: id (String unique identifier), title (String), company (String), category (String e.g. Engineering, Design), location (String), type (String e.g. Full-time, Internship), salary (String), experience (String), skills (Array of Strings), description (String), requirements (String), and postedAt (ISO date string).')
add_p('• applications Collection: Contains submitted candidate profiles with fields: id (String unique identifier), jobId (String foreign key referencing target job), jobTitle (String), company (String), name (String candidate name), email (String), phone (String 10-digit Indian mobile), experience (String years), qualification (String degree), resumeUrl (String optional portfolio link), coverLetter (String), status (Enum: Pending, Under Review, Shortlisted, Rejected, Offered), and appliedAt (ISO date string).')

doc.add_page_break()

add_heading('7. REST API SPECIFICATION', level=1)
api_table = doc.add_table(rows=1, cols=4)
api_table.alignment = WD_TABLE_ALIGNMENT.CENTER
a_hdr = api_table.rows[0].cells
a_hdr[0].paragraphs[0].add_run('Endpoint').font.bold = True
a_hdr[1].paragraphs[0].add_run('Method').font.bold = True
a_hdr[2].paragraphs[0].add_run('Payload / Parameters').font.bold = True
a_hdr[3].paragraphs[0].add_run('Status & Functionality').font.bold = True
for c in a_hdr:
    c.paragraphs[0].runs[0].font.name = 'Times New Roman'

endpoints = [
    ('/api/stats', 'GET', 'None', '200 OK — Aggregate counts of jobs, applications, and status metrics.'),
    ('/api/jobs', 'GET', '?search=&type=&category=&location=', '200 OK — Filtered array of matching active job postings.'),
    ('/api/jobs/:id', 'GET', 'URL parameter id', '200 OK — Single job details; returns 404 if not found.'),
    ('/api/jobs', 'POST', '{ title, company, type, location, ... }', '201 Created — Validates and appends new job to database.'),
    ('/api/jobs/:id', 'DELETE', 'URL parameter id', '200 OK — Deletes job and cascading candidate applications.'),
    ('/api/apply', 'POST', '{ jobId, name, email, phone, ... }', '201 Created / 400 Bad Request — Submits candidate application with strict validation.'),
    ('/api/applications', 'GET', '?jobId=&status=&search=', '200 OK — Retrieves submitted candidate applications.'),
    ('/api/applications/:id/status', 'PATCH', '{ status: "Shortlisted" | "Rejected" }', '200 OK — Updates applicant lifecycle status in database.'),
    ('/api/applications/:id', 'DELETE', 'URL parameter id', '200 OK — Removes individual application record.')
]
for ep, m, param, st in endpoints:
    row = api_table.add_row().cells
    r0 = row[0].paragraphs[0].add_run(ep)
    r1 = row[1].paragraphs[0].add_run(m)
    r2 = row[2].paragraphs[0].add_run(param)
    r3 = row[3].paragraphs[0].add_run(st)
    r0.font.bold = True
    for c in row:
        c.paragraphs[0].runs[0].font.name = 'Times New Roman'
        c.paragraphs[0].runs[0].font.size = Pt(9.5)

add_heading('8. CLIENT-SIDE & SERVER-SIDE VALIDATION MATRIX', level=1)
val_table = doc.add_table(rows=1, cols=4)
val_table.alignment = WD_TABLE_ALIGNMENT.CENTER
v_hdr = val_table.rows[0].cells
v_hdr[0].paragraphs[0].add_run('Field').font.bold = True
v_hdr[1].paragraphs[0].add_run('Client-Side Validation').font.bold = True
v_hdr[2].paragraphs[0].add_run('Server-Side Enforcement').font.bold = True
v_hdr[3].paragraphs[0].add_run('Error Message Displayed').font.bold = True
for c in v_hdr:
    c.paragraphs[0].runs[0].font.name = 'Times New Roman'

val_rules = [
    ('Candidate Name', 'Length >= 3 characters on blur', 'name.trim().length >= 3 check', 'Full name must contain at least 3 characters.'),
    ('Email Address', 'Regex: /^[^\s@]+@[^\s@]+\.[^\s@]+$/', 'Server-side regex validation', 'Please provide a valid email address.'),
    ('Mobile Number', 'Regex: /^[6-9]\d{9}$/ (10-digit Indian)', 'Server-side phone regex check', 'Enter a valid 10-digit Indian mobile number.'),
    ('Qualification', 'Non-empty dropdown selection', 'qualification.trim().length >= 2', 'Please select or enter your qualification.'),
    ('Experience', 'Range check between 0 and 50 years', 'Finite number parsing check', 'Experience must be between 0 and 50 years.'),
    ('Resume URL', 'Optional; if provided must use http/https', 'new URL() protocol check', 'Resume URL must start with http:// or https://'),
    ('Job Title', 'Length >= 3 characters', 'title.trim().length >= 3 check', 'Title must be at least 3 characters long.'),
    ('Job Description', 'Length >= 15 characters', 'description.trim().length >= 15 check', 'Description must be at least 15 characters.')
]
for f, cv, sv, em in val_rules:
    row = val_table.add_row().cells
    row[0].paragraphs[0].add_run(f).font.bold = True
    row[1].paragraphs[0].add_run(cv)
    row[2].paragraphs[0].add_run(sv)
    row[3].paragraphs[0].add_run(em)
    for c in row:
        c.paragraphs[0].runs[0].font.name = 'Times New Roman'
        c.paragraphs[0].runs[0].font.size = Pt(9.5)

doc.add_page_break()

add_heading('9. SCREENSHOTS AND APPLICATION DEMONSTRATION', level=1)
img_folder = os.path.join(os.path.dirname(__file__), 'screenshots')
screenshots = [
    ('Figure_1_Homepage.png', 'Figure 1: JobConnect Homepage displaying live metrics, search bar, category chips, and job cards.'),
    ('Figure_2_Job_Details.png', 'Figure 2: Job Details page showing full role specifications, requirements, and compensation.'),
    ('Figure_3_Candidate_Validation.png', 'Figure 3: Interactive Candidate Application Form populated with demo student data and validation.'),
    ('Figure_4_Submission_Success.png', 'Figure 4: Confirmed application submission with success notification banner and toast message.'),
    ('Figure_5_Recruiter_Dashboard.png', 'Figure 5: Recruiter & Operations Dashboard showing candidate table, status dropdowns, and metrics.'),
    ('Figure_6_Post_Job.png', 'Figure 6: Recruiter Job Posting Portal with category selection, compensation, and required skills.')
]
for fname, caption in screenshots:
    fpath = os.path.join(img_folder, fname)
    if os.path.exists(fpath):
        doc.add_paragraph().paragraph_format.space_before = Pt(8)
        doc.add_picture(fpath, width=Inches(6.2))
        cp = doc.add_paragraph()
        cp.alignment = WD_ALIGN_PARAGRAPH.CENTER
        cp.paragraph_format.space_after = Pt(14)
        cpr = cp.add_run(caption)
        cpr.font.name = 'Times New Roman'
        cpr.font.size = Pt(10)
        cpr.font.italic = True

doc.add_page_break()

add_heading('10. TEACHER DEMONSTRATION & VIVA GUIDE', level=1)
add_p('During individual project demonstration to the subject teacher, the following key points can be presented:')
viva_qa = [
    ('Q1: What real-world problem does this project solve?',
     'A1: JobConnect provides an end-to-end digital employment platform connecting candidates with vetted tech positions, eliminating paper resumes through structured digital submissions and providing recruiters with live applicant tracking pipelines.'),
    ('Q2: Explain the client-server interaction in this project.',
     'A2: The front-end is decoupled from the server. When a user interacts with the UI (e.g. searching, applying, updating status), client JavaScript sends asynchronous fetch() HTTP requests with JSON payloads to the Express REST API. The server validates the request, updates db.json, and returns appropriate HTTP status codes.'),
    ('Q3: How is data stored and managed?',
     'A3: Data is stored in db.json as schema-compliant JSON documents for jobs and applications. Node.js fs module reads and atomically writes serialized records, ensuring data survives server restarts without external database engine dependencies.'),
    ('Q4: How does validation work across the application?',
     'A4: Validation is implemented at both ends. Client-side validation uses on-blur events and regex checks to provide immediate visual feedback (red borders, clear error text). Server-side validation inspects incoming payloads and rejects malformed requests with HTTP 400 Bad Request.'),
    ('Q5: What are the recruiter features?',
     'A5: Recruiters have access to the Dashboard (dashboard.html) displaying live statistics, an applicant table with inline status dropdowns (Pending, Under Review, Shortlisted, Rejected), candidate cover letter modal viewers, and a job creation hub (post-job.html).')
]
for q, a in viva_qa:
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(6)
    rq = p.add_run(q + '\n')
    rq.font.bold = True
    rq.font.size = Pt(11)
    rq.font.name = 'Times New Roman'
    ra = p.add_run(a)
    ra.font.size = Pt(11)
    ra.font.name = 'Times New Roman'

add_heading('11. CONCLUSION', level=1)
add_p('The JobConnect Full-Stack Mini-Project successfully fulfills all requirements of CA Activity 2 (Project-Based Activity). It demonstrates an individual, complete full-stack web application integrating modern front-end design, Node.js and Express RESTful API backend, schema-driven persistent JSON database, robust dual-layer validation, and an interactive recruiter workflow. The project is fully functional, thoroughly documented, and prepared for individual teacher demonstration and evaluation.')

out_path = 'd:/TY subjects/WT Lab/202401100022_PravinMachhindraThombare_JobConnect.docx'
doc.save(out_path)
print('Successfully saved report to', out_path)
