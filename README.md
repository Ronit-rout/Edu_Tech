# Raise Labs Learning Platform

Welcome to **Raise Labs Learning**, a professional, fully connected skill-verification and learning platform built using **Python + Django** on the backend and preserving premium **Warm Minimalist** design guidelines on the frontend.

---

## 1. Features

### Core Student Features
- **Student Dashboard**: The central command center detailing active courses, program roadmaps, and progress stats.
- **Unified Course Marketplace**: Interactive catalog listing internships and professional training programs. Shows program specifications (duration, level, pricing).
- **Secure Checkouts**: Secure mock payment forms for enrollment.
- **Learning Hub / Project Workspace**: Interactive course player containing task briefs, requirements checklists, and submission forms.
- **Evaluation Center**: Transparent grading feedback detailing strengths, improvements, and rubric grades.
- **Skills Wallet**: Digital vault listing cryptographically verified credentials and documents.
- **Final Interview Scheduling**: Booking interface for technical evaluations.
- **Certificate Verification**: Claim certificates and schedule retries if evaluation rubrics fail.

### Operational Command Features (Gated)
- **Educator Studio**: Course curriculum configuration dashboard.
- **HR Talent Dashboard**: Talent search, candidate listings, and profile verifications.
- **Admin Command Overview**: Submission audit queues and system metrics dashboards.

---

## 2. Installation & Quickstart

### Prerequisites
- Python 3.10+
- Django 6.0+

### Setup Steps
1. **Navigate to the Project Directory**:
   ```bash
   cd c:\Users\ronit\Downloads\stitch_skillstitch_evidence_ecosystem
   ```
2. **Apply Database Migrations**:
   ```bash
   python manage.py makemigrations accounts courses learning
   python manage.py migrate
   ```
3. **Seed Database with Demo Data**:
   ```bash
   python seed.py
   ```
4. **Start the Development Server**:
   ```bash
   python manage.py runserver 8000
   ```

---

## 3. Demo Accounts Credentials

The seeding script generates these pre-configured user profiles with password **`raiselabs123`**:

| Role | Username | Email | Access |
| :--- | :--- | :--- | :--- |
| **Student** | `student` | `student@raiselabs.com` | Dashboard, Learning Hub, Checkout, Training |
| **Educator** | `educator` | `educator@raiselabs.com` | Program Builder, submission reviews |
| **HR / Employer** | `hr` | `hr@raiselabs.com` | Talent Registry, Candidate profiles |
| **Admin** | `admin` | `admin@raiselabs.com` | Full Operational Command, Queue metrics |
