# 🚀 AI Chatbot Deployment Guide - Render

## 📋 **Project Names & URLs**

- **GitHub Repository**: `ai-chatbot`
- **Frontend App Name**: `ai-chatbot-app`
- **Backend API Name**: `ai-chatbot-api`
- **Frontend URL**: `https://ai-chatbot-app.onrender.com`
- **Backend URL**: `https://ai-chatbot-api.onrender.com`

This guide will help you deploy your document-based chatbot to Render with full functionality.

## 🎯 **Step-by-Step Deployment Process**

### **Step 1: Prepare GitHub Repository**

1. **Create a new repository on GitHub**:
   - Repository name: `ai-chatbot`
   - Description: "AI-powered document chatbot with file upload and Q&A functionality"
   - Make it Public or Private (your choice)

2. **Push your code to GitHub**:
   ```powershell
   # Navigate to your project root
   cd "E:\chatbot\chatbot-mvp\Chatbot - Copy"
   
   # Initialize git (if not already done)
   git init
   
   # Add all files
   git add .
   
   # Create initial commit
   git commit -m "Initial commit: AI chatbot with document upload and chat functionality"
   
   # Add your GitHub repository as remote
   git remote add origin https://github.com/YOUR_USERNAME/ai-chatbot.git
   
   # Push to GitHub
   git push -u origin main
   ```

---

### **Step 2: Deploy Backend API to Render**

1. **Go to Render Dashboard** (https://render.com)
2. **Click "New" → "Web Service"**
3. **Connect GitHub Repository**:
   - Select your `ai-chatbot` repository
   - Click "Connect"

4. **Configure Service Settings**:
   ```
   Name: ai-chatbot-api
   Environment: Python 3
   Region: Oregon (US West) or closest to you
   Branch: main
   Root Directory: backend
   Runtime: Use runtime.txt
   ```

5. **Build & Deploy Settings**:
   ```
   Build Command: pip install --upgrade pip && pip install -r requirements_simple.txt
   Start Command: uvicorn main:app --host 0.0.0.0 --port $PORT
   ```

6. **Environment Variables**:
   - Click "Advanced" → "Add Environment Variable"
   - Add: `GOOGLE_API_KEY` = `AIzaSyDxkp6DDyHfOb_pGyqLnoCgusRjUch2ZOA`

7. **❗ SKIP Persistent Storage** (Free Tier):
   - **Free tier doesn't support disks** - that's okay!
   - Your app uses **in-memory storage** instead
   - Documents will be temporary (lost on restart)
   - This is normal for free tier deployment

8. **Deploy**:
   - Click "Create Web Service"
   - Wait for deployment (5-10 minutes)
   - Your API will be available at: `https://ai-chatbot-api.onrender.com`

---

### **Step 3: Deploy Frontend App to Render**

1. **Create Static Site**:
   - In Render Dashboard, click "New" → "Static Site"
   - Select the same `ai-chatbot` repository

2. **Configure Site Settings**:
   ```
   Name: ai-chatbot-app
   Branch: main
   Root Directory: (leave empty)
   ```

3. **Build Settings**:
   ```
   Build Command: npm install && npm run build
   Publish Directory: dist
   ```

4. **Environment Variables**:
   - Add: `VITE_API_URL` = `https://ai-chatbot-api.onrender.com`

5. **Deploy**:
   - Click "Create Static Site"
   - Wait for deployment (3-5 minutes)
   - Your app will be available at: `https://ai-chatbot-app.onrender.com`

---

### **Step 4: Test Your Deployment**

1. **Test Backend**:
   - Visit: `https://ai-chatbot-api.onrender.com/test`
   - Should show: API status, Gemini configured: true

2. **Test Frontend**:
   - Visit: `https://ai-chatbot-app.onrender.com`
   - Login with any email/password
   - Go to Knowledge Base section
   - Upload a PDF file
   - Test chat functionality

---

## 🆓 **Free Tier Limitations & Solutions**

### **What Happens on Free Tier**:
- ✅ **App works perfectly** for testing and demo
- ⚠️ **Documents stored in memory only** (not persistent)
- ⚠️ **Service sleeps after 15 minutes** of inactivity  
- ⚠️ **Documents lost when service restarts** (cold start)

### **User Experience**:
- Upload documents → Works immediately
- Chat with documents → Works perfectly
- Service sleeps → Documents are lost
- User returns → Needs to re-upload documents
- **Perfect for demos and testing!**

### **If You Need Persistence**:
**Option A: Upgrade to Paid Plan** ($7/month)
- Add persistent disk storage
- Documents survive restarts
- No cold starts

**Option B: Use Supabase Free Tier** (Database storage)
- 500MB free database
- Documents stored in PostgreSQL
- Survives restarts even on free tier
- Setup instructions below ⬇️

---

## 🗄️ **Optional: Supabase Integration (Free Tier)**

### **Why Use Supabase?**
- **Free tier**: 500MB database (plenty for document text)
- **Persistent**: Documents survive service restarts
- **Still free**: Works with Render free tier

### **Quick Setup**:
1. **Create Supabase account**: https://supabase.com (free)
2. **Create new project**: Note your URL and API key
3. **Create table in SQL editor**:
   ```sql
   CREATE TABLE documents (
       id TEXT PRIMARY KEY,
       name TEXT NOT NULL,
       type TEXT NOT NULL,
       status TEXT NOT NULL,
       date_added TIMESTAMP DEFAULT NOW(),
       size_kb NUMERIC,
       content TEXT
   );
   ```
4. **Update backend environment variables**:
   - `SUPABASE_URL` = your_project_url
   - `SUPABASE_KEY` = your_anon_key
5. **Switch to Supabase version**: Replace main.py content with database version

---

## 📁 **What to Push to GitHub**

### **Include These Files**:
```
ai-chatbot/
├── backend/
│   ├── main.py                 ✅
│   ├── requirements_simple.txt ✅
│   ├── .env                   ❌ (Don't push - contains API key)
│   └── data/                  ❌ (Will be created on Render)
├── src/
│   ├── components/            ✅
│   ├── pages/                 ✅
│   ├── services/api.ts        ✅ (Updated with env variables)
│   └── ...                    ✅
├── public/                    ✅
├── package.json               ✅
├── vite.config.ts            ✅
├── .env                      ❌ (Don't push - contains API URLs)
├── .env.example              ✅ (Template for others)
└── README.md                 ✅
```

### **Create .gitignore file**:
```gitignore
# Environment variables
.env
backend/.env

# Dependencies
node_modules/
backend/__pycache__/

# Build outputs
dist/
build/

# Data files
backend/data/
backend/documents.json
backend/chroma_db/

# OS files
.DS_Store
Thumbs.db
```

---

## 🔧 **Important Configuration Updates**

### **Backend (main.py)**:
- ✅ CORS updated to allow `https://ai-chatbot-app.onrender.com`
- ✅ Data path configured for Render persistent storage
- ✅ Environment variable handling

### **Frontend (api.ts)**:
- ✅ API URL uses environment variable: `VITE_API_URL`
- ✅ Falls back to localhost for development

---

## � **Security Note**

**Never push these files to GitHub**:
- `.env` files (contain API keys)
- `backend/data/` folder (user uploaded files)
- `backend/__pycache__/` (Python cache)

---

## ⚡ **Quick Commands Summary**

### **Push to GitHub**:
```powershell
git add .
git commit -m "Ready for Render deployment"
git push origin main
```

### **Backend Deploy Settings**:
```
Name: ai-chatbot-api
Build: cd backend && pip install -r requirements_simple.txt
Start: cd backend && uvicorn main:app --host 0.0.0.0 --port $PORT
Env: GOOGLE_API_KEY=AIzaSyDxkp6DDyHfOb_pGyqLnoCgusRjUch2ZOA
Disk: chatbot-data → /opt/render/project/src/backend/data
```

### **Frontend Deploy Settings**:
```
Name: ai-chatbot-app
Build: npm install && npm run build
Publish: dist
Env: VITE_API_URL=https://ai-chatbot-api.onrender.com
```

---

## � **Final Result**

After deployment, you'll have:
- ✅ **Frontend**: `https://ai-chatbot-app.onrender.com`
- ✅ **Backend**: `https://ai-chatbot-api.onrender.com`
- ✅ **Full functionality**: Document upload, processing, and chat
- ✅ **Persistent storage**: Files survive service restarts
- ✅ **Professional URLs**: Easy to remember and share

Your AI chatbot will work exactly like it does locally, but accessible from anywhere in the world!