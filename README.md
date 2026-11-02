# JobConnect — Full-Stack Job Portal & Recruitment Management System
### Web Technology Laboratory (WT Lab) — CA Activity 2: Project-Based Activity

> **Institution:** MIT Academy of Engineering, Alandi, Pune  
> **Department:** Department of Software Engineering  
> **Student Name:** Pravin Machhindra Thombare  
> **PRN:** 202401100022  
> **Branch & Division:** Software Engineering (Division A)  
> **Academic Year:** 2026–2027  

---

## 1. Executive Summary & Problem Statement
In the contemporary technology employment ecosystem, candidates struggle with opaque application processes while recruiters face unorganized applicant communications.

**JobConnect** solves this through a unified Full-Stack Web Application providing:
1. **Candidate Job Board:** Search, explore, and filter active job openings by keywords, job category (Engineering, Design, Internships), employment type (Full-time, Part-time, Contract), and location (Remote, Hybrid).
2. **Interactive Candidate Application System:** Directly apply for listings with verified personal, academic, and professional details, online portfolio/resume links, and custom cover letters, featuring **dual-layer client-side and server-side validation**.
3. **Recruiter & Operations Dashboard:** Real-time visibility into hiring pipelines with aggregate metrics (Total Openings, Total Applications, Shortlisted, Pending), dynamic candidate status lifecycle transitions (`Pending` ➔ `Under Review` ➔ `Shortlisted` ➔ `Rejected` ➔ `Offered`), candidate details modal inspection, and individual application/job deletion.
4. **Recruiter Job Publishing Hub:** Post structured job openings with skill tags, compensation, experience levels, and detailed responsibilities that appear immediately on the portal feed.

---

## 2. Technology Stack & Architecture

| Layer | Technologies Used | Role & Functionality |
| :--- | :--- | :--- |
| **Front-End Client** | HTML5, CSS3, JavaScript (ES6+), Inter Google Font | Semantic DOM layout, responsive CSS custom property tokens, asynchronous `fetch()` API calls, and real-time input event listeners. |
| **Back-End Server** | Node.js, Express.js (v5), CORS, JSON Parser | High-performance asynchronous REST API routing, request validation middleware, HTTP status codes (`200`, `201`, `400`, `404`, `500`), and static file serving. |
| **Persistent Storage** | File-backed JSON Database (`db.json`) | Persistent schema-based collections for `jobs` and `applications`; new local databases are initialized from `db.example.json`. |
| **Development & Testing** | Git, GitHub, REST client, VS Code | Modular codebase version control, automated browser UI testing, and live API verification. |

### Architectural Flow Diagram
```
[ Web Browser Client ]
   ├── index.html       (Search & Browse Job Board)
   ├── job-detail.html  (Job Specs & Client-Validated Application Form)
   ├── post-job.html    (Recruiter Job Publishing Form)
   └── dashboard.html   (Recruiter Pipeline & Application Lifecycle)
            │
            ▼ Asynchronous JSON HTTP Requests (fetch)
[ Express.js REST API Server (Port 3000) ]
   ├── Validation Middleware (Email regex, Phone regex, Schema bounds)
   ├── Route Handlers (/api/jobs, /api/apply, /api/stats, /api/applications)
   └── Response Serialization & Error Handling
            │
            ▼ File System I/O
[ Persistent JSON Storage (db.json) ]
   ├── jobs[] (Job listings, requirements, tags, compensation)
   └── applications[] (Candidate profiles, contact, cover letters, pipeline status)
```

---

## 3. REST API Specification

| Endpoint | Method | Request Payload | Response / Status | Purpose |
| :--- | :---: | :--- | :--- | :--- |
| `/api/stats` | `GET` | *None* | `200 OK` (JSON Metrics) | Returns count of active jobs, total applications, and status counts. |
| `/api/jobs` | `GET` | Query: `?search=&type=&category=&location=` | `200 OK` (Job Array) | Filtered and searched job listings. |
| `/api/jobs/:id` | `GET` | *None* | `200 OK` (Job Object) or `404 Not Found` | Details of a single job opening. |
| `/api/jobs` | `POST` | `{ title, company, category, type, location, salary, experience, skills, description, requirements }` | `201 Created` / `400 Bad Request` | Creates and validates a new job posting. |
| `/api/jobs/:id` | `DELETE` | *None* | `200 OK` / `404 Not Found` | Deletes a job listing and cascading applications. |
| `/api/apply` | `POST` | `{ jobId, name, email, phone, qualification, experience, resumeUrl, coverLetter }` | `201 Created` / `400 Bad Request` | Submits a candidate application with dual validation. |
| `/api/applications` | `GET` | Query: `?jobId=&status=&search=` | `200 OK` (Application Array) | Retrieves submitted candidate applications. |
| `/api/applications/:id/status` | `PATCH` | `{ status: "Under Review" \| "Shortlisted" \| "Rejected" \| "Offered" }` | `200 OK` / `400 Bad Request` | Updates candidate hiring pipeline stage. |
| `/api/applications/:id` | `DELETE` | *None* | `200 OK` / `404 Not Found` | Removes an individual application record. |

---

## 4. Dual-Layer Validation Matrix

| Field | Client-Side Check | Server-Side Validation | Invalid Test Example | Error Message |
| :--- | :--- | :--- | :--- | :--- |
| **Full Name** | On-blur length $\ge 3$ | `name.trim().length >= 3` | `"Al"` or `""` | *"Full name must contain at least 3 characters."* |
| **Email Address** | Standard email regex pattern | `/^[^\s@]+@[^\s@]+\.[^\s@]+$/` | `"candidate@domain"` | *"Please enter a valid email address."* |
| **Mobile Number** | 10-digit Indian mobile regex | `/^[6-9]\d{9}$/` | `"12345"` or `"4987654321"` | *"Enter a valid 10-digit Indian mobile number (starting 6-9)."* |
| **Qualification** | Dropdown non-empty selection | `qualification.trim().length >= 2` | Unselected (`""`) | *"Please select or enter your qualification."* |
| **Experience** | Range: $0 \le \text{exp} \le 50$ | Finite number check | `"-2"` or `"60"` | *"Experience must be a number between 0 and 50 years."* |
| **Resume URL** | Optional; valid HTTP/HTTPS protocol | `new URL(url).protocol` check | `"ftp://site.com"` | *"Resume URL must start with http:// or https://"* |
| **Job Title** | Title length $\ge 3$ chars | `title.trim().length >= 3` | `"JD"` | *"Title must be at least 3 characters long."* |

---

## 5. Local Setup & Execution Guide

### Prerequisites
- **Node.js** (v18.x or v20.x or higher)
- **npm** (v9.x or higher)

### Installation & Run Steps
```bash
# 1. Navigate to the job-portal directory
cd "d:/TY subjects/WT Lab/job-portal"

# 2. Install dependencies (express, cors)
npm install

# 3. Start the Full-Stack Server
node server.js
# Or using npm
npm start
```
The server creates a local `db.json` from the sanitized `db.example.json` seed on first run. The local database is ignored by Git so application data is not published.
The server will boot and display:
```
=======================================================
  JobConnect Full-Stack Server Running!
  Local URL: http://localhost:3000
=======================================================
```
Open **`http://localhost:3000`** in any web browser to access the live application.

---

## 6. Individual Presentation & Viva Demonstration Guide

When demonstrating **JobConnect** to the subject teacher, follow this structured walkthrough:

1. **Problem Statement & Introduction:**
   - *"Good morning/afternoon, Sir/Madam. My project is JobConnect, a Full-Stack Job Portal and Career Management System addressing transparent recruitment and candidate screening."*
2. **Architecture & Technologies:**
   - Front-End: Modern vanilla JS with asynchronous `fetch` and custom responsive CSS.
   - Back-End: Node.js with Express.js REST API implementing robust route handling, CORS, and request validation.
   - Database: Persistent schema-based JSON database (`db.json`) enabling atomic read/write persistence across restarts.
3. **Candidate Workflow Demonstration:**
   - Open `http://localhost:3000`. Show live search by entering keywords (e.g. `React`, `Node.js`).
   - Click a job card to open `job-detail.html`.
   - Point out the client-side validation by submitting empty fields to show the red error outlines.
   - Click the **"✨ Fill Demo Candidate"** button to auto-populate valid sample student data (Pravin Machhindra Thombare).
   - Click **"Submit Application Now"** to demonstrate instant API submission and celebration toast.
4. **Recruiter Dashboard Demonstration:**
   - Click **"Recruiter Dashboard"** (`dashboard.html`).
   - Point out the live aggregate metric cards (Total Jobs, Applications Received, Shortlisted).
   - Locate the newly submitted application in the Candidate Applications table.
   - Click the status dropdown and switch it from `Pending` to `Shortlisted`. Show how the status is updated on the server in real-time via `PATCH /api/applications/:id/status`.
   - Click the modal eye icon (`👁️`) to view the candidate's cover letter statement and resume link.
5. **Posting a New Opening:**
   - Click **"+ Post a Job"** (`post-job.html`).
   - Click **"✨ Fill Demo Job"** and hit **"Publish Job Opening"**.
   - Return to the homepage to show that the new opening immediately appears in the active job feed.
