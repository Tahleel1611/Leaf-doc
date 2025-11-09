# 🚀 LeafDoc Quick Reference

## Start Commands

### Windows (Easy)

```bash
start-all.bat
```

### Manual Start

```bash
# Terminal 1 - Backend
cd backend
venv\Scripts\activate
uvicorn app.main:app --reload

# Terminal 2 - Frontend
cd leafdoc-plant-aid
npm run dev
```

## URLs

| Service      | URL                          |
| ------------ | ---------------------------- |
| Frontend     | http://localhost:5173        |
| Backend API  | http://localhost:8000        |
| API Docs     | http://localhost:8000/docs   |
| Health Check | http://localhost:8000/health |

## Key Files

```
📁 Backend Config
   backend/.env                 # Environment variables
   backend/app/config.py        # Settings
   backend/alembic.ini          # Database config

📁 Frontend Config
   leafdoc-plant-aid/.env       # API URL
   leafdoc-plant-aid/src/lib/api-client.ts  # API client

📁 Documentation
   README.md                    # Main readme
   INTEGRATION_GUIDE.md         # Connection guide
   SETUP_CHECKLIST.md          # Setup checklist
   backend/README.md            # Backend docs
   backend/API_EXAMPLES.md      # Code examples
```

## Common Commands

### Backend

```bash
# Start server
uvicorn app.main:app --reload

# Run tests
pytest

# Database migration
alembic upgrade head

# Seed database
python seed_db.py 10

# Format code
black app/ tests/
isort app/ tests/
```

### Frontend

```bash
# Start dev server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview

# Run tests
npm test

# Type check
npm run type-check
```

## API Endpoints

```bash
# Health check
curl http://localhost:8000/health

# Predict (PowerShell)
curl -X POST http://localhost:8000/api/predict `
  -F "file=@C:\path\to\image.jpg"

# Get history
curl http://localhost:8000/api/history?page=1&limit=20

# Submit feedback
curl -X POST http://localhost:8000/api/feedback `
  -H "Content-Type: application/json" `
  -d '{"id":"uuid","correct":false,"true_label":"disease_name"}'
```

## Environment Variables

### Backend (.env)

```env
CORS_ORIGINS=http://localhost:5173,http://localhost:3000
DATABASE_URL=sqlite:///./leafdoc.db
MODEL_PATH=models/leafdoc_mobilev3.ts
STORAGE_DIR=storage
LOG_LEVEL=INFO
```

### Frontend (.env)

```env
VITE_API_BASE_URL=http://localhost:8000
```

## Troubleshooting

| Problem            | Solution                              |
| ------------------ | ------------------------------------- |
| CORS error         | Update `CORS_ORIGINS` in backend/.env |
| Connection refused | Ensure backend running on port 8000   |
| 404 Not Found      | Check API_PREFIX=/api in backend      |
| Images not showing | Create storage/images directory       |
| Database error     | Run `alembic upgrade head`            |

## Quick Tests

```bash
# Test backend connectivity
python test_connection.py

# Test health endpoint
curl http://localhost:8000/health

# Check logs
# Backend: Check terminal output
# Frontend: Press F12 in browser
```

## Project Structure

```
leaf-disease-detection/
├── backend/                 # FastAPI backend
│   ├── app/                # Application code
│   ├── migrations/         # Database migrations
│   ├── tests/              # Backend tests
│   ├── storage/            # Uploaded files
│   └── models/             # ML models
│
├── leafdoc-plant-aid/      # React frontend
│   ├── src/               # Source code
│   └── public/            # Static assets
│
├── start-all.bat          # Startup script
└── test_connection.py     # Test script
```

## Development Workflow

1. **Start both services**

   ```bash
   start-all.bat  # or manual start
   ```

2. **Make changes**

   - Backend: Edit files in `backend/app/`
   - Frontend: Edit files in `leafdoc-plant-aid/src/`
   - Both have hot reload enabled

3. **Test changes**

   - Backend: `pytest`
   - Frontend: `npm test`
   - Integration: Use the web UI

4. **Commit changes**
   ```bash
   git add .
   git commit -m "Description"
   git push
   ```

## Keyboard Shortcuts

### VS Code

- `Ctrl+Shift+P` - Command palette
- `Ctrl+`` - Toggle terminal
- `F5` - Start debugging

### Browser DevTools

- `F12` - Open developer tools
- `Ctrl+Shift+C` - Inspect element
- `Ctrl+Shift+I` - Console

## Support Resources

- 📖 Full docs: [README.md](README.md)
- 🔗 Integration: [INTEGRATION_GUIDE.md](INTEGRATION_GUIDE.md)
- ✅ Checklist: [SETUP_CHECKLIST.md](SETUP_CHECKLIST.md)
- 📚 API examples: [backend/API_EXAMPLES.md](backend/API_EXAMPLES.md)

## Status Check

```bash
# Backend
✓ Running on :8000
✓ Health check passes
✓ Database connected
✓ Storage dirs exist

# Frontend
✓ Running on :5173
✓ Can reach backend
✓ No CORS errors
✓ Assets loading

# Integration
✓ Can upload images
✓ Predictions working
✓ History displaying
✓ Feedback submits
```

---

**Version**: 1.0.0  
**Last Updated**: November 2025
