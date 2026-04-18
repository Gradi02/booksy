# Booksy Hardware Manager

A fullstack inventory management system for tracking company hardware devices and rentals.

**Live Demo:** 
- Backend: https://hardware-api-woty.onrender.com
- Frontend: https://booksy-rosy-three.vercel.app

## Fully Implemented

### Core Features
- **Device Inventory Management**
  - View all devices with filters (status, sorting by date/name/brand)
  - Create, edit, delete devices (admin only)
  - Track device status: Available, In Use, Repair

- **Hardware Rental System**
  - Rent available devices → status changes to "In Use"
  - Return rented devices → status reverts to "Available"
  - View personal rentals in dedicated tab

- **User & Access Control**
  - JWT token-based authentication (30-min expiration)
  - Admin role management
  - Admin-only device creation/editing/deletion
  - Admin-only user management panel
  - Password validation: min 8 characters
  - Email format requirement: `username@booksy.com` (except admin)
  - Prevent users from deleting end editing their own accounts

- **Responsive UI**
  - Sidebar navigation with admin features
  - Dynamic page titles for each view
  - Status badges with color coding
  - Modals for creating/editing devices and users
  - Session persistence (localStorage)

- **Smart Assistant** (AI-Powered by gemini 2.5 Flash only)
  - Natural language device queries using Gemini,
  - User-provided API keys (never stored, in-memory only)
  - Automatic parsing of AI responses for filter/sort commands
  - One-click application of AI-detected filters to device list
  - Works directly with provider APIs (no backend proxy)
  - Primary tool for intelligent device discovery and management

- **Auto-Healing System**
  - Database tables auto-created on startup
  - Data auto-seeded from `seed.json` if empty
  - Admin user (`admin@booksy.com/admin`) ensured on every restart
  - Works on Render's free tier with cold starts

### Backend (FastAPI + SQLAlchemy)
- RESTful API with proper HTTP status codes
- JWT authentication with OAuth2 password flow
- PostgreSQL for production, SQLite for development
- Connection pooling configured for PostgreSQL
- CORS properly configured via environment variables
- Role-based access control on all admin endpoints

### Frontend (Vue 3 + Vite + Tailwind)
- Single Page Application (SPA) with client-side routing
- Form validation with helpful error messages
- Responsive design (Tailwind CSS)
- Environment-based API URL configuration

## Shortcuts & Hacks

### 1. **Default Admin Credentials Hardcoded**
- Admin user created automatically on every startup
- **Why?** Everyone can login to admin account if the default password is not changed, but in this case I decided to leave it as it is, because this app is not going to work live, its only one time demo.
- **Future improvement:** Make it one-time only or use a setup wizard

### 2. **No Refresh Token Implementation**
- JWT tokens expire after 30 minutes → full re-login required
- **Future improvement:** Implement refresh token rotation
- **Workaround:** Session persisted in localStorage, but tokens don't auto-renew

### 3. **Limited Email Validation**
- Only checks `@booksy.com` suffix, no domain existence verification
- **Why?** This app is not going to be used in real company, so users can be 'fake' 
- **Future improvement:** Add email verification on sign-up

### 4. **No Rate Limiting**
- Login endpoint vulnerable to brute force attacks
- **Why?** There are no sensitive data inside the app so even if someone will hack it, cant steel anything.
- **Future improvement:** Add rate limiting middleware

### 5. **Device History Not Used**
- `history` field in Device model exists but never updated
- **Why?** Its nice feature, but not required in MVP workflow
- **Future improvement:** Track device status changes with timestamps

### 6. **Postgress database for deployment**
- second database provider for deployment purposes
- **Why?** Because of deployment sites requirement - free sites have many limitations like not persistance disks
- **Future improvement:** Using one database provider for both deployment and local app running and switching cloud service for better and more complex one.

### 7. **Manual Frontend Test Runner**
- `run-tests-manual.js` validates UI logic without vitest
- **Why?** Vitest requires Node.js v16+, but older environments may have v14. Manual runner works anywhere.
- **Workaround:** Run `node frontend/run-tests-manual.js` to validate 10 critical UI tests
- **Future improvement:** Upgrade Node.js to v18+ LTS and use full vitest suite (see TESTING.md)
Smart Assistant Usage

### 8. **AI api key required from user**
- user need to use his own api key in case of using AI tools in app
- **Why?** Global api key will require to be safely stored in backend but in this case where everyone can access app and no strict hacker blockers are featured, this is the safest and easiest way to implement this AI integration.
- **Future improvement:** In case of better cloud systems, there should be global api key builded inside the backend. With things like langfuse it will be able to track usage of it. This may also need a systems preventing from spamming to AI api.

## Best Next Steps - 24h Roadmap

1. **Add email verification** for new users (confirm @booksy.com domain)
2. **Device History Tracking** Record status changes with timestamps
3. **Update AI agent feature** to provide better user experience

## Local Development

### Backend
```bash
cd backend
python -m venv .venv
.venv\\Scripts\\activate
pip install -r requirements.txt
uvicorn main:app --reload
```
- API: http://127.0.0.1:8000
- Docs: http://127.0.0.1:8000/docs

### Frontend
```bash
cd frontend
npm install
npm run dev
```
- App: http://localhost:5173

## Default Credentials

- **Username:** `admin@booksy.com`
- **Password:** `admin`

## Tech Stack

- **Backend:** FastAPI, SQLAlchemy, SQLite (dev), PostgreSQL (prod), JWT auth
- **Frontend:** Vue 3, Vite, Tailwind CSS
- **Deployment:** Render (backend), Vercel (frontend)

## License

Internal use only