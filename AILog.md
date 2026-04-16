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



## Prompt 8: Transaction Safety & Race Condition Mitigation
### Tool:
VSC with GitHub Copilot

### AI Generated Code Notes:
**Critical Issues Found:**
1. **Device Status Updates** (`PATCH /devices/{id}/status/{status}`)
2. **Device Updates** (`PUT /devices/{id}`)
3. **User Creation** (`POST /users`)
4. **User Updates** (`PUT /users/{id}`)
5. **Device/User Deletions** (`DELETE` endpoints)
6. **Device Creation** (`POST /devices`)

### Solution Implementation:
**Pessimistic Locking Strategy:**
- Used SQLAlchemy's `.with_for_update()` to lock rows at database level
- Works on both SQLite and PostgreSQL:
  - **SQLite**: Uses SERIALIZABLE isolation level (transaction-level locking)
  - **PostgreSQL**: Uses `FOR UPDATE` clause (row-level locking)

**Session Management:**
- All mutation endpoints wrapped in try/except blocks
- `session.rollback()` called on any exception (except HTTPException which is re-raised)
- Ensures database state consistency even after failed operations
- `db.refresh(model)` after commit to guarantee fresh data

### Audit:
- App is working fine after all these crucial changes, but i cannot test it now alone on my pc. Next step will be to implement tests and simulations to test if everything is working correctly. This prompt was prepared with help of gemini to match the prompt engeneering techniques and worked perfect fixing only selected issues.



## Prompt 9: Comprehensive Test Suite Implementation
### Tool:
VSC with GitHub Copilot

### AI Generated Code Notes:
Created production-grade test suite covering critical business logic with 6+ tests per domain (backend + frontend).

**Backend Tests (pytest + FastAPI TestClient):**
- Setup: In-memory SQLite with database fixtures and JWT token generation
- 6 test classes with 25+ critical tests:
  1. **Device Rental Logic** - Success/fail cases, race conditions, role authorization
  2. **Authentication/Authorization** - 401/403 validation across all endpoints
  3. **User Management** - Creation, duplicate prevention (409), password updates
  4. **Transaction Safety** - Concurrent operations serialize correctly
  5. **Error Handling** - Invalid IDs/credentials return appropriate HTTP codes

**Frontend Tests (vitest + @vue/test-utils):**
- Mock API client completely (no network requests)
- 5 test suites with 15+ critical tests:
  1. **Device Rental UI** - Rent button visibility for Repair/In Use/Available status
  2. **Rent Action Triggers** - Correct API calls on action, error handling
  3. **Role-Based Visibility** - Admin controls only visible to admins
  4. **Session Persistence** - localStorage restoration and logout cleanup
  5. **Navigation Guards** - Non-admins blocked from admin views

**Backend:**
1. ✅ User successfully rents Available device (admin auth required)
2. ✅ User CANNOT rent Repair/In Use device
3. ✅ User CANNOT rent already rented device (race condition)
4. ✅ Unauthenticated user gets 401 on any endpoint
5. ✅ Regular user gets 403 on admin-only endpoints
6. ✅ Cannot create duplicate username (409 Conflict)

**Frontend:**
1. ✅ Rent button NOT shown for Repair status
2. ✅ Rent button NOT shown for In Use status
3. ✅ Rent button shown for Available status
4. ✅ Rent action triggers correct API call with device ID
5. ✅ Mark as Repaired button only visible to admins
6. ✅ Session persists across page reloads via localStorage

**Additional Logic That Should Be Tested (Future):**
1. **Return Device Flow** - Transition from "In Use" → "Available"
2. **Mark Device In Repair** - State transition validation
3. **Concurrent User Updates** - Two admins editing same user
4. **Admin Promotion** - Cannot promote/demote own account
5. **Device History Tracking** - Audit trail updates
6. **Bulk Operations** - Multiple devices updated atomically
7. **Permission Boundaries** - User cannot modify other users' rentals
8. **Device Assignment Lifecycle** - Assigned_to field validation
9. **Timestamp Validation** - Purchase date cannot be in future
10. **Search & Filter** - Device search with status filters

### Audit:
Created tests were not all fine at first and I needed to cooperate more with Agent to solve the occured issues and make the tests work. There were also added 3 new .md files that I didnt asked for, but I will leave them for now as a part of testing documentation. In future I will need to read them carefully to see if I really need this. Also important note is that there are only a few tests and this may need to be expansed to coverage a whole app.
After short iteration I decided to not improve the tests much and just make them work. I have used workaround in frontend tests by adding new special .js file that is running tests to dont have to fight with libs versions management at this moment.


## Prompt 10: Frontend-Only LLM Integration
### Tool:
VSC with GitHub Copilot

### AI Generated Code Notes:
- **Provider Abstraction Layer** (`llmProviders.js`): Unified `callLLM()` interface for OpenAI, Gemini, and Grok
- **Provider-specific adapters**: Each provider has native API format (OpenAI: messages array, Gemini: contents object, Grok: OpenAI-compatible)
- **Response Parsing**: `parseResponseForBackendCommand()` extracts filter/sort intents from AI responses
- **UI Component** (`AIChatPanel.vue`): Provider selector, API key input (memory-only), model dropdown, prompt textarea, response display
- **Security**: Keys never logged, never sent to backend, only in-memory storage, direct to provider APIs

### Audit:
Frontend-only LLM integration works perfectly, but not at expected scope. Still its nice upgrade that I will iterate to got the solution that is in my mind.



## Prompt 11: Smart Assistant Enhancement & Custom Model Support
### Tool:
VSC with GitHub Copilot

### AI Generated Code Notes:
- **Renamed AI Assistant to Smart Assistant** - Better reflects equipment management purpose
- **Removed search bar** from Header component - Replaced with dynamic page titles
- **Custom Model Support** - Added toggle between Preset (dropdown) and Custom (text input) modes
- **Expanded Model Lists**: 
  - OpenAI: gpt-4-turbo, gpt-4, gpt-4o, gpt-4o-mini, gpt-3.5-turbo
  - Gemini: gemini-pro, gemini-1.5-pro, gemini-1.5-flash, gemini-2.0-flash, **gemini-2.5-flash**, **gemini-2.5-pro**
  - Grok: grok-1, grok-vision-beta, **grok-2**
- **Future-proof**: Custom mode allows any model without code changes

### Audit:
Smart Assistant is now the primary device querying tool. Users can access latest models (Gemini 2.5, GPT-4o-mini, etc.) via custom mode. All tests passing, no regressions. Still not what I was thinking about.



## Prompt 12: Smart Assistant Enhancement & Custom Model Support
### Tool:
VSC with GitHub Copilot

### AI Generated Code Notes:
- Fixed Gemini API Safety Settings - Updated llmProviders.js to use valid Gemini safety categories (HARM_CATEGORY_HATE_SPEECH, SEXUALLY_EXPLICIT, DANGEROUS_CONTENT, HARASSMENT) instead of UNSPECIFIED. This resolves the error you were getting.
- Simplified to Gemini 2.5 Flash Only - Created new AIChatModal.vue component that hardcodes this single model. No provider selection, no model dropdown—just clean and focused.
- Persistent AI Panel Across App - Added a floating 🤖 button in bottom-right corner that persists across all views:
- Click to toggle the AI chat panel on/off
Panel stays accessible from Hardware List, My Rentals, Admin views
Doesn't interfere with existing navigation
Uses z-index layering to float above main content
Modal UI - Right-side compact panel (w-80 h-96) with:
- Minimal setup (just API key input)
Query textarea
Send button
Response display with filter application
Close button to collapse

### Audit:
UI and UX looks much better now but its not working correctly now. Sending prompts does nothing so i need to investigate it.



## Prompt 13: Smart Assistant Enhancement
### Tool:
VSC with GitHub Copilot

### AI Generated Code Notes:
1. Frontend UI Changes
Removed AI Assistant from left sidebar navigation (Sidebar.vue)
Removed dedicated AIAssistantView route from the main app (App.vue)
The AI assistant now appears only as a floating button in the bottom-right corner
2. Enhanced AI Command System
Updated the command parsing to support diverse actions:
Filter - By device status (Available, In Use, Repair, All)
Sort - By brand, date, or name
Search - Find devices by name/description
Navigate - Switch between views (rentals, device management)
Click - Execute button actions (extensible for rent/return)
3. Backend AI Router
Created ai.py with:
/api/ai/parse-command - Endpoint to parse natural language into structured commands
/api/ai/suggestions - Endpoint to provide usage suggestions
New schemas for AICommand and AIResponse in schemas.py
4. Updated Components
AIChatModal now:
Displays detected actions in a clear format
Shows what will happen before applying changes
Supports multiple simultaneous commands
App.vue now:
Handles applyAIActions events with diverse command types
Intelligently switches views when applying filters
Supports navigation and multi-action sequences
5. Improved Command Parsing

### Audit:
Finally AI agent inside the app is working fine. There apeard some weird functions that will require updating, but main rout is nice for this prototype. 