# LeafDoc Backend - Setup Complete! 🎉

## What Has Been Created

A complete, production-ready FastAPI backend for plant disease detection with the following structure:

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI app with CORS, logging, static files
│   ├── config.py               # Pydantic settings configuration
│   ├── deps.py                 # Dependency injection
│   ├── db.py                   # Database setup
│   ├── models.py               # SQLAlchemy models (Prediction, Feedback)
│   ├── schemas.py              # Pydantic schemas for validation
│   │
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── predict.py          # POST /api/predict
│   │   ├── history.py          # GET /api/history
│   │   └── feedback.py         # POST /api/feedback
│   │
│   ├── services/
│   │   ├── __init__.py
│   │   ├── inference.py        # PyTorch model inference
│   │   ├── gradcam.py          # Grad-CAM visualization
│   │   └── storage.py          # File storage management
│   │
│   └── utils/
│       ├── __init__.py
│       └── tips.py             # Disease care tips
│
├── migrations/
│   ├── env.py                  # Alembic environment
│   ├── script.py.mako          # Migration template
│   └── versions/
│       └── 001_initial_migration.py
│
├── tests/
│   ├── __init__.py
│   ├── conftest.py             # Pytest fixtures
│   ├── test_predict.py         # Prediction tests
│   ├── test_history.py         # History tests
│   ├── test_feedback.py        # Feedback tests
│   └── test_health.py          # Health check tests
│
├── storage/
│   └── .gitkeep
├── models/
│   └── .gitkeep
│
├── Dockerfile                  # Multi-stage production build
├── docker-compose.yml          # Docker services
├── requirements.txt            # Python dependencies
├── alembic.ini                 # Alembic configuration
├── pyproject.toml              # Tool configurations
├── .env.example                # Environment template
├── .gitignore                  # Git ignore patterns
├── .pre-commit-config.yaml     # Pre-commit hooks
├── Makefile                    # Development commands
├── README.md                   # Comprehensive documentation
├── CHANGELOG.md                # Version history
├── seed_db.py                  # Database seeding script
├── start.bat                   # Windows quick start
├── start.sh                    # Linux/Mac quick start
└── classes.json                # Disease class labels
```

## Key Features Implemented ✅

### 1. API Endpoints

- ✅ **POST /api/predict** - Image upload and disease classification
- ✅ **GET /api/history** - Paginated history with filters (label, correct, date range)
- ✅ **POST /api/feedback** - User feedback submission
- ✅ **GET /health** - Health check with model status
- ✅ **GET /** - API information

### 2. Model Inference

- ✅ TorchScript model loading with singleton pattern
- ✅ Stub predictions when model is absent (development mode)
- ✅ ImageNet preprocessing (224x224, normalize)
- ✅ Confidence scores (0-1 range)
- ✅ 25 disease classes supported

### 3. Grad-CAM Visualization

- ✅ Heatmap generation for predictions
- ✅ Image overlay creation
- ✅ Graceful fallback when unavailable
- ✅ Saved to storage and served via static files

### 4. Database

- ✅ SQLAlchemy 2.0 ORM models
- ✅ Prediction and Feedback tables with relationships
- ✅ UUID primary keys
- ✅ Timestamps and indexing
- ✅ SQLite (default) and PostgreSQL support
- ✅ Alembic migrations

### 5. Storage

- ✅ Local file storage for images and heatmaps
- ✅ Automatic directory creation
- ✅ Static file serving via FastAPI
- ✅ URL generation for frontend consumption
- ✅ Easy S3 integration (boto3 ready)

### 6. Configuration

- ✅ Pydantic settings with .env support
- ✅ Environment-based configuration
- ✅ CORS configuration
- ✅ Database URL flexibility
- ✅ Logging levels

### 7. Developer Experience

- ✅ Comprehensive test suite (pytest)
- ✅ Quick start scripts (Windows/Linux)
- ✅ Database seeding
- ✅ Hot reload in development
- ✅ Makefile commands
- ✅ Pre-commit hooks
- ✅ Code formatting (black, isort)
- ✅ Linting (ruff, mypy)

### 8. Production Ready

- ✅ Docker support with multi-stage build
- ✅ Docker Compose configuration
- ✅ Health checks
- ✅ Request logging with IDs
- ✅ Structured error handling
- ✅ Graceful startup/shutdown
- ✅ Static file serving
- ✅ CORS middleware

## Quick Start Guide 🚀

### Option 1: Quick Start Script (Recommended)

**Windows:**

```cmd
cd backend
start.bat
```

**Linux/Mac:**

```bash
cd backend
chmod +x start.sh
./start.sh
```

### Option 2: Manual Setup

```bash
# Navigate to backend
cd backend

# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate
# Activate (Linux/Mac)
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
copy .env.example .env  # Windows
cp .env.example .env    # Linux/Mac

# Create directories
mkdir storage\images storage\heatmaps models  # Windows
mkdir -p storage/images storage/heatmaps models  # Linux/Mac

# Run migrations
alembic upgrade head

# (Optional) Seed database
python seed_db.py 10

# Start server
uvicorn app.main:app --reload
```

### Option 3: Docker

```bash
cd backend
docker-compose up -d
```

## Access Points 🌐

Once running, access:

- **API**: http://localhost:8000
- **Interactive Docs**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health

## Testing the API 🧪

### Using curl (Windows PowerShell)

```powershell
# Health check
curl http://localhost:8000/health

# Predict (replace with actual image path)
curl -X POST http://localhost:8000/api/predict `
  -F "file=@path\to\image.jpg"

# Get history
curl http://localhost:8000/api/history

# Submit feedback
curl -X POST http://localhost:8000/api/feedback `
  -H "Content-Type: application/json" `
  -d '{\"id\":\"prediction-id\",\"correct\":true}'
```

### Using Python

```python
import requests

# Predict
with open("image.jpg", "rb") as f:
    response = requests.post(
        "http://localhost:8000/api/predict",
        files={"file": f}
    )
    print(response.json())

# History
response = requests.get("http://localhost:8000/api/history?page=1&limit=10")
print(response.json())

# Feedback
response = requests.post(
    "http://localhost:8000/api/feedback",
    json={"id": "prediction-id", "correct": True}
)
print(response.json())
```

## Development Commands 🛠️

Using Makefile (or run commands directly):

```bash
make dev          # Start development server
make test         # Run tests
make format       # Format code
make lint         # Lint code
make migrate      # Run migrations
make clean        # Clean generated files
make docker-up    # Start Docker
make docker-down  # Stop Docker
```

## Model Support 🤖

### Without Model (Development)

- API works with **stub predictions**
- Returns deterministic fake results (confidence = 0.42)
- No Grad-CAM generation
- Perfect for frontend development!

### With Model (Production)

1. Place TorchScript model at: `backend/models/leafdoc_mobilev3.ts`
2. Restart server
3. Real predictions and Grad-CAM will work

**Export PyTorch model to TorchScript:**

```python
import torch

model.eval()
example = torch.rand(1, 3, 224, 224)
traced = torch.jit.trace(model, example)
traced.save("models/leafdoc_mobilev3.ts")
```

## Supported Disease Classes 🌿

25 classes across 5 plant types:

- **Apple**: scab, black_rot, cedar_rust, healthy
- **Corn**: cercospora_leaf_spot, common_rust, northern_leaf_blight, healthy
- **Grape**: black_rot, esca, leaf_blight, healthy
- **Potato**: early_blight, late_blight, healthy
- **Tomato**: 9 diseases + healthy

See `classes.json` for full list.

## Environment Variables 📝

Key configurations in `.env`:

```env
# App
APP_NAME=LeafDoc
API_PREFIX=/api
LOG_LEVEL=INFO

# Model & Storage
MODEL_PATH=models/leafdoc_mobilev3.ts
STORAGE_DIR=storage

# Database
DATABASE_URL=sqlite:///./leafdoc.db
# Or PostgreSQL: postgresql://user:pass@host/db

# CORS
CORS_ORIGINS=*

# Server
HOST=0.0.0.0
PORT=8000
```

## Testing 🧪

```bash
# Run all tests
pytest

# With coverage
pytest --cov=app

# Specific test file
pytest tests/test_predict.py

# Verbose
pytest -v -s
```

## Troubleshooting 🔧

### Port 8000 already in use

```bash
# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Linux/Mac
lsof -ti:8000 | xargs kill -9
```

### Import errors

```bash
# Ensure in virtual environment
pip install -r requirements.txt
```

### Database errors

```bash
# Reset database
alembic downgrade base
alembic upgrade head
```

### Storage errors

```bash
# Recreate directories
mkdir storage\images storage\heatmaps  # Windows
mkdir -p storage/images storage/heatmaps  # Linux/Mac
```

## Next Steps 🎯

1. **Start the server**: `uvicorn app.main:app --reload`
2. **Test endpoints**: Visit http://localhost:8000/docs
3. **Connect frontend**: Update frontend API URL to `http://localhost:8000`
4. **Add your model**: Place TorchScript model in `models/` directory
5. **Deploy**: Use Docker or deploy to cloud platform

## Production Deployment 🚀

### Using Docker

```bash
docker-compose up -d
```

### Using Gunicorn

```bash
pip install gunicorn
gunicorn app.main:app \
  --workers 4 \
  --worker-class uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:8000
```

### Environment for Production

```env
LOG_LEVEL=WARNING
CORS_ORIGINS=https://yourdomain.com
DATABASE_URL=postgresql://user:pass@host/db
```

## Documentation 📚

- **README.md**: Complete usage guide
- **API Docs**: http://localhost:8000/docs (auto-generated)
- **CHANGELOG.md**: Version history
- **Code Comments**: Docstrings throughout

## Support 💬

If you encounter issues:

1. Check the logs in the terminal
2. Visit http://localhost:8000/docs for API testing
3. Review README.md for detailed instructions
4. Check .env configuration
5. Ensure all dependencies are installed

## Summary ✨

You now have a **fully functional FastAPI backend** with:

✅ Working endpoints for prediction, history, and feedback
✅ Database models and migrations
✅ Model inference with stub fallback
✅ Grad-CAM visualization
✅ Comprehensive test suite
✅ Docker support
✅ Development tools and scripts
✅ Production-ready configuration
✅ Complete documentation

**The API is ready to run!** Just execute `uvicorn app.main:app --reload` and start testing.

Enjoy building with LeafDoc! 🌱🔬
