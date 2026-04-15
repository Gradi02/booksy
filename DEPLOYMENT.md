# Deployment Guide: Booksy Hardware Manager

Quick step-by-step instructions to deploy to Render (backend) and Vercel (frontend).

## Pre-Deployment Checklist

- [ ] Backend code changes committed to GitHub
- [ ] Frontend code changes committed to GitHub
- [ ] Generated strong SECRET_KEY for production
- [ ] Updated `.env` with new SECRET_KEY

---

## Step 1: Generate Production SECRET_KEY

Run this command locally to generate a strong key:

```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

Save this key - you'll need it when deploying to Render.

**Example output:** `cb82a8e986dd7def4b37a759c98e12fa33e2fc1e54b5ae0f44f4410470c0cb80`

---

## Step 2: Deploy Backend to Render

### Option A: Automatic Blueprint Deployment (Recommended)

1. Push your code to GitHub
2. Go to [render.com](https://render.com) and sign in
3. Click **"New +"** → **"Blueprint"**
4. Connect your GitHub repository
5. Render will auto-detect `render.yaml`
6. Confirm and deploy

### Option B: Manual Dashboard Setup

1. **Create PostgreSQL Database:**
   - Click **"New +"** → **"PostgreSQL Database"**
   - Name: `booksy-postgres`
   - Plan: Free tier
   - Region: Oregon (or closest to you)
   - Save the **Internal Database URL** (not External)

2. **Create Web Service:**
   - Click **"New +"** → **"Web Service"**
   - Connect your GitHub repository
   - Name: `booksy-backend`
   - Runtime: Python
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
   
3. **Set Environment Variables:**
   - `DATABASE_URL`: (paste the Internal Database URL from PostgreSQL)
   - `SECRET_KEY`: (use the generated key from Step 1)
   - `ALLOWED_ORIGINS`: `https://your-frontend.vercel.app,https://booksy-backend.onrender.com`

4. Click **"Create Web Service"** and wait for deployment (~2 min)

5. **Copy your backend URL** - you'll need it in Step 4

---

## Step 3: Deploy Frontend to Vercel

1. Go to [vercel.com](https://vercel.com) and sign in (use GitHub)
2. Click **"Add New..."** → **"Project"**
3. Select your GitHub repository
4. Configure:
   - **Framework Preset**: Vite
   - **Build Command**: `npm run build`
   - **Output Directory**: `dist`
   - **Root Directory**: `frontend`

5. **Set Environment Variable:**
   - `VITE_API_URL`: `https://your-backend.onrender.com` (replace with your actual Render backend URL from Step 2)

6. Click **"Deploy"** and wait (~1 min)

7. Copy your frontend URL after deployment

---

## Step 4: Update Backend CORS Origins (if needed)

If deployed successfully, go back to Render backend service:

1. Go to your backend service on Render
2. Click **"Environment"**
3. Update `ALLOWED_ORIGINS` to include your Vercel frontend URL:
   ```
   https://your-frontend.vercel.app,https://booksy-backend.onrender.com
   ```
4. Click **"Save" → "Manual Deploy"** to restart

---

## Step 5: Test the Deployment

1. Open your Vercel frontend URL in browser
2. Log in with:
   - **Username:** `admin`
   - **Password:** `admin123`
3. Try viewing devices, creating a new user, etc.
4. **IMPORTANT:** Change the admin password immediately after first login

---

## Troubleshooting

### Backend shows "Service is spinning up"
- Render's free tier takes ~30 sec to wake up
- Wait a moment and refresh the page
- Auto-healing will reload database and seed data on startup

### Login doesn't work
- Check `ALLOWED_ORIGINS` on Render includes your Vercel frontend URL
- Check frontend `.env.production` has correct `VITE_API_URL`
- Check browser console for CORS errors
- Verify `SECRET_KEY` is set in Render environment

### Database connection error
- Ensure `DATABASE_URL` uses **Internal** connection string (not External)
- PostgreSQL takes ~1 min to initialize on first Render deployment

### "Admin access required" when creating/editing devices
- Only admins can create/edit devices
- Use admin account or grant admin role to your user

---

## Auto-Healing System

If Render backend wakes from cold start:
1. Database connection restored
2. All tables recreated if missing
3. Data reseeded from `seed.json`
4. Admin user (`admin/admin123`) ensured to exist

No manual intervention needed - the app auto-recovers.

---

## Production Notes

- Default admin user: `admin` / `admin123` → **Change password immediately**
- All passwords must be at least 8 characters
- Regular users must use email format: `username@booksy.com`
- Devices can only be created/edited/deleted by admins
- Token expiration: 30 minutes
- Sessions persist in browser localStorage

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
