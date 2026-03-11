from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user

from backend.extensions import db
from backend.models import Disease

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")


@admin_bp.before_request
@login_required
def require_admin():
    if not current_user.is_admin:
        flash("Admin access required.", "error")
        return redirect(url_for("diagnosis.dashboard"))


@admin_bp.route("/diseases")
def diseases():
    all_diseases = Disease.query.order_by(Disease.plant, Disease.name).all()
    return render_template("admin/diseases.html", diseases=all_diseases)


@admin_bp.route("/diseases/add", methods=["GET", "POST"])
def add_disease():
    if request.method == "POST":
        disease = Disease(
            name=request.form["name"],
            plant=request.form["plant"],
            description=request.form.get("description", ""),
            treatment=request.form.get("treatment", ""),
            prevention=request.form.get("prevention", ""),
            chemical_treatment=request.form.get("chemical_treatment", ""),
        )
        db.session.add(disease)
        db.session.commit()
        flash("Disease added.", "success")
        return redirect(url_for("admin.diseases"))

    return render_template("admin/disease_form.html", disease=None)


@admin_bp.route("/diseases/edit/<int:disease_id>", methods=["GET", "POST"])
def edit_disease(disease_id):
    disease = Disease.query.get_or_404(disease_id)

    if request.method == "POST":
        disease.name = request.form["name"]
        disease.plant = request.form["plant"]
        disease.description = request.form.get("description", "")
        disease.treatment = request.form.get("treatment", "")
        disease.prevention = request.form.get("prevention", "")
        disease.chemical_treatment = request.form.get("chemical_treatment", "")
        db.session.commit()
        flash("Disease updated.", "success")
        return redirect(url_for("admin.diseases"))

    return render_template("admin/disease_form.html", disease=disease)


@admin_bp.route("/diseases/delete/<int:disease_id>", methods=["POST"])
def delete_disease(disease_id):
    disease = Disease.query.get_or_404(disease_id)
    db.session.delete(disease)
    db.session.commit()
    flash("Disease deleted.", "success")
    return redirect(url_for("admin.diseases"))
