import os

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-change-in-production")
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{os.path.join(BASE_DIR, 'database', 'plant_disease.db')}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")
    MAX_CONTENT_LENGTH = 10 * 1024 * 1024  # 10 MB
    ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}
