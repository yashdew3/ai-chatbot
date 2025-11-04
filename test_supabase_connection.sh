#!/bin/bash
# Test script to verify local Supabase backend connection

echo "🔧 Testing Local Supabase Backend Connection..."
echo "Backend should be running on: http://localhost:8000"
echo ""

# Test 1: Health check
echo "1️⃣ Testing health check endpoint..."
curl -s http://localhost:8000/ | jq . || echo "❌ Health check failed"
echo ""

# Test 2: Connection test
echo "2️⃣ Testing connection test endpoint..."
curl -s http://localhost:8000/test | jq . || echo "❌ Connection test failed"
echo ""

# Test 3: Check data sources
echo "3️⃣ Testing data sources endpoint..."
curl -s http://localhost:8000/api/v1/data/sources | jq . || echo "❌ Data sources test failed"
echo ""

echo "✅ All tests completed!"
echo ""
echo "📋 Instructions:"
echo "1. Make sure backend is running: & \"E:\chatbot\chatbot-mvp\Chatbot - Copy\backend\start_supabase.bat\""
echo "2. Open frontend: http://localhost:8080/admin"
echo "3. Upload a PDF document"
echo "4. Watch backend terminal for detailed logs"
echo "5. Check Supabase dashboard for stored documents"