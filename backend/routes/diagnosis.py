import os
from datetime import datetime

from flask import (
    Blueprint, render_template, request, redirect,
    url_for, flash, current_app, send_from_directory,
)
from flask_login import login_required, current_user

from backend.extensions import db
from backend.models import Diagnosis as DiagnosisModel
from backend.services.image_service import ImageService
from backend.services.prediction_service import PredictionService

diagnosis_bp = Blueprint("diagnosis", __name__)


def _get_image_service():
    return ImageService(current_app.config["UPLOAD_FOLDER"])


def _get_prediction_service():
    return PredictionService()


@diagnosis_bp.route("/")
def index():
    return render_template("index.html")


@diagnosis_bp.route("/dashboard")
@login_required
def dashboard():
    recent = (
        DiagnosisModel.query
        .filter_by(user_id=current_user.id)
        .order_by(DiagnosisModel.created_at.desc())
        .limit(5)
        .all()
    )
    total = DiagnosisModel.query.filter_by(user_id=current_user.id).count()
    return render_template("diagnosis/dashboard.html", recent=recent, total=total)


@diagnosis_bp.route("/upload", methods=["GET", "POST"])
@login_required
def upload():
    if request.method == "POST":
        if "image" not in request.files:
            flash("No image provided.", "error")
            return redirect(url_for("diagnosis.upload"))

        file = request.files["image"]
        if file.filename == "":
            flash("No file selected.", "error")
            return redirect(url_for("diagnosis.upload"))

        image_service = _get_image_service()
        if not image_service.is_allowed(file.filename):
            flash("Only JPEG and PNG files are accepted.", "error")
            return redirect(url_for("diagnosis.upload"))

        original_name = file.filename
        filename = image_service.save_and_preprocess(file)

        prediction_service = _get_prediction_service()
        image_path = os.path.join(current_app.config["UPLOAD_FOLDER"], filename)
        disease_name, confidence, disease_id = prediction_service.predict(
            image_path, original_filename=original_name
        )

        record = DiagnosisModel(
            user_id=current_user.id,
            disease_id=disease_id,
            image_filename=filename,
            predicted_disease=disease_name,
            confidence=confidence,
        )
        db.session.add(record)
        db.session.commit()

        return redirect(url_for("diagnosis.result", diagnosis_id=record.id))

    return render_template("diagnosis/upload.html")


@diagnosis_bp.route("/result/<int:diagnosis_id>")
@login_required
def result(diagnosis_id):
    record = DiagnosisModel.query.get_or_404(diagnosis_id)
    if record.user_id != current_user.id and not current_user.is_admin:
        flash("Access denied.", "error")
        return redirect(url_for("diagnosis.dashboard"))

    prediction_service = _get_prediction_service()
    low_confidence = prediction_service.is_low_confidence(record.confidence)

    return render_template(
        "diagnosis/result.html", record=record, low_confidence=low_confidence
    )


@diagnosis_bp.route("/history")
@login_required
def history():
    disease_filter = request.args.get("disease", "")
    date_from = request.args.get("date_from", "")
    date_to = request.args.get("date_to", "")

    query = DiagnosisModel.query.filter_by(user_id=current_user.id)

    if disease_filter:
        query = query.filter(
            DiagnosisModel.predicted_disease.ilike(f"%{disease_filter}%")
        )
    if date_from:
        query = query.filter(
            DiagnosisModel.created_at >= datetime.strptime(date_from, "%Y-%m-%d")
        )
    if date_to:
        query = query.filter(
            DiagnosisModel.created_at
            <= datetime.strptime(date_to + " 23:59:59", "%Y-%m-%d %H:%M:%S")
        )

    records = query.order_by(DiagnosisModel.created_at.desc()).all()

    disease_names = [
        row[0]
        for row in db.session.query(DiagnosisModel.predicted_disease)
        .filter_by(user_id=current_user.id)
        .distinct()
        .all()
    ]

    return render_template(
        "diagnosis/history.html",
        records=records,
        disease_names=disease_names,
        disease_filter=disease_filter,
        date_from=date_from,
        date_to=date_to,
    )


@diagnosis_bp.route("/uploads/<filename>")
@login_required
def uploaded_file(filename):
    return send_from_directory(current_app.config["UPLOAD_FOLDER"], filename)
