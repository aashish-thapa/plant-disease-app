from backend.extensions import db


class Disease(db.Model):
    __tablename__ = "diseases"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), unique=True, nullable=False)
    plant = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    treatment = db.Column(db.Text)
    prevention = db.Column(db.Text)
    chemical_treatment = db.Column(db.Text)
