import os
import random
import time

from backend.models import Disease


class PredictionService:
    """
    FR-05: Disease prediction from leaf image.

    Currently simulates CNN output for prototyping.
    Replace `predict()` internals with a real TensorFlow/PyTorch
    model call when the trained model is ready.
    """

    CONFIDENCE_THRESHOLD = 0.70

    # Keyword-to-disease mapping used by the prototype to give
    # realistic predictions based on the original filename.
    # A real model would ignore filenames entirely.
    # Ordered most-specific first so "potato_late_blight" matches potato
    # before the generic "late_blight" rule.
    _KEYWORD_MAP = [
        ("potato_early",          "Potato - Early Blight"),
        ("potato_late",           "Potato - Late Blight"),
        ("potato",                "Potato - Late Blight"),
        ("tomato_early",          "Tomato - Early Blight"),
        ("tomato_late",           "Tomato - Late Blight"),
        ("tomato_leaf",           "Tomato - Leaf Mold"),
        ("early_blight",          "Tomato - Early Blight"),
        ("late_blight",           "Tomato - Late Blight"),
        ("leaf_mold",             "Tomato - Leaf Mold"),
        ("apple",                 "Apple - Apple Scab"),
        ("scab",                  "Apple - Apple Scab"),
        ("corn",                  "Corn - Common Rust"),
        ("rust",                  "Corn - Common Rust"),
        ("grape",                 "Grape - Black Rot"),
        ("healthy",               "Healthy Plant"),
    ]

    def predict(self, image_path, original_filename=""):
        """
        Run prediction on a preprocessed image.

        Returns:
            tuple: (disease_name, confidence, disease_id)
        """
        diseases = Disease.query.all()
        if not diseases:
            return "Unknown", 0.0, None

        # --- Prototype: simulate model inference time (~8s) ----------------
        time.sleep(8)

        disease_name = self._match_by_filename(original_filename or image_path)
        confidence = round(random.uniform(0.82, 0.97), 2)

        selected = None
        if disease_name:
            for d in diseases:
                if d.name == disease_name:
                    selected = d
                    break

        # Fallback: random disease if no keyword matched
        if not selected:
            selected = random.choice(diseases)
            disease_name = selected.name
            confidence = round(random.uniform(0.73, 0.92), 2)
        # ------------------------------------------------------------------

        return disease_name, confidence, selected.id

    def _match_by_filename(self, image_path):
        """Check if the upload's original name hints at a specific disease."""
        basename = os.path.basename(image_path).lower()
        for keyword, disease_name in self._KEYWORD_MAP:
            if keyword in basename:
                return disease_name
        return None

    def is_low_confidence(self, confidence):
        return confidence < self.CONFIDENCE_THRESHOLD
