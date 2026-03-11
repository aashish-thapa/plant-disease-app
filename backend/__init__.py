import os

from flask import Flask

from backend.config import Config
from backend.extensions import db, login_manager
from backend.models import User
from backend.routes import auth_bp, diagnosis_bp, admin_bp
from backend.seed import seed_database


def create_app():
    app = Flask(
        __name__,
        template_folder=os.path.join(os.path.dirname(__file__), "..", "frontend", "templates"),
        static_folder=os.path.join(os.path.dirname(__file__), "..", "frontend", "static"),
    )
    app.config.from_object(Config)

    db.init_app(app)
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return db.session.get(User, int(user_id))

    app.register_blueprint(auth_bp)
    app.register_blueprint(diagnosis_bp)
    app.register_blueprint(admin_bp)

    with app.app_context():
        os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)
        os.makedirs(os.path.join(os.path.dirname(__file__), "..", "database"), exist_ok=True)
        db.create_all()
        seed_database()

    return app
