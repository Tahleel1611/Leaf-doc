# ✅ LeafDoc Setup Checklist

Use this checklist to ensure everything is properly configured for the frontend-backend integration.

## Backend Setup

### 1. Environment Setup

- [ ] Python 3.11+ installed
- [ ] Virtual environment created (`python -m venv venv`)
- [ ] Virtual environment activated
- [ ] Dependencies installed (`pip install -r requirements.txt`)

### 2. Configuration

- [ ] `.env` file created from `.env.example`
- [ ] `CORS_ORIGINS` includes frontend URL (e.g., `http://localhost:5173`)
- [ ] `DATABASE_URL` configured (default SQLite is fine)
- [ ] `STORAGE_DIR` configured (default: `storage`)

### 3. Database

- [ ] `storage/images` directory exists
- [ ] `storage/heatmaps` directory exists
- [ ] Database migrations run (`alembic upgrade head`)

### 4. Backend Running

- [ ] Backend starts without errors
- [ ] Health check works: `curl http://localhost:8000/health`
- [ ] API docs accessible: http://localhost:8000/docs
- [ ] No error messages in terminal

### 5. Optional: Model

- [ ] Model file placed at `models/leafdoc_mobilev3.ts` (optional)
- [ ] Or using stub predictions for development (default)

## Frontend Setup

### 1. Environment Setup

- [ ] Node.js 18+ installed
- [ ] npm or yarn available
- [ ] Dependencies installed (`npm install`)

### 2. Configuration

- [ ] `.env` file created from `.env.example`
- [ ] `VITE_API_BASE_URL=http://localhost:8000` configured

### 3. Frontend Running

- [ ] Frontend starts without errors (`npm run dev`)
- [ ] App accessible at http://localhost:5173
- [ ] No compilation errors

## Integration Tests

### 1. Connection Test

- [ ] Run `python test_connection.py` - all tests pass
- [ ] Health endpoint returns 200 OK
- [ ] CORS headers present in responses
- [ ] No connection errors

### 2. Frontend-Backend Communication

- [ ] Open http://localhost:5173 in browser
- [ ] Navigate to "Detect" page
- [ ] Upload an image (any JPG/PNG)
- [ ] Click "Analyze Plant"
- [ ] Result appears with disease name, confidence, and tips
- [ ] No CORS errors in browser console (F12)
- [ ] No 404 or 500 errors

### 3. Static Files

- [ ] Image URL works in result (shows uploaded image)
- [ ] Heatmap URL works if model is loaded
- [ ] Images display correctly in UI

### 4. History Page

- [ ] Navigate to "History" page
- [ ] Previous prediction appears in table
- [ ] Can view details by clicking on item
- [ ] Pagination works (if >20 items)
- [ ] Filters work (try filtering by disease name)

### 5. Feedback System

- [ ] Click on a history item
- [ ] Side panel opens with details
- [ ] Can mark as "Correct" or "Incorrect"
- [ ] Feedback saves successfully
- [ ] Feedback icon appears in history table

## Browser Console Check

Open browser console (F12) and verify:

- [ ] No CORS errors
- [ ] No 404 Not Found errors
- [ ] No 500 Internal Server errors
- [ ] API requests show 200 OK status
- [ ] No TypeScript/JavaScript errors

## Backend Logs Check

In backend terminal, verify:

- [ ] Requests logged: `Request started: POST /api/predict`
- [ ] Successful responses: `Request completed: ... Status: 200`
- [ ] No Python exceptions or stack traces
- [ ] Processing time reasonable (< 5s per request)

## Common Issues Resolved

### ✅ CORS Error

```
Access to fetch at 'http://localhost:8000/api/predict' has been blocked by CORS policy
```

**Solution**: Updated `CORS_ORIGINS` in backend `.env` to include frontend URL

### ✅ Connection Refused

```
Failed to fetch
```

**Solution**: Backend is running on port 8000, verified with health check

### ✅ 404 Not Found on /api/predict

```
404 Not Found
```

**Solution**: Verified `API_PREFIX=/api` in backend config

### ✅ Images Not Displaying

```
Failed to load resource: 404
```

**Solution**: Created `storage/images` and `storage/heatmaps` directories

## Performance Check

- [ ] Image upload completes in < 2 seconds
- [ ] Prediction returns in < 5 seconds (stub) or < 10 seconds (with model)
- [ ] History loads in < 1 second
- [ ] UI remains responsive during requests
- [ ] No memory leaks or performance degradation

## Security Check (For Production)

- [ ] HTTPS enabled
- [ ] CORS restricted to specific domains
- [ ] Authentication added (if required)
- [ ] Rate limiting configured
- [ ] Input validation working
- [ ] SQL injection prevented (using SQLAlchemy ORM ✓)
- [ ] File upload size limited
- [ ] Logs don't expose sensitive data

## Deployment Ready

- [ ] All tests pass
- [ ] Environment variables configured for production
- [ ] Database backed up (if using data)
- [ ] Model file available (if using real model)
- [ ] Static files accessible
- [ ] HTTPS certificates configured
- [ ] Monitoring set up
- [ ] Error tracking configured

## 🎉 Success Criteria

Your setup is complete when:

1. ✅ Backend running on http://localhost:8000
2. ✅ Frontend running on http://localhost:5173
3. ✅ Can upload image and get prediction
4. ✅ Can view history of predictions
5. ✅ Can submit feedback
6. ✅ Images display correctly
7. ✅ No errors in console or terminal

---

## Next Steps

Once all items are checked:

1. **Test with real data**: Upload actual plant images
2. **Add your model**: Place trained model in `backend/models/`
3. **Customize**: Modify UI colors, add features, etc.
4. **Deploy**: Follow production deployment guide
5. **Monitor**: Set up logging and analytics

## Need Help?

- **Integration issues**: See [INTEGRATION_GUIDE.md](INTEGRATION_GUIDE.md)
- **Backend issues**: See [backend/README.md](backend/README.md)
- **API examples**: See [backend/API_EXAMPLES.md](backend/API_EXAMPLES.md)
- **Test connection**: Run `python test_connection.py`

---

**Date Completed**: ******\_******

**Notes**:

---

---

---
