from datetime import datetime

from backend.extensions import db


class Diagnosis(db.Model):
    __tablename__ = "diagnoses"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    disease_id = db.Column(db.Integer, db.ForeignKey("diseases.id"), nullable=True)
    image_filename = db.Column(db.String(256), nullable=False)
    predicted_disease = db.Column(db.String(200), nullable=False)
    confidence = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    disease = db.relationship("Disease", backref="diagnoses")
