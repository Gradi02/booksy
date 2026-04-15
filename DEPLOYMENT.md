# Deployment Guide for Booksy

## Overview
This guide covers deploying the Booksy fullstack application:
- **Backend**: FastAPI → Render (with auto-healing PostgreSQL)
- **Frontend**: Vue 3 + Vite → Vercel

## What's Been Prepared

### Backend Changes
1. **requirements.txt** - Added `psycopg2-binary` (PostgreSQL driver) and `python-dotenv`
2. **database.py** - Now loads environment variables and supports PostgreSQL with connection pooling
3. **main.py** - CORS origins are now configurable via `ALLOWED_ORIGINS` environment variable
4. **.env.example** - Template showing required configuration variables
5. **render.yaml** - Render deployment manifest with PostgreSQL database setup

### Frontend Changes
1. **App.vue** - Updated to use `import.meta.env.VITE_API_URL` for API endpoint
2. **.env.example** - Template showing required environment variables
3. **vercel.json** - SPA routing configuration for Vercel

### Auto-Healing System
The auto-healing is built into your existing startup logic:
```python
@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)  # Creates all tables if missing
    initialize_data(db)                     # Seeds data if empty
```

When Render wakes up the container:
1. ✅ Database connection is restored
2. ✅ Tables are recreated if needed
3. ✅ Data is seeded from `seed.json` if database is empty
4. ✅ Admin user (`admin/admin123`) is ensured

---

## Deployment Steps

### Step 1: Render Backend Deployment

#### Option A: Using render.yaml (Automatic)
```bash
# 1. Push your code to GitHub
git add .
git commit -m "Prepare for deployment"
git push

# 2. Go to https://render.com and sign up
# 3. Create new "Blueprint" (Infrastructure as Code)
# 4. Connect your GitHub repository
# 5. Select the render.yaml file
# 6. Deploy!
```

#### Option B: Manual Dashboard Setup
```bash
# 1. Create PostgreSQL database:
#    - Service: PostgreSQL Database
#    - Name: booksy-postgres
#    - Plan: Free tier
#    - Region: Oregon (or closest)
#    - Note: Copy the Internal Database URL (not External)

# 2. Create Web Service:
#    - Name: booksy-backend
#    - Runtime: Python
#    - Build Command: pip install -r requirements.txt
#    - Start Command: uvicorn main:app --host 0.0.0.0 --port $PORT
#    - Environment Variables:
#      • DATABASE_URL: (from PostgreSQL service connection string)
#      • ALLOWED_ORIGINS: https://your-frontend.vercel.app,https://your-backend.onrender.com

# 3. Deploy!
```

### Step 2: Vercel Frontend Deployment

```bash
# 1. Ensure .env.production exists in frontend/ directory
#    Add: VITE_API_URL=https://your-backend.onrender.com

# 2. Go to https://vercel.com and sign up

# 3. Import your GitHub repository

# 4. Framework Preset: Other (or Vite)
#    Build & Development Settings:
#    - Framework: Vite
#    - Build Command: npm run build
#    - Output Directory: dist
#    - Root Directory: frontend (if monorepo)

# 5. Environment Variables: Add from .env.example
#    VITE_API_URL=https://your-backend.onrender.com

# 6. Deploy!
```

### Step 3: Connect Frontend to Backend

After both are deployed:

1. **Get Render backend URL** (e.g., `https://booksy-backend.onrender.com`)
2. **Update Vercel environment variable**: 
   - Go to Vercel Project Settings → Environment Variables
   - Set `VITE_API_URL` to your Render backend URL
   - Redeploy
3. **Update Render CORS**:
   - Go to Render Service Settings → Environment
   - Set `ALLOWED_ORIGINS` to your Vercel frontend URL
   - Service will auto-restart

---

## Environment Variables Reference

### Backend (.env or Render dashboard)
```env
# PostgreSQL connection string (Render provides this automatically)
DATABASE_URL=postgresql://user:password@host:port/dbname

# Comma-separated list of allowed origins
ALLOWED_ORIGINS=https://your-frontend.vercel.app,https://booksy-backend.onrender.com
```

### Frontend (.env.local or Vercel dashboard)
```env
# Backend API URL
VITE_API_URL=https://your-backend.onrender.com
```

---

## Testing Deployment

### 1. Test Backend Health
```bash
curl https://your-backend.onrender.com/
# Should return: {"message": "Booksy Inventory API is running"}
```

### 2. Test Frontend Access
```bash
# Open frontend URL in browser
# Should see login form
# Try logging in with admin / admin123
```

### 3. Test Auto-Healing
```bash
# On Render dashboard:
# 1. Go to your backend service
# 2. Click "Settings" → "Restart"
# 3. Watch the logs - should see initialization messages
# 4. Once restarted, login should work seamlessly
```

---

## Troubleshooting

### Backend won't start
- Check `DATABASE_URL` is set correctly in Render environment
- Look at Render logs for error messages
- Verify `psycopg2-binary` is in requirements.txt

### Frontend can't connect to backend
- Check `VITE_API_URL` matches your backend URL
- Make sure backend `ALLOWED_ORIGINS` includes your frontend URL
- Check browser console for CORS errors
- Verify backend is running: `curl https://your-backend.onrender.com/`

### Seed data not loading
- Check backend logs for errors during startup
- Verify `seed.json` is in backend directory
- Ensure database tables are created (check PostgreSQL)
- Database is read-only? Check PostgreSQL credentials

### Database connection issues
- Verify `DATABASE_URL` format: `postgresql://user:password@host:port/dbname`
- Check PostgreSQL IP allowlist (Render allows all by default)
- Test connection from local machine first

---

## Cost Estimates

- **Render PostgreSQL**: Free tier available (limited storage)
- **Render Backend**: Free tier available (sleeps after 15 min inactivity, auto-wake)
- **Vercel Frontend**: Free tier available
- **Total**: $0-50/month for hobby/small projects

---

## Next Steps (Optional)

1. **Custom Domain**: Add your domain to both Render and Vercel
2. **SSL Certificate**: Both handle this automatically
3. **CI/CD**: Both supports auto-deployment on GitHub push
4. **Monitoring**: Set up alerts for Render backend to notify when it fails
5. **Database Backups**: Render provides daily backups on paid plans

---

## Support Links

- Render Docs: https://render.com/docs
- Vercel Docs: https://vercel.com/docs
- FastAPI Production: https://fastapi.tiangolo.com/deployment/
- Vue 3 Production: https://vuejs.org/guide/deployment.html
