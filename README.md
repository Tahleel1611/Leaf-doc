# LeafDoc - Plant Disease Detection System

A full-stack web application for detecting plant diseases using deep learning, featuring a React frontend and FastAPI backend.

## 🌟 Features

- 🔍 **AI-Powered Detection** - Classify 25+ plant diseases with confidence scores
- 🎨 **Grad-CAM Visualization** - See which parts of the leaf influenced the diagnosis
- 📊 **History Tracking** - View and manage all past detections
- 💬 **Feedback System** - Correct predictions and improve the model
- 🎯 **Care Recommendations** - Get actionable tips for each detected disease
- 🌓 **Dark Mode** - Comfortable viewing in any lighting
- 📱 **Responsive Design** - Works on desktop, tablet, and mobile

## 🏗️ Architecture

```
leafdoc-plant-aid/          # React + TypeScript frontend
backend/                    # FastAPI + Python backend
```

### Frontend Stack

- ⚛️ React 18 + TypeScript
- 🎨 Tailwind CSS + shadcn/ui
- 🔄 TanStack Query (React Query)
- 🚀 Vite

### Backend Stack

- ⚡ FastAPI + Uvicorn
- 🤖 PyTorch for ML inference
- 💾 SQLAlchemy + Alembic
- 🐘 SQLite/PostgreSQL

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- Node.js 18+
- npm or yarn

### Option 1: Automated Setup (Windows)

```bash
# Run the startup script
start-all.bat
```

This will:

1. Set up backend (create venv, install dependencies)
2. Set up frontend (npm install)
3. Start both services
4. Open the app in your browser

### Option 2: Manual Setup

#### Backend Setup

```bash
# Navigate to backend
cd backend

# Create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac

# Install dependencies
pip install -r requirements.txt

# Create .env file
copy .env.example .env  # Windows
cp .env.example .env    # Linux/Mac

# Run migrations
alembic upgrade head

# Start server
uvicorn app.main:app --reload
```

Backend runs on: **http://localhost:8000**

#### Frontend Setup

```bash
# Navigate to frontend
cd leafdoc-plant-aid

# Install dependencies
npm install

# Create .env file
copy .env.example .env  # Windows
cp .env.example .env    # Linux/Mac

# Start dev server
npm run dev
```

Frontend runs on: **http://localhost:5173**

### Verify Connection

```bash
# Test backend connectivity
python test_connection.py
```

## 📖 Documentation

- **[Integration Guide](INTEGRATION_GUIDE.md)** - Connecting frontend and backend
- **[Backend README](backend/README.md)** - Backend setup and API docs
- **[API Examples](backend/API_EXAMPLES.md)** - Code examples for all endpoints
- **[Frontend README](leafdoc-plant-aid/README.md)** - Frontend setup and components

## 🔗 Access Points

Once running:

- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:8000
- **API Docs (Swagger)**: http://localhost:8000/docs
- **API Docs (ReDoc)**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health

## 🎯 Usage

### 1. Detect Disease

1. Navigate to the **Detect** page
2. Upload a photo of a plant leaf
3. Click **Analyze Plant**
4. View the diagnosis, confidence score, and care tips
5. Toggle Grad-CAM visualization to see the model's focus areas

### 2. View History

1. Navigate to the **History** page
2. Browse all past detections
3. Filter by disease type or feedback status
4. Click on any item to view details

### 3. Submit Feedback

1. Open any prediction from history
2. Mark as "Correct" or "Incorrect"
3. If incorrect, provide the actual disease name
4. Feedback is stored for model improvement

## 🐳 Docker Deployment

```bash
# Start with Docker Compose
cd backend
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

## 🧪 Testing

### Backend Tests

```bash
cd backend
pytest
pytest --cov=app  # With coverage
```

### Frontend Tests

```bash
cd leafdoc-plant-aid
npm test
```

## 📁 Project Structure

```
.
├── backend/                    # FastAPI backend
│   ├── app/
│   │   ├── main.py            # FastAPI app
│   │   ├── routers/           # API endpoints
│   │   ├── services/          # Business logic
│   │   ├── models.py          # Database models
│   │   └── schemas.py         # Pydantic schemas
│   ├── migrations/            # Alembic migrations
│   ├── tests/                 # Backend tests
│   ├── storage/               # Uploaded images & heatmaps
│   ├── models/                # ML model files
│   └── requirements.txt
│
├── leafdoc-plant-aid/         # React frontend
│   ├── src/
│   │   ├── pages/             # Route pages
│   │   ├── components/        # React components
│   │   ├── lib/               # Utilities & API client
│   │   └── store/             # State management
│   ├── public/
│   └── package.json
│
├── start-all.bat              # Startup script (Windows)
├── test_connection.py         # Integration test script
└── INTEGRATION_GUIDE.md       # Integration documentation
```

## 🔧 Configuration

### Backend (.env)

```env
APP_NAME=LeafDoc
API_PREFIX=/api
MODEL_PATH=models/leafdoc_mobilev3.ts
STORAGE_DIR=storage
DATABASE_URL=sqlite:///./leafdoc.db
CORS_ORIGINS=http://localhost:5173,http://localhost:3000
LOG_LEVEL=INFO
```

### Frontend (.env)

```env
VITE_API_BASE_URL=http://localhost:8000
```

## 🤖 Model Support

### Development (No Model)

The backend works without a trained model:

- Uses stub predictions (deterministic fake results)
- Returns confidence of 0.42
- Perfect for frontend development!

### Production (With Model)

Place your TorchScript model at: `backend/models/leafdoc_mobilev3.ts`

To export a PyTorch model:

```python
import torch

model.eval()
example = torch.rand(1, 3, 224, 224)
traced = torch.jit.trace(model, example)
traced.save("backend/models/leafdoc_mobilev3.ts")
```

## 🌱 Supported Diseases

- **Apple**: Scab, Black Rot, Cedar Rust, Healthy
- **Corn**: Cercospora Leaf Spot, Common Rust, Northern Leaf Blight, Healthy
- **Grape**: Black Rot, Esca, Leaf Blight, Healthy
- **Potato**: Early Blight, Late Blight, Healthy
- **Tomato**: 9 diseases including Early Blight, Late Blight, Leaf Mold, etc.

## 🐛 Troubleshooting

### CORS Errors

- Verify `CORS_ORIGINS` in backend `.env` includes your frontend URL
- Restart backend after changing .env

### Connection Refused

- Ensure backend is running on port 8000
- Check firewall settings
- Verify `VITE_API_BASE_URL` in frontend `.env`

### Images Not Displaying

- Ensure `storage/images` and `storage/heatmaps` directories exist
- Check file permissions
- Verify static file mounting in backend

### Database Errors

- Run migrations: `alembic upgrade head`
- Check database file permissions
- For PostgreSQL, ensure database exists

## 📊 API Endpoints

| Method | Endpoint        | Description            |
| ------ | --------------- | ---------------------- |
| GET    | `/health`       | Health check           |
| POST   | `/api/predict`  | Analyze plant image    |
| GET    | `/api/history`  | Get prediction history |
| POST   | `/api/feedback` | Submit feedback        |
| GET    | `/docs`         | Swagger UI             |
| GET    | `/redoc`        | ReDoc documentation    |

## 🔒 Security Notes

For production deployment:

- Enable HTTPS
- Add authentication (JWT/OAuth)
- Restrict CORS origins
- Use environment secrets management
- Enable rate limiting
- Set up monitoring and logging

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📝 License

MIT License - See [LICENSE](backend/LICENSE) for details

## 🆘 Support

- **Documentation**: Check the `/docs` folder
- **API Docs**: http://localhost:8000/docs (when running)
- **Issues**: Open a GitHub issue
- **Integration**: See [INTEGRATION_GUIDE.md](INTEGRATION_GUIDE.md)

## 🎉 Acknowledgments

- Plant disease dataset providers
- OpenAI for development assistance
- shadcn/ui for beautiful components
- FastAPI for the amazing framework

---

**Made with 💚 for plant lovers and developers**
