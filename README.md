# 🌿 MulberryCare AI

AI-Powered Mulberry Health & Sericulture Support Platform.

Helps mulberry/sericulture farmers identify plant health issues from photos and get
trusted, understandable treatment and prevention guidance — in English and Tamil.

## Status

Phase 1: project architecture & setup. Core features (auth, AI diagnosis, chatbot,
marketplace) are not implemented yet — see project phases below.

## Project Structure

```
mulberrycare/
├── backend/        FastAPI app (API, models, schemas, services, database, ai)
├── frontend/        Browser-based prototype UI
├── ml/              Datasets, notebooks, training, evaluation, trained models
├── docs/            Project documentation
├── tests/           Automated tests
├── .env.example
└── .gitignore
```

## Tech Stack

- **Backend:** Python + FastAPI
- **Frontend:** HTML/CSS/JavaScript (prototype)
- **AI:** PyTorch/TensorFlow, OpenCV, NumPy (added in later phase)
- **Database:** TBD (Phase 2)

## Running Locally

### Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Visit `http://localhost:8000/api/health` — should return `{"status": "ok"}`.

### Frontend

Open `frontend/index.html` in a browser (or serve it with any static server).
It calls the backend health endpoint to confirm connectivity.

## Development Phases

1. Architecture & setup ✅ (current)
2. Authentication
3. Farmer profile & onboarding
4. Mulberry variety management
5. Image upload/camera workflow
6. Disease prediction module
7. Disease result & treatment advisory
8. Diagnosis history
9. Tamil/English localization
10. Chatbot ("Ask MulberryCare")
11. Cocoon marketplace
12. Factory module
13. Admin/moderation
14. Testing, security & deployment

## Future Improvements

Automatic variety recognition, disease severity segmentation, IoT/drone integration,
yield & price prediction, silkworm disease detection, government scheme integration.
