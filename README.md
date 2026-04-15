# booksy

Minimal fullstack monorepo:
- `backend` - FastAPI + SQLAlchemy + SQLite + JWT auth
- `frontend` - Vue 3 + Vite

## Backend setup

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload
```

Backend URL: `http://127.0.0.1:8000`

Default user:
- username: `admin`
- password: `admin123`

Notes:
- SQLite DB file (`app.db`) is created on startup.
- Data from `backend/seed.json` is loaded automatically once when `devices` table is empty.

## Frontend setup

```bash
cd frontend
npm install
npm run dev
```

Frontend URL: `http://localhost:5173`

## API overview

- `POST /token` - OAuth2 password login, returns JWT
- `GET /devices` - list devices (requires Bearer token)
- `GET /devices/{id}` - get one device (requires Bearer token)
- `POST /devices` - create device (requires Bearer token)
- `PUT /devices/{id}` - update device (requires Bearer token)
- `DELETE /devices/{id}` - delete device (requires Bearer token)