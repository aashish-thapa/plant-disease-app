import os
import json
import numpy as np
from PIL import Image

from backend.models import Disease

_model = None
_class_names = None

_MODEL_DIR = os.path.join(os.path.dirname(__file__), "..", "ml_model")


def _load_model():
    global _model, _class_names
    if _model is not None:
        return

    import torch
    from torchvision import models
    import torch.nn as nn

    with open(os.path.join(_MODEL_DIR, "class_names.json")) as f:
        _class_names = json.load(f)

    # same architecture as what we trained in colab
    _model = models.mobilenet_v2(weights=None)
    _model.classifier = nn.Sequential(
        nn.Dropout(0.3),
        nn.Linear(_model.last_channel, len(_class_names))
    )

    weights = os.path.join(_MODEL_DIR, "plant_disease_model.pth")
    _model.load_state_dict(torch.load(weights, map_location="cpu", weights_only=True))
    _model.eval()
    print(f"Loaded model with {len(_class_names)} classes")


def _preprocess(image_path):
    """Same transforms we used for validation in colab."""
    import torch

    img = Image.open(image_path).convert("RGB")
    img = img.resize((256, 256))
    # center crop 224
    left = (256 - 224) // 2
    top = (256 - 224) // 2
    img = img.crop((left, top, left + 224, top + 224))

    arr = np.array(img, dtype=np.float32) / 255.0
    mean = np.array([0.485, 0.456, 0.406])
    std = np.array([0.229, 0.224, 0.225])
    arr = (arr - mean) / std

    tensor = torch.tensor(arr).permute(2, 0, 1).unsqueeze(0).float()
    return tensor


# plantvillage folder names -> our db names
_NAME_MAP = {
    "Tomato___Early_blight": "Tomato - Early Blight",
    "Tomato___Late_blight": "Tomato - Late Blight",
    "Tomato___Leaf_Mold": "Tomato - Leaf Mold",
    "Tomato___Bacterial_spot": "Tomato - Bacterial Spot",
    "Tomato___Septoria_leaf_spot": "Tomato - Septoria Leaf Spot",
    "Tomato___Spider_mites Two-spotted_spider_mite": "Tomato - Spider Mites",
    "Tomato___Target_Spot": "Tomato - Target Spot",
    "Tomato___Tomato_Yellow_Leaf_Curl_Virus": "Tomato - Yellow Leaf Curl Virus",
    "Tomato___Tomato_mosaic_virus": "Tomato - Mosaic Virus",
    "Potato___Early_blight": "Potato - Early Blight",
    "Potato___Late_blight": "Potato - Late Blight",
    "Apple___Apple_scab": "Apple - Apple Scab",
    "Apple___Black_rot": "Apple - Black Rot",
    "Apple___Cedar_apple_rust": "Apple - Cedar Apple Rust",
    "Corn_(maize)___Common_rust_": "Corn - Common Rust",
    "Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot": "Corn - Cercospora Leaf Spot",
    "Corn_(maize)___Northern_Leaf_Blight": "Corn - Northern Leaf Blight",
    "Grape___Black_rot": "Grape - Black Rot",
    "Grape___Esca_(Black_Measles)": "Grape - Esca Black Measles",
    "Grape___Leaf_blight_(Isariopsis_Leaf_Spot)": "Grape - Leaf Blight",
    "Orange___Haunglongbing_(Citrus_greening)": "Orange - Huanglongbing",
    "Peach___Bacterial_spot": "Peach - Bacterial Spot",
    "Pepper,_bell___Bacterial_spot": "Pepper Bell - Bacterial Spot",
    "Squash___Powdery_mildew": "Squash - Powdery Mildew",
    "Strawberry___Leaf_scorch": "Strawberry - Leaf Scorch",
    "Cherry_(including_sour)___Powdery_mildew": "Cherry - Powdery Mildew",
}


def _clean_label(raw):
    if "healthy" in raw.lower():
        return "Healthy Plant"
    if raw in _NAME_MAP:
        return _NAME_MAP[raw]
    # just strip out the weird underscores if its something we didnt map
    return " ".join(raw.replace("___", " - ").replace("_", " ").split())


class PredictionService:
    """Runs the trained CNN on uploaded leaf images (FR-05)."""

    CONFIDENCE_THRESHOLD = 0.70

    def predict(self, image_path, original_filename=""):
        import torch

        _load_model()

        tensor = _preprocess(image_path)
        with torch.no_grad():
            out = _model(tensor)

        probs = torch.nn.functional.softmax(out, dim=-1)[0]
        idx = probs.argmax().item()
        confidence = round(probs[idx].item(), 2)

        disease_name = _clean_label(_class_names[idx])

        disease = Disease.query.filter_by(name=disease_name).first()
        disease_id = disease.id if disease else None

        return disease_name, confidence, disease_id

    def is_low_confidence(self, confidence):
        return confidence < self.CONFIDENCE_THRESHOLD
