# AILog - Prompt History

## Prompt 1: Initial Fullstack Setup

Create a fullstack application with the following setup:

Architecture:
- monorepo with /backend and /frontend folders

Backend:
- Python with FastAPI
- SQLite database using SQLAlchemy
- include models based on seed.json structure
- CRUD endpoints for one main entity (based on seed data)
- JWT authentication using OAuth2 password flow (FastAPI standard)
- create a default admin user:
  - username: admin
  - password: admin123

Database:
- initialize SQLite DB on startup
- load data from backend/seed.json automatically

Frontend:
- Vue 3 with Vite
- simple table view displaying all records from backend
- basic login form (JWT auth)
- no styling needed, focus on functionality

AILog:
- create a file AILog.md in root
- include:
  - section "Prompt History"
  - section "AI Generated Code Notes"
  - section "Audit" (empty placeholder)
- this is a static file, not part of app logic

General:
- keep it minimal and runnable
- include instructions to run both frontend and backend



## Prompt 2: Fixing Initial Fullstack Setup and Adding missing files

- Add a .gitignore file to this project
- Make @AILog.md cleaner - dont change the content of it but divide it into 2 files so first can hold full prompts history and second one will have only short notes and audit with links to the first prompts file.
- Investigate why backend is not launching and telling that "ValueError: password cannot be longer than 72 bytes, truncate manually if necessary (e.g. my_password[:72])"



## Prompt 3: Fix Frontend CORS Error

when loging, it throws "POST http://127.0.0.1:8000/token net::ERR_FAILED 200 (OK)
login	@	App.vue:20" but post methog of loging in backend seems good "http 200".



## Prompt 4: Full CRUD, Backend Restructuring, Smart Dashboard, and Status Enum

Requirements:
- Add full CRUD for hardware management: Add new items, delete old ones, and toggle the "Repair" status
- Make file structure in backend cleaner and separate login and devices logic (preparing for users managing and Docker)
- Smart Dashboard: A list of hardware showing Name, Brand, Purchase Date, and Status (Available, In Use, Repair -> via enum). Must support sorting and filtering.
- Update AILog.md and AILog prompts history
