# Frontend-Backend Integration Guide

This guide explains how to connect the LeafDoc React frontend with the FastAPI backend.

## Quick Start

### 1. Start the Backend

```bash
# Terminal 1 - Backend
cd backend
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt
uvicorn app.main:app --reload
```

The backend will run on: **http://localhost:8000**

### 2. Start the Frontend

```bash
# Terminal 2 - Frontend
cd leafdoc-plant-aid
npm install
npm run dev
```

The frontend will run on: **http://localhost:5173**

### 3. Test the Connection

1. Open http://localhost:5173
2. Navigate to "Detect" page
3. Upload a plant image
4. Click "Analyze Plant"
5. View results with disease classification and tips

## Configuration

### Frontend Environment (.env)

Located at: `leafdoc-plant-aid/.env`

```env
VITE_API_BASE_URL=http://localhost:8000
```

### Backend Environment (.env)

Located at: `backend/.env`

```env
# CORS - Allow frontend origins
CORS_ORIGINS=http://localhost:5173,http://localhost:3000,http://localhost:5174

# Other settings...
APP_NAME=LeafDoc
API_PREFIX=/api
DATABASE_URL=sqlite:///./leafdoc.db
STORAGE_DIR=storage
```

## API Integration Details

### Architecture

```
Frontend (React + TypeScript)
    ↓ HTTP Requests
API Client (api-client.ts)
    ↓ REST API
Backend (FastAPI + Python)
    ↓
Database (SQLite/PostgreSQL)
```

### Endpoints Connected

#### 1. Predict Disease

**Frontend:** `src/pages/Detect.tsx`
**Backend:** `POST /api/predict`

```typescript
// Frontend call
const result = await apiClient.predict(imageFile);

// Backend returns
{
  "id": "uuid",
  "class": "tomato_early_blight",
  "confidence": 0.95,
  "tips": "Care recommendations...",
  "image_url": "/static/images/uuid.jpg",
  "heatmap_url": "/static/heatmaps/uuid.jpg",
  "created_at": "2025-11-09T10:00:00"
}
```

#### 2. Get History

**Frontend:** `src/pages/History.tsx`
**Backend:** `GET /api/history`

```typescript
// Frontend call
const history = await apiClient.getHistory({
  page: 1,
  limit: 20,
  label: "tomato",
  correct: true
});

// Backend returns
{
  "items": [...],
  "total": 150,
  "page": 1,
  "limit": 20,
  "pages": 8
}
```

#### 3. Submit Feedback

**Frontend:** `src/components/SidePanel.tsx`
**Backend:** `POST /api/feedback`

```typescript
// Frontend call
await apiClient.submitFeedback({
  id: "prediction-uuid",
  correct: false,
  true_label: "actual_disease",
});
```

## Data Flow

### 1. Image Upload & Prediction

```
User uploads image
    ↓
Frontend: Detect.tsx
    ↓
API Client: predict(file)
    ↓
Backend: POST /api/predict
    ↓
- Save image to storage/images/
- Run ML inference
- Generate Grad-CAM heatmap
- Save to database
    ↓
Return PredictResponse
    ↓
Frontend: Display in ResultCard
```

### 2. View History

```
User navigates to History page
    ↓
Frontend: History.tsx → HistoryTable
    ↓
API Client: getHistory(params)
    ↓
Backend: GET /api/history
    ↓
- Query database with filters
- Join with feedback table
- Paginate results
    ↓
Return HistoryResponse
    ↓
Frontend: Display in table
```

### 3. Submit Feedback

```
User clicks "Mark as incorrect"
    ↓
Frontend: SidePanel feedback form
    ↓
API Client: submitFeedback(data)
    ↓
Backend: POST /api/feedback
    ↓
- Validate prediction exists
- Create/update feedback record
- Return updated item
    ↓
Frontend: Update UI, show toast
```

## Static Files

The backend serves uploaded images and heatmaps via static file mounting:

```python
# Backend: app/main.py
app.mount("/static", StaticFiles(directory="storage"), name="static")
```

Frontend accesses via:

- Images: `http://localhost:8000/static/images/{uuid}.jpg`
- Heatmaps: `http://localhost:8000/static/heatmaps/{uuid}.jpg`

These URLs are returned in API responses and displayed in frontend components.

## CORS Configuration

The backend is configured to accept requests from frontend development servers:

```python
# Backend: app/main.py
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## Type Safety

Frontend TypeScript types match backend Pydantic schemas:

| Frontend Type     | Backend Schema    | Endpoint           |
| ----------------- | ----------------- | ------------------ |
| `PredictResponse` | `PredictResponse` | POST /api/predict  |
| `HistoryItem`     | `HistoryItem`     | GET /api/history   |
| `HistoryResponse` | `HistoryResponse` | GET /api/history   |
| `FeedbackRequest` | `FeedbackCreate`  | POST /api/feedback |

## Error Handling

### Frontend

```typescript
try {
  const result = await apiClient.predict(file);
  toast.success("Analysis complete!");
} catch (error) {
  toast.error("Analysis failed", {
    description: error.message,
  });
}
```

### Backend

```python
try:
    # Process request
    return response
except Exception as e:
    logger.error(f"Error: {e}")
    raise HTTPException(status_code=500, detail=str(e))
```

## Development Workflow

### 1. Both Services Running

```bash
# Terminal 1 - Backend
cd backend
venv\Scripts\activate
uvicorn app.main:app --reload

# Terminal 2 - Frontend
cd leafdoc-plant-aid
npm run dev
```

### 2. Without Model (Development)

The backend works perfectly without a trained model:

- Uses stub predictions (deterministic fake results)
- Returns confidence of 0.42
- Skips Grad-CAM generation
- Perfect for frontend development!

### 3. With Model (Production)

Place your TorchScript model at `backend/models/leafdoc_mobilev3.ts`:

- Backend auto-loads on startup
- Performs real inference
- Generates Grad-CAM heatmaps

## Testing the Integration

### 1. Health Check

```bash
curl http://localhost:8000/health
```

Should return:

```json
{
  "status": "healthy",
  "app_name": "LeafDoc",
  "model_loaded": false
}
```

### 2. Test Prediction via Frontend

1. Open http://localhost:5173/detect
2. Upload test image
3. Check browser console for API calls
4. Verify response data

### 3. Check Backend Logs

Backend terminal shows:

```
INFO: Request started: POST /api/predict
INFO: Saved image to storage/images/uuid.jpg
INFO: Prediction: tomato_early_blight with confidence 0.42
INFO: Request completed: POST /api/predict Status: 200
```

## Troubleshooting

### CORS Errors

**Problem:** "Access-Control-Allow-Origin" error

**Solution:**

1. Check backend `.env` has correct CORS_ORIGINS
2. Restart backend after changing .env
3. Verify frontend is using correct API_BASE_URL

### Connection Refused

**Problem:** Cannot connect to backend

**Solution:**

1. Ensure backend is running on port 8000
2. Check firewall settings
3. Verify URL in frontend .env

### 404 Not Found

**Problem:** API endpoints return 404

**Solution:**

1. Check API_PREFIX in backend config (should be `/api`)
2. Verify frontend uses correct endpoint paths
3. Check backend logs for routing errors

### Image Not Displaying

**Problem:** Uploaded images don't show

**Solution:**

1. Ensure `storage/images` directory exists
2. Check static files are mounted in backend
3. Verify image URLs in API response

### Database Errors

**Problem:** Database connection issues

**Solution:**

1. Run migrations: `alembic upgrade head`
2. Check DATABASE_URL in backend .env
3. Ensure SQLite file has write permissions

## Production Deployment

### Environment Variables

**Frontend (.env.production)**

```env
VITE_API_BASE_URL=https://api.yourdomain.com
```

**Backend (.env.production)**

```env
CORS_ORIGINS=https://yourdomain.com
DATABASE_URL=postgresql://user:pass@host/db
LOG_LEVEL=WARNING
```

### Deployment Options

#### Option 1: Separate Hosting

- Frontend: Vercel/Netlify
- Backend: Railway/Render/AWS

#### Option 2: Docker Compose

```bash
docker-compose up -d
```

#### Option 3: Kubernetes

Use provided manifests (if available)

## API Documentation

When backend is running, access:

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Monitoring

### Backend Logs

Check `backend/logs/` for detailed logs

### Request IDs

Each request has a unique ID for tracing:

```
X-Request-ID: abc123...
```

### Performance

Check response times in backend logs:

```
Request completed: POST /api/predict Status: 200 Time: 0.1234s
```

## Next Steps

1. ✅ Backend and Frontend running
2. ✅ API integration working
3. 🔄 Add your trained model
4. 🔄 Test with real plant images
5. 🔄 Deploy to production

## Support

- Backend docs: `backend/README.md`
- API examples: `backend/API_EXAMPLES.md`
- Frontend: Check component comments
- Issues: Open GitHub issue

---

**Success Checklist:**

- [ ] Backend running on port 8000
- [ ] Frontend running on port 5173
- [ ] Can upload and analyze images
- [ ] Can view history
- [ ] Can submit feedback
- [ ] Images and heatmaps display correctly
- [ ] No CORS errors in console
