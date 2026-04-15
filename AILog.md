# AILog - Notes & Audit

## Tooling: 
Cursor, Github Copilot, Gemini/ChatGPT (online LLMs)
## Data Strategy:
Firstly I asked online LLM, about sugested tech-stack to analyze it and look for any issues. At the beginning I was sure that deployment will be the hardest part of it because of limitations of free hostings. Finally I decided to mostly follow base tech-stack with minor modifications to fit for selected free hostings requirements. Initial Data are going to be a safe spot, and app is going to import them at every backend startup. It is the effect of selected hosting, but also nice option for this type of live demo - after some testing app will reset to initial data set.
## Prompt Trial:
For complete major prompt history, see [AILog_Prompts.md]. Lower there, you can see the short descriptions of these prompts and my personal Audit - short grade of what I got with this prompt.
## The "Correction":
The hardest was frontend actually, because of many buttons and panels. There was many bugs that were blocked in backend but not in frontend causing for example red error throwin in frontend when trying to edit device.
Another example may be, that admins only endpoints like "adding new user" were not secured at the backend. Anyone will be able to use eg.: POSTMAN to get access to admin-only features. 
That was all mostly easy to fix bugs that were mostly fixed via AI just by showing my agent an example bad routes.

## Prompt 1: 
### Tool: 
Cursor with OpenAI

### AI Generated Code Notes:
- Backend uses FastAPI + SQLAlchemy with SQLite and auto-seeds from `backend/seed.json` at startup.
- OAuth2 password flow is implemented with `/token`; default credentials are `admin` / `admin123`.
- Frontend is a minimal Vue 3 + Vite app with a login form and authenticated table view of devices.

### Audit:
- Most of the files were created properly, but backend wont start because of some auth and default admin account issues. I also forgot about .gitignore file so I will ask for it in next prompt. File structure may be more complex and less chaotic especially in /backend. As an initial prompt for basic tech setup with selected tech stack it looks clean and good as a start point. 



## Prompt 2: 
### Tool: 
VSC with github copilot

### AI Generated Code Notes:
- Added comprehensive .gitignore file for Python/Node.js fullstack project
- Split AILog documentation into separate files for better organization:
  - [AILog_Prompts.md](AILog_Prompts.md) - Full prompt history
  - AILog.md - This file, short notes and audit
- **Backend password length validation error**: Fixed by downgrading bcrypt to version 3.2 (compatible with passlib). The error was caused by bcrypt 4.0+ breaking API changes where the `__about__` module was removed. Updated requirements.txt to pin `bcrypt>=3.2,<4.0`.

### Audit:
- Downgrading the package version fixed the starting issue and app is running properly. It seems to be a problem with default admin login that I will now investigate.



## Prompt 3:
### Tool:
VSC with github copilot

### AI Generated Code Notes:
- **Frontend CORS error fix**: The login POST request was failing with `net::ERR_FAILED 200 (OK)` - a CORS issue where the response succeeded but the browser couldn't process it.
- Root cause: CORS middleware only allowed `http://localhost:5173` but frontend was running on `http://127.0.0.1:5173`
- Solution: Updated CORS configuration to:
  - Explicitly list both `localhost` and `127.0.0.1` origins for ports 5173 and 3000
  - Use explicit HTTP methods instead of wildcards (`["GET", "POST", "PUT", "DELETE", "OPTIONS"]`)
  - Added `expose_headers=["*"]` for proper header exposure

### Audit:
- Login endpoint now accessible from frontend without CORS errors
- Backend properly configured to handle both localhost and 127.0.0.1 origins



## Prompt 4-5: Bug Fixes & Security Hardening
### Tool:
VSC with github copilot

### AI Generated Code Notes:
- Fixed 3 critical bugs in user deletion and device creation
- Implemented security features:
  - JWT SECRET_KEY now read from .env (configurable for production)
  - Added admin-only authorization to device endpoints (POST, PUT, PATCH, DELETE)
  - Password validation: minimum 8 characters
  - Email validation: users must use format `username@booksy.com` (except admin)
  - Connection pooling for PostgreSQL (pool_size=5, max_overflow=10, pool_pre_ping=True)
- Updated documentation with deployment guide and tech debt notes
- Frontend UI updated to show email format requirements and password constraints

### Audit:
- All validators tested and working correctly
- Admin endpoints properly protected
- Deployment documentation simplified and actionable
- Ready for production deployment on Render + Vercel



## Prompt 4:
### Tool:
VSC with github copilot

### AI Generated Code Notes:
- Using `pushd` to properly set working directory for uvicorn
- Database auto-recreates on startup with enum schema
- All endpoints require JWT authentication
- CORS properly configured for both development IPs

### Audit:
- Basics are working fine, now I need to adjust it to fit the requirments.



## Prompt 5:
### Tool:
VSC with github copilot and ChatGPT online as helper in prompt preparation

### AI Generated Code Notes:
- Built professional **Hardware Manager** dashboard using Vue 3 + Tailwind CSS
- Created reusable component architecture:
  - **Sidebar.vue** - Fixed navigation with active states
  - **Header.vue** - Search bar + device count with icons
  - **DeviceTable.vue** - Card-style table with status badges and actions
  - **StatusBadge.vue** - Color-coded status indicator
  - **LoginPage.vue** - Professional login screen with gradient
- Added Tailwind CSS config + custom component classes (.btn-primary, .badge, .card)
- Responsive design with hover states, smooth transitions, and disabled button handling

### Audit:
- production-ready UI were delivered but not all options are already implemented in backend - this will be next step. Also some minor fixes in frontend may be needed but its just some UI/UX polishing.



## Prompt 6:
### Tool:
VSC with github copilot - firstly asked about "how to implement this solution", then decided to "do it as you described before"

### AI Generated Code Notes:
- Analyzed deployment requirements for Vercel (frontend) + Render (backend) with auto-healing
- Identified SQLite persistence issue on Render's ephemeral filesystem
- Recommended PostgreSQL migration for production stability
- - **Backend Deps**: Added `psycopg2-binary` (PostgreSQL driver) and `python-dotenv` to requirements.txt
- **Database Layer**: Updated database.py to:
  - Load `.env` file via `python-dotenv`
  - Support both SQLite (local dev) and PostgreSQL (production) via `DATABASE_URL` env var
  - Added connection pooling for production (skipped for SQLite)
- **CORS Configuration**: Moved hardcoded CORS origins to environment variable `ALLOWED_ORIGINS` in main.py
- **Frontend**: Updated App.vue to use `import.meta.env.VITE_API_URL` instead of hardcoded localhost
- **Configuration Files Created**:
  - `backend/.env.example` - Template for backend configuration
  - `backend/.env` - Local development settings (SQLite + local CORS)
  - `backend/render.yaml` - Render deployment manifest with PostgreSQL setup
  - `frontend/.env.example` - Template for frontend environment
  - `frontend/.env.production` - Production API URL template
  - `frontend/vercel.json` - Vercel SPA routing configuration
  - `DEPLOYMENT.md` - Complete deployment guide with step-by-step instructions

### Audit:
- Filer were prepared for deploy for selected platform and project is still running properly on localhost. Time to add missing features.



## Prompt 7:
### Tool:
VSC with github copilot

### AI Generated Code Notes:
- **Backend Users CRUD Implementation**: Created complete user management endpoints at `/users`:
  - `GET /users` - List all users (admin only)
  - `GET /users/{id}` - Get specific user (admin only)
  - `POST /users` - Create new user (admin only, validates unique username)
  - `PUT /users/{id}` - Update user including password and admin role (admin only)
  - `DELETE /users/{id}` - Delete user with self-deletion protection (admin only)
  - All endpoints require admin authentication, return proper HTTP status codes, and handle errors gracefully
  
- **Updated Backend Structure**:
  - Created `routers/users.py` following consistent pattern with devices router
  - Added `UserCreate` and `UserUpdate` Pydantic schemas in `schemas.py`
  - Updated `routers/__init__.py` to export users_router
  - Integrated users_router into `main.py`
  - Password hashing automatically applied for new/updated users
  
- **Frontend Session Persistence**:
  - Added `onMounted` hook to restore token and user data from localStorage on page refresh
  - Implemented `saveSession()` and `clearSession()` functions to manage token persistence
  - Login now calls `saveSession()` to store token and currentUser data
  - Logout calls `clearSession()` to remove stored data
  - **Fixes page refresh issue** - user no longer redirected to login after refresh
  
- **Frontend User Management Implementation**:
  - Added `addUser()`, `updateUser()`, `deleteUser()` async functions in App.vue
  - User modal form with username (disabled on edit), password, and admin role checkbox
  - Connected all user CRUD operations to new backend endpoints
  - Admin Users View (`AdminUsersView.vue`) shows roles alongside user management options
  - All operations update UI immediately via `fetchUsers()` after API calls
  
- **Frontend UI Cleanup**:
  - Removed star emoticon (✨) from search bar in Header.vue
  - Removed refresh button (🔄) from Header.vue
  - Removed "X items" device count display from Header.vue
  - Simplified Header component to only show search input with left icon (🔍)
  - Updated App.vue Header call to only pass search prop (removed device-count and @refresh)

### Audit:
- All missing features were implemented and look fine and safe for now.