# 🚀 AI Chatbot Supabase Edition - Complete Deployment Guide

## 📋 **What We're Deploying**
- **Frontend**: ChatDemo.tsx (clean interface, no admin section)
- **Backend**: main_supabase.py (Supabase + Google Gemini AI)
- **Database**: Supabase (persistent document storage)

## ✅ **Confirmed: Your Chatbot USES Supabase Backend**
Your `main_supabase.py`:
- ✅ Stores documents in Supabase (`documents` table)
- ✅ Stores document chunks in Supabase (`document_chunks` table) 
- ✅ Searches Supabase when users ask questions
- ✅ Uses Google Gemini AI to generate responses from Supabase content
- ✅ Stores conversations in Supabase for analytics

---

## 🎯 **Project Names for Render**
- **Backend**: `AI-Chatbot-Backend`
- **Frontend**: `AI-Chatbot-Frontend`

---

## 📂 **Step 1: Prepare Production Files**

I've created production-ready files for you:

### 📁 **Files Created**:
1. `src/App.production.tsx` - Clean frontend (no admin routes)
2. `src/services/api.production.ts` - Production API client with env vars
3. `.env.production` - Frontend environment variables
4. `.env.example` - Environment template
5. `backend/requirements.txt` - Backend dependencies
6. `render.yaml` - Render deployment configuration

### 🔄 **Replace Current Files**:
```bash
# Replace App.tsx with production version
cp src/App.production.tsx src/App.tsx

# Replace api.ts with production version  
cp src/services/api.production.ts src/services/api.ts
```

---

## 📤 **Step 2: Push to GitHub**

### Using Your Existing 'ai-chatbot' Repo:

```bash
# Navigate to your project
cd "E:\chatbot\chatbot-mvp\Chatbot - Copy"

# Initialize git if not already done
git init

# Add your existing GitHub repo as remote
git remote add origin https://github.com/yashdew3/ai-chatbot.git

# Add all files
git add .

# Commit changes
git commit -m "Deploy Supabase edition - ChatDemo frontend only"

# Push to main branch
git push -u origin main
```

---

## 🚀 **Step 3: Deploy Backend on Render**

### 3.1 Create Backend Service:
1. Go to [Render Dashboard](https://dashboard.render.com)
2. Click **"New +"** → **"Web Service"**
3. Connect your GitHub account and select `ai-chatbot` repository

### 3.2 Backend Configuration:
```yaml
Name: AI-Chatbot-Backend
Environment: Python 3
Region: Oregon (or closest to you)
Branch: main

Build Command: pip install -r backend/requirements.txt
Start Command: cd backend && python main_supabase.py
```

### 3.3 Environment Variables:
Add these in Render dashboard:
```
GOOGLE_API_KEY = your_google_gemini_api_key
SUPABASE_ANON_KEY = your_supabase_anonymous_key  
PORT = 8000
```

### 3.4 Deploy Backend:
- Click **"Create Web Service"**
- Wait 5-10 minutes for deployment
- Copy the backend URL: `https://ai-chatbot-backend-xxxx.onrender.com`

---

## 🎨 **Step 4: Deploy Frontend on Render**

### 4.1 Create Frontend Service:
1. In Render Dashboard, click **"New +"** → **"Static Site"**
2. Select the same `ai-chatbot` repository

### 4.2 Frontend Configuration:
```yaml
Name: AI-Chatbot-Frontend
Branch: main

Build Command: npm install && npm run build
Publish Directory: ./dist
```

### 4.3 Environment Variables:
```
VITE_BACKEND_URL = https://ai-chatbot-backend-xxxx.onrender.com
```
*(Replace with your actual backend URL from step 3.4)*

### 4.4 Deploy Frontend:
- Click **"Create Static Site"**
- Wait 5-10 minutes for deployment
- Your frontend will be live at: `https://ai-chatbot-frontend-xxxx.onrender.com`

---

## 🧪 **Step 5: Test Your Deployment**

### Backend Test:
Visit: `https://your-backend-url.onrender.com/test`

**Expected Response:**
```json
{
  "status": "success",
  "supabase_configured": true,
  "gemini_configured": true,
  "documents_count": 0,
  "chunks_count": 0,
  "storage_mode": "supabase"
}
```

### Frontend Test:
1. **Visit your frontend URL**
2. **Try the "Try Demo Chat" button**
3. **Ask a question** (e.g., "What services do you offer?")
4. **Verify**: You get a response saying no documents are uploaded yet

---

## 📚 **Step 6: Upload Documents (Admin Setup)**

Since you're the admin and want to add documents to the knowledge base:

### Option A: Temporary Admin Access
1. **Restore admin temporarily** for document upload
2. **Upload documents** via admin interface
3. **Remove admin access** again

### Option B: Direct Supabase Upload
1. **Go to your Supabase dashboard**
2. **Use the SQL editor** to insert documents directly
3. **Or use the storage interface** to upload files

### Option C: API Upload (Recommended)
Create a simple upload script that calls your backend API directly.

---

## 🎉 **Step 7: Final Configuration**

### Update CORS for Production:
In your `main_supabase.py`, make sure CORS includes your frontend URL:
```python
FRONTEND_URLS = [
    "https://ai-chatbot-frontend-xxxx.onrender.com",  # Your actual frontend URL
    "https://*.onrender.com",
    "*"  # Remove this in production for security
]
```

### Test Complete Flow:
1. **Upload documents** (via admin or API)
2. **Test chat** - ask questions about uploaded documents
3. **Verify** AI responds with relevant content from Supabase

---

## 🔧 **Troubleshooting**

### Common Issues:

**❌ CORS Errors:**
- Add your frontend URL to backend CORS configuration

**❌ 500 Backend Errors:**
- Check environment variables are set correctly
- Verify Supabase and Google API keys are valid

**❌ Chat Not Working:**
- Confirm `VITE_BACKEND_URL` points to correct backend
- Check browser console for error messages

**❌ No AI Responses:**
- Ensure documents are uploaded to Supabase
- Check backend logs for API errors

---

## 🎯 **Success Checklist**

- [ ] Backend deployed and responding at `/test` endpoint
- [ ] Frontend deployed and loading ChatDemo page
- [ ] Chat widget appears and opens
- [ ] Backend connects to Supabase successfully
- [ ] Google Gemini API configured correctly
- [ ] Documents uploaded to knowledge base
- [ ] AI responds to questions with relevant content

---

## 📞 **Final Result**

You'll have:
- **Clean public chat interface** (ChatDemo.tsx only)
- **AI chatbot** powered by Supabase documents
- **Persistent storage** of all conversations and documents
- **Professional deployment** on Render's infrastructure
- **Scalable architecture** ready for production use

**Your users can simply visit the frontend URL and start chatting with your AI assistant!**

🚀 **Happy Deploying!**