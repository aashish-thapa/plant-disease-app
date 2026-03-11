import os
import uuid

from PIL import Image
from werkzeug.utils import secure_filename


class ImageService:
    """Handles image upload validation and preprocessing (FR-03, FR-04)."""

    ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}
    TARGET_SIZE = (224, 224)

    def __init__(self, upload_folder):
        self.upload_folder = upload_folder
        os.makedirs(self.upload_folder, exist_ok=True)

    def is_allowed(self, filename):
        return (
            "." in filename
            and filename.rsplit(".", 1)[1].lower() in self.ALLOWED_EXTENSIONS
        )

    def save_and_preprocess(self, file):
        """Save uploaded file and resize to 224x224. Returns the filename."""
        ext = file.filename.rsplit(".", 1)[1].lower()
        filename = f"{uuid.uuid4().hex}.{ext}"
        filepath = os.path.join(self.upload_folder, filename)

        file.save(filepath)
        self._preprocess(filepath)

        return filename

    def _preprocess(self, filepath):
        """FR-04: Resize to 224x224 and save."""
        img = Image.open(filepath).convert("RGB")
        img = img.resize(self.TARGET_SIZE, Image.LANCZOS)
        img.save(filepath)
