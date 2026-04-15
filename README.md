# Booksy Hardware Manager

A fullstack inventory management system for tracking company hardware devices and rentals.

**Live Demo:** 
- Backend: https://booksy-backend.onrender.com
- Frontend: https://booksy-hardware-manager.vercel.app

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
  - Search bar (placeholder for future AI integration)
  - Header with device count
  - Status badges with color coding
  - Modals for creating/editing devices and users
  - Session persistence (localStorage)

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

## Best Next Steps - 24h Roadmap

1. **Change default admin password** immediately in production
2. **Add rate limiting** to `/token` endpoint (prevent brute force)
3. **Implement refresh tokens** (better UX for long sessions)
4. **Add email verification** for new users (confirm @booksy.com domain)
5. **Device History Tracking** Record status changes with timestamps
6. **Reporting & Analytics**
   - Most rented devices
   - Device availability report
   - User activity dashboard
   - Device depreciation tracking
7. **Integrate Langfuse** for AI usage tracking and analytics
8. **Enhanced UI/UX**
   - Device images/thumbnails
   - Dark mode
   - Advanced dashboard with charts
   - Calendar view for rental timeline

---

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

---

## Deployment

See [DEPLOYMENT.md](DEPLOYMENT.md) for production deployment procedures (Render backend + Vercel frontend).

---

## Default Credentials

- **Username:** `admin@booksy.com`
- **Password:** `admin`

⚠️ **Change immediately after first login in production**

---

## Project Structure

```
booksy/
├── backend/
│   ├── main.py              # FastAPI app & routes
│   ├── auth.py              # JWT authentication
│   ├── database.py          # SQLAlchemy setup
│   ├── models.py            # Database models
│   ├── schemas.py           # Pydantic schemas
│   ├── seed_loader.py       # Database seeding
│   ├── seed.json            # Initial data
│   ├── requirements.txt     # Python dependencies
│   ├── render.yaml          # Render deployment config
│   └── routers/             # API endpoint routers
│
├── frontend/
│   ├── src/
│   │   ├── App.vue          # Main app component
│   │   ├── main.js          # Vue entry point
│   │   ├── components/      # Reusable components
│   │   └── views/           # Page components
│   ├── package.json         # Node dependencies
│   ├── vite.config.js       # Vite config
│   └── vercel.json          # Vercel SPA routing
│
├── DEPLOYMENT.md            # Production deployment guide
├── AILog.md                 # AI conversation notes
└── README.md                # This file
```

---

## Tech Stack

- **Backend:** FastAPI, SQLAlchemy, SQLite (dev), PostgreSQL (prod), JWT auth
- **Frontend:** Vue 3, Vite, Tailwind CSS
- **Deployment:** Render (backend), Vercel (frontend)

---

## License

Internal use only