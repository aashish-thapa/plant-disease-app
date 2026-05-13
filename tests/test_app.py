import pytest
from backend import create_app
from backend.extensions import db
from backend.models import User
from backend.services.image_service import ImageService
from backend.services.prediction_service import PredictionService, _clean_label


@pytest.fixture
def app():
    app = create_app()
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    app.config["TESTING"] = True
    with app.app_context():
        db.drop_all()
        db.create_all()
        yield app


@pytest.fixture
def client(app):
    return app.test_client()


# testing if password check works with the right password
def test_correct_password(app):
    with app.app_context():
        u = User(name="John", email="john@email.com")
        u.set_password("mypassword")
        assert u.check_password("mypassword") == True


# testing if wrong password gets rejected
def test_wrong_password(app):
    with app.app_context():
        u = User(name="John", email="john@email.com")
        u.set_password("mypassword")
        assert u.check_password("wrongone") == False


# new users should not be admin
def test_default_not_admin(app):
    with app.app_context():
        u = User(name="John", email="john@email.com")
        u.set_password("mypassword")
        db.session.add(u)
        db.session.commit()
        assert u.is_admin == False


# jpg should be accepted
def test_jpg_allowed(app):
    svc = ImageService(app.config["UPLOAD_FOLDER"])
    assert svc.is_allowed("leaf.jpg") == True


# exe should be rejected
def test_exe_not_allowed(app):
    svc = ImageService(app.config["UPLOAD_FOLDER"])
    assert svc.is_allowed("bad.exe") == False


# check if the disease label gets cleaned up right
def test_disease_label_cleanup():
    assert _clean_label("Tomato___Early_blight") == "Tomato - Early Blight"


# low confidence should be flagged, high confidence should not
def test_confidence_check():
    svc = PredictionService()
    assert svc.is_low_confidence(0.5) == True
    assert svc.is_low_confidence(0.8) == False


# homepage should load fine
def test_homepage(client):
    resp = client.get("/")
    assert resp.status_code == 200


# register page should load fine
def test_register_page(client):
    resp = client.get("/register")
    assert resp.status_code == 200
