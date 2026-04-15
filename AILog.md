# AILog - Notes & Audit

For complete prompt history, see [AILog_Prompts.md] 

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
