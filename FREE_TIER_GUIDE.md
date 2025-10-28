# 🆓 FREE TIER DEPLOYMENT - QUICK GUIDE

## ✅ **Current Status**
Your code is **ready for free tier deployment**! The backend has been optimized to work without persistent disks.

## 🚀 **Deploy Now (5 Minutes)**

### **Step 1: Copy the free tier backend**
```powershell
# Copy the optimized version
copy "backend\main_freetier.py" "backend\main.py"

# Commit and push
git add .
git commit -m "Optimize for free tier deployment"
git push origin main
```

### **Step 2: Deploy Backend to Render**
1. **Render.com** → New → Web Service
2. **Connect**: Select your `ai-chatbot` repository
3. **Settings**:
   - Name: `ai-chatbot-api`
   - Build: `cd backend && pip install -r requirements_simple.txt`
   - Start: `cd backend && uvicorn main:app --host 0.0.0.0 --port $PORT`
   - Environment: `GOOGLE_API_KEY` = `AIzaSyDxkp6DDyHfOb_pGyqLnoCgusRjUch2ZOA`
   - **Skip disk setup** (not available on free tier)

### **Step 3: Deploy Frontend to Render**
1. **Render.com** → New → Static Site
2. **Connect**: Same `ai-chatbot` repository
3. **Settings**:
   - Name: `ai-chatbot-app`
   - Build: `npm install && npm run build`
   - Publish: `dist`
   - Environment: `VITE_API_URL` = `https://ai-chatbot-api.onrender.com`

## 🎯 **What to Expect**

### **✅ Will Work**:
- Document upload and processing
- AI chat responses from documents
- Full admin interface
- Professional URLs

### **⚠️ Free Tier Limitations**:
- **Service sleeps** after 15 minutes of inactivity
- **Documents lost** when service restarts (cold start)
- **Users re-upload** documents after cold starts
- **Perfect for demos** and testing!

## 🔄 **User Flow on Free Tier**:
1. User visits your app
2. Uploads PDF documents ✅
3. Chats with AI about documents ✅
4. Service sleeps after 15 minutes 😴
5. User returns → Documents gone ❌
6. User re-uploads → Works again ✅

## 💡 **Tips for Free Tier**:
- **Demo ready**: Perfect for showcasing your app
- **Test thoroughly**: Upload different document types
- **Consider upgrade**: $7/month for persistent storage
- **Alternative**: Use Supabase free tier for persistence

## 🚀 **Deploy Command Summary**:

```powershell
# 1. Replace main.py with free tier version
copy "backend\main_freetier.py" "backend\main.py"

# 2. Push to GitHub
git add .
git commit -m "Free tier optimization"
git push origin main

# 3. Deploy on Render (follow steps above)
```

Your app will be live at:
- **Frontend**: https://ai-chatbot-app.onrender.com
- **Backend**: https://ai-chatbot-api.onrender.com

**Ready to deploy!** 🚀