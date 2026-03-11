# PlantDoc - Plant Disease Prediction Web App

A web app that helps farmers identify plant diseases by uploading a photo of a leaf. The app runs the image through a machine learning model and tells you what disease it found, how confident it is, and what to do about it.

Built as a capstone project for CSC 424 at the University of Southern Mississippi.

## What it does

- Users sign up, log in, and upload a photo of a sick-looking leaf
- The app resizes the image and feeds it to a CNN model
- It returns the disease name, a confidence score, and treatment info (what to do, how to prevent it, what chemicals to use)
- If the model isn't confident enough (below 70%), it tells the user to try again with a better photo
- Every diagnosis gets saved so users can go back and look at past results, filter by disease or date
- Admin users can add, edit, or delete diseases and treatments in the database

The prediction is currently simulated for prototyping. When the real trained model is ready, swap out the code inside `backend/services/prediction_service.py` and everything else stays the same.

## Project structure

```
plant-disease-app/
├── run.py                    # Entry point
├── requirements.txt          # Python dependencies
│
├── backend/                  # Server-side code
│   ├── __init__.py           # App factory (create_app)
│   ├── config.py             # App settings (DB path, upload limits)
│   ├── extensions.py         # Shared instances (database, login manager)
│   ├── seed.py               # Initial disease data loaded on first run
│   ├── models/               # Database tables (one file per table)
│   │   ├── user.py           # User model with password hashing
│   │   ├── disease.py        # Disease info, treatment, prevention
│   │   └── diagnosis.py      # Diagnosis records linking user + disease + image
│   ├── routes/               # URL handlers grouped by feature
│   │   ├── auth.py           # Register, login, logout
│   │   ├── diagnosis.py      # Upload, result, history, dashboard
│   │   └── admin.py          # Disease CRUD for admin users
│   └── services/             # Business logic (separated from routes)
│       ├── image_service.py   # Image validation, save, resize to 224x224
│       └── prediction_service.py  # Disease prediction (swap in real CNN here)
│
├── frontend/                 # Client-side code
│   ├── templates/            # Jinja2 HTML templates organized by feature
│   │   ├── base.html         # Shared layout with navbar and flash messages
│   │   ├── index.html        # Landing page
│   │   ├── auth/             # Login and register pages
│   │   ├── diagnosis/        # Dashboard, upload, result, history pages
│   │   └── admin/            # Disease management pages
│   └── static/
│       ├── css/style.css     # Responsive stylesheet (mobile-first)
│       └── js/app.js         # Upload drag-drop, camera, preview
│
├── demo_images/              # Sample diseased leaf images for testing
├── database/                 # SQLite database file (auto-created)
└── uploads/                  # User-uploaded images (auto-created)
```

## How to run it

```bash
git clone https://github.com/aashish-thapa/plant-disease-app
cd plant-disease-app

# Create a virtual environment and activate it
python -m venv venv
source venv/bin/activate        # On Mac/Linux
# venv\Scripts\activate         # On Windows

# Install dependencies and start the app
pip install -r requirements.txt
python run.py
```

Then open http://127.0.0.1:5000 in your browser.

## Demo accounts

An admin account is created automatically on first run:

| Role | Email | Password |
|------|-------|----------|
| Admin | admin@plantdoc.com | admin123 |
| Farmer | farmer@demo.com | demo123 |

Five demo images are included in `demo_images/` for testing uploads:
- `tomato_early_blight.jpg`
- `tomato_late_blight.jpg`
- `potato_late_blight.jpg`
- `apple_scab.jpg`
- `corn_rust.jpg`

## Tech stack

- **Backend:** Python / Flask
- **Database:** SQLite via SQLAlchemy
- **Image processing:** Pillow (resize to 224x224)
- **Frontend:** Plain HTML, CSS, JavaScript (no framework)
- **Auth:** Flask-Login with Werkzeug password hashing

## SRS requirements coverage

| Requirement | Status | Implementation |
|-------------|--------|----------------|
| FR-01 Registration | Done | `backend/routes/auth.py` |
| FR-02 Login | Done | `backend/routes/auth.py` |
| FR-03 Image upload | Done | `backend/services/image_service.py` |
| FR-04 Preprocessing | Done | Resize to 224x224 via Pillow |
| FR-05 Prediction | Done | `backend/services/prediction_service.py` |
| FR-06 Treatment info | Done | `backend/seed.py` + result page |
| FR-07 Diagnosis history | Done | `backend/routes/diagnosis.py` |
| FR-08 Admin management | Done | `backend/routes/admin.py` |

## What's next

- Plug in the real CNN model trained on the PlantVillage dataset
- Move from SQLite to PostgreSQL for production
- Deploy to a cloud platform
- Add more plant diseases over time
