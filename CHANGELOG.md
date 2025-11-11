# Changelog

All notable changes to the LeafDoc API will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2025-11-09

### Added

- Initial release of LeafDoc FastAPI backend
- Plant disease classification endpoint (`POST /api/predict`)
- Prediction history endpoint with pagination and filters (`GET /api/history`)
- Feedback submission endpoint (`POST /api/feedback`)
- Health check endpoint (`GET /health`)
- PyTorch TorchScript model inference support
- Stub inference for development without model
- Grad-CAM visualization for model interpretability
- SQLAlchemy models for Predictions and Feedback
- Alembic database migrations
- Static file serving for images and heatmaps
- Comprehensive test suite with pytest
- Docker support with docker-compose
- PostgreSQL and SQLite database support
- CORS middleware for frontend integration
- Request logging with request ID tracking
- Disease-specific care tips and recommendations
- Automatic storage directory creation
- Database seeding script for development
- Quick start scripts for Windows and Linux
- Complete API documentation
- Pre-commit hooks for code quality
- Makefile for common development tasks

### Features

- **Model Support**: TorchScript model loading with fallback to stub predictions
- **Visualization**: Grad-CAM heatmap generation for predictions
- **Database**: SQLAlchemy ORM with Alembic migrations, supports SQLite and PostgreSQL
- **API**: RESTful endpoints with automatic OpenAPI documentation
- **Testing**: Comprehensive test coverage with pytest
- **Docker**: Production-ready containerization
- **Code Quality**: Black, isort, ruff, mypy, and pre-commit hooks
- **Development UX**: Quick start scripts, seeding, hot reload

### Technical Details

- Python 3.11+
- FastAPI 0.104+
- PyTorch 2.1+
- SQLAlchemy 2.0+
- Pydantic 2.5+ with settings management
- Uvicorn ASGI server
- Alembic for database migrations
- OpenCV for image processing
- PIL for image manipulation

### API Endpoints

- `GET /` - API information
- `GET /health` - Health check
- `POST /api/predict` - Image classification
- `GET /api/history` - Prediction history with filters
- `POST /api/feedback` - User feedback submission
- `GET /docs` - Swagger UI documentation
- `GET /redoc` - ReDoc documentation

### Configuration

- Environment-based configuration with `.env` support
- Configurable CORS origins
- Configurable database URL (SQLite/PostgreSQL)
- Configurable model path
- Configurable storage directory
- Configurable API prefix
- Configurable logging level

### Documentation

- Comprehensive README with quickstart guide
- API endpoint documentation
- Docker deployment guide
- Testing guide
- Development setup instructions
- Troubleshooting section
- Production deployment recommendations
