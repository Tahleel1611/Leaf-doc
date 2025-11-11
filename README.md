# LeafDoc API Backend

FastAPI backend for LeafDoc plant disease detection application.

## Features

- 🌱 Plant disease classification using PyTorch models
- 📊 Grad-CAM visualization for model interpretability
- 💾 SQLite/PostgreSQL database with Alembic migrations
- 🔄 REST API with automatic OpenAPI documentation
- 🐳 Docker support for easy deployment
- ✅ Comprehensive test suite

## Tech Stack

- **Framework**: FastAPI 0.104+
- **Server**: Uvicorn with auto-reload
- **ML**: PyTorch 2.1, TorchVision, OpenCV
- **Database**: SQLAlchemy 2.0 with Alembic
- **Validation**: Pydantic 2.5
- **Testing**: Pytest with async support

## Project Structure

```
backend/
├── app/
│   ├── main.py              # FastAPI application
│   ├── config.py            # Configuration with pydantic-settings
│   ├── deps.py              # Dependency injection
│   ├── db.py                # Database setup
│   ├── models.py            # SQLAlchemy models
│   ├── schemas.py           # Pydantic schemas
│   ├── routers/             # API endpoints
│   │   ├── predict.py       # POST /api/predict
│   │   ├── history.py       # GET /api/history
│   │   └── feedback.py      # POST /api/feedback
│   ├── services/            # Business logic
│   │   ├── inference.py     # Model inference
│   │   ├── gradcam.py       # Visualization
│   │   └── storage.py       # File management
│   └── utils/
│       └── tips.py          # Disease care tips
├── migrations/              # Alembic migrations
├── tests/                   # Test suite
├── models/                  # PyTorch model files
├── storage/                 # Uploaded images & heatmaps
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```

## Quick Start

### Prerequisites

- Python 3.11+
- pip or poetry

### Installation

1. **Clone and navigate to backend directory**:

```bash
cd backend
```

2. **Create virtual environment**:

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

3. **Install dependencies**:

```bash
pip install -r requirements.txt
```

4. **Create .env file**:

```bash
cp .env.example .env
```

5. **Run database migrations**:

```bash
alembic upgrade head
```

6. **Start development server**:

```bash
uvicorn app.main:app --reload
```

The API will be available at:

- API: http://localhost:8000
- Docs: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### Using Makefile

```bash
# Start development server
make dev

# Run tests
make test

# Format code
make format

# Lint code
make lint

# Run migrations
make migrate
```

## Configuration

Configure the application via environment variables or `.env` file:

```env
# Application
APP_NAME=LeafDoc
API_PREFIX=/api
LOG_LEVEL=INFO

# Model & Storage
MODEL_PATH=models/leafdoc_mobilev3.ts  # TorchScript model
STORAGE_DIR=storage

# Database
DATABASE_URL=sqlite:///./leafdoc.db
# For PostgreSQL:
# DATABASE_URL=postgresql://user:password@localhost:5432/leafdoc

# CORS
CORS_ORIGINS=*  # Or comma-separated: http://localhost:5173,http://localhost:3000

# Server
HOST=0.0.0.0
PORT=8000
```

## API Endpoints

### Health Check

```http
GET /health
```

Returns API health status and model load state.

### Predict Disease

```http
POST /api/predict
Content-Type: multipart/form-data

Parameters:
- file: Image file (JPEG, PNG)

Response:
{
  "id": "uuid",
  "class": "disease_name",
  "confidence": 0.95,
  "tips": "Care recommendations...",
  "image_url": "/static/images/uuid.jpg",
  "heatmap_url": "/static/heatmaps/uuid.jpg",
  "created_at": "2025-11-09T10:00:00"
}
```

### Get History

```http
GET /api/history?page=1&limit=20&label=apple&correct=true

Query Parameters:
- page: Page number (default: 1)
- limit: Items per page (default: 20, max: 100)
- label: Filter by disease label
- correct: Filter by feedback (true/false)
- from: Filter from date (ISO format)
- to: Filter to date (ISO format)

Response:
{
  "items": [...],
  "total": 100,
  "page": 1,
  "limit": 20,
  "pages": 5
}
```

### Submit Feedback

```http
POST /api/feedback
Content-Type: application/json

{
  "id": "prediction-uuid",
  "correct": false,
  "true_label": "actual_disease_name"
}

Response:
{
  "id": "uuid",
  "pred_label": "predicted_disease",
  "feedback": {
    "correct": false,
    "true_label": "actual_disease_name"
  },
  ...
}
```

## Model Support

### With TorchScript Model

Place your TorchScript model at `models/leafdoc_mobilev3.ts`:

```python
# Export PyTorch model to TorchScript
model.eval()
example = torch.rand(1, 3, 224, 224)
traced = torch.jit.trace(model, example)
traced.save("models/leafdoc_mobilev3.ts")
```

### Without Model (Development)

If no model is found, the API uses stub predictions:

- Returns deterministic fake classifications
- Confidence fixed at 0.42
- Skips Grad-CAM generation
- Perfect for frontend development!

## Database

### Using SQLite (Default)

```env
DATABASE_URL=sqlite:///./leafdoc.db
```

### Using PostgreSQL

```env
DATABASE_URL=postgresql://user:password@localhost:5432/leafdoc
```

### Migrations

```bash
# Create new migration
alembic revision --autogenerate -m "Description"

# Apply migrations
alembic upgrade head

# Rollback
alembic downgrade -1
```

## Docker Deployment

### Build and run with Docker Compose

```bash
# Build and start
docker-compose up -d

# View logs
docker-compose logs -f

# Stop
docker-compose down
```

### Using PostgreSQL in Docker

Uncomment the `postgres` service in `docker-compose.yml` and update the environment variables.

## Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app --cov-report=html

# Run specific test file
pytest tests/test_predict.py

# Run with verbose output
pytest -v -s
```

## Development

### Code Quality

The project uses:

- **Black**: Code formatting
- **isort**: Import sorting
- **Ruff**: Fast linting
- **mypy**: Type checking

```bash
# Format code
black .
isort .

# Lint
ruff check .

# Type check
mypy app/
```

### Pre-commit Hooks

```bash
# Install pre-commit
pip install pre-commit

# Setup hooks
pre-commit install

# Run manually
pre-commit run --all-files
```

## Troubleshooting

### Model not loading

- Check `MODEL_PATH` in `.env`
- Verify model file exists and is valid TorchScript
- Check logs for detailed error messages
- API will work with stub predictions if model is missing

### Database errors

- Run migrations: `alembic upgrade head`
- Check `DATABASE_URL` configuration
- For PostgreSQL, ensure database exists

### Storage issues

- Ensure `storage/images` and `storage/heatmaps` directories exist
- Check file permissions
- Verify `STORAGE_DIR` in `.env`

### CORS errors

- Update `CORS_ORIGINS` in `.env`
- Use `*` for development or specific origins for production

## Production Deployment

### Environment Variables

Set these for production:

```env
LOG_LEVEL=WARNING
CORS_ORIGINS=https://yourdomain.com
DATABASE_URL=postgresql://user:pass@host/db
```

### Using Gunicorn

```bash
pip install gunicorn

gunicorn app.main:app \
  --workers 4 \
  --worker-class uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:8000
```

### Behind Reverse Proxy

Configure nginx or similar:

```nginx
location /api {
    proxy_pass http://localhost:8000;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
}

location /static {
    proxy_pass http://localhost:8000;
}
```

## License

MIT License - See LICENSE file for details

## Support

For issues and questions:

- Open an issue on GitHub
- Check the API documentation at `/docs`
- Review test files for usage examples
