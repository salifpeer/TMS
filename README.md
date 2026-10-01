# Talent Management System (TMS)

A full-stack employee management application built with Python, FastAPI, and Streamlit. The system supports employee registration, login, attendance tracking, leave applications, and personal details management, with a simple JSON-based persistence layer for storing employee and attendance records.

---

## Overview

The TMS project is designed to help an organization manage employee information and daily work operations in a lightweight, easy-to-run system. It combines:

- A FastAPI backend for API-driven operations
- A Streamlit frontend for employee interaction
- JSON-based data storage in the Database folder
- JWT-based authentication for login
- Optional location verification during attendance check-in

This project is ideal for small teams or learning environments that want a practical, end-to-end employee management system without a heavy database setup.

---

## Key Features

### 1. Employee Registration

- New employees can register with personal and contact details
- Email uniqueness is checked before registration
- Registered employees are stored in the JSON database

### 2. Employee Login

- Secure sign-in using email and password
- JSON user records are validated at login
- JWT token is generated for authenticated sessions

### 3. Attendance Management

- Employee check-in and check-out
- Break start and resume tracking
- Working hours and break summaries
- Attendance records kept in the attendance JSON file

### 4. Leave Management

- Employees can apply for single-day or multiple-day leave
- Leave requests include start date, end date, and reason
- Leave history is stored and accessible per employee

### 5. Employee Details View

- Employees can view their stored personal data through the dashboard
- Details are retrieved from the employee registration records

### 6. Location-Based Check-In

- The attendance flow includes a location verification step
- This is used to support office or workplace attendance checks

### 7. Dashboard Interface

- Streamlit dashboard provides a user-friendly UI
- Includes relevant tabs for dashboard, details, and leave management

---

## Tech Stack

- Python 3
- FastAPI
- Streamlit
- Pydantic
- Requests
- Python-JOSE (JWT)
- JSON file storage

---

## Project Structure

```text
TMS/
├── backend/
│   ├── auth/
│   │   └── auth.py
│   ├── Database/
│   │   ├── attendance.json
│   │   ├── details.json
│   │   ├── leaves.json
│   │   └── register.json
│   ├── repository/
│   │   ├── attendance.py
│   │   ├── breaks_cal.py
│   │   ├── details.py
│   │   ├── leaves.py
│   │   ├── login.py
│   │   └── Register.py
│   ├── routes/
│   │   ├── attendance.py
│   │   ├── details.py
│   │   ├── leaves.py
│   │   ├── login.py
│   │   └── Register.py
│   ├── services/
│   │   ├── attendance.py
│   │   ├── details.py
│   │   ├── leaves.py
│   │   ├── login.py
│   │   ├── Register.py
│   │   ├── Location_based_check_in.py
│   │   └── __init__.py
│   └── main.py
├── frontend/
│   ├── app.py
│   ├── Dashboard.py
│   ├── Dashboard_aqsa.py
│   ├── location.py
│   ├── login.py
│   └── Register.py
├── requirements.txt
├── pvenv/
├── .gitignore
└── README.md
```

---

## Backend Architecture

The backend is built using FastAPI and exposes API routes for:

- `/login`
- `/register/employee`
- `/details`
- `/leave`
- `/leaves`
- `/checkin`
- `/checkout`
- `/break/start`
- `/break/resume`
- `/tabledata`

These routes are registered in `backend/main.py` and connect to their corresponding service and repository layers.

### Backend Layers

- `routes/` — API endpoints
- `services/` — business logic
- `repository/` — JSON file read/write operations
- `Database/` — local persistent storage
- `auth/` — token generation logic

---

## Frontend Architecture

The frontend is built with Streamlit and is used to:

- Display the login/register screen
- Navigate between pages
- Show employee dashboard
- Manage attendance actions
- Apply for leave
- View personal details

The main entry file is:

- `frontend/app.py`

This file manages the current page state using `st.session_state` and routes users to login, register, dashboard, or location pages.

---

## Data Storage

The system uses JSON files as the storage mechanism. The core files are located in:

- `backend/Database/register.json`
- `backend/Database/attendance.json`
- `backend/Database/leaves.json`
- `backend/Database/details.json`

This design keeps the project lightweight and easy to run in local development without external database setup.

---

## Getting Started

### Prerequisites

Make sure the following are installed on your machine:

- Python 3.10 or newer
- pip
- A terminal or command prompt
- Access to a browser for the Streamlit UI

---

## Installation

From the project root (`TMS/`):

```bash
python -m venv pvenv
```

On Windows:

```bash
pvenv\Scripts\activate
```

Then install dependencies:

```bash
pip install -r requirements.txt
```

If you are using a different Python environment, make sure the required libraries are installed in that environment before running the app.

---

## Running the Backend

Start the FastAPI backend from the project root or inside the backend folder:

```bash
cd backend
uvicorn main:app --reload
```

The API will typically run at:

```text
http://127.0.0.1:8000
```

You can access the Swagger docs at:

```text
http://127.0.0.1:8000/docs
```

---

## Running the Frontend

Open a second terminal and start the Streamlit frontend:

```bash
cd frontend
streamlit run app.py
```

The application will open in the browser and load the login page by default.

---

## User Flow

### Registration Flow

1. User clicks Register in the login page
2. User fills in personal details
3. Account is created and saved in the JSON database
4. User is redirected to the login screen

### Login Flow

1. User enters email and password
2. Backend validates the credentials
3. JWT token is generated
4. Dashboard loads for the authenticated employee

### Attendance Flow

1. User logs in
2. Dashboard checks location verification state
3. User performs check-in or check-out
4. Attendance timestamps and break data are saved

### Leave Flow

1. User opens the Leaves tab
2. Selects one-day or multiple-day leave
3. Enters leave dates and reason
4. Request is stored in the leave JSON file

### Flow chart

<img src="TMS Attendance System Flowchart.png">

## Conclusion

The Talent Management System is a practical employee management application that brings together registration, attendance tracking, leave handling, and employee details in a single local system. It is easy to run, easy to extend, and a good base for learning full-stack application development with Python.

If you want, the next step can be to add a proper project screenshot section, deployment instructions, or a sample employee data schema to this README.
