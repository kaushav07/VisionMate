import os
import zipfile
import requests
from pathlib import Path
from insightface.app import FaceAnalysis
from app.shared.paths import BASE_DIR

# Model config
FACE_MODEL_NAME = "buffalo_l"
FACE_MODEL_PROVIDERS = ["CPUExecutionProvider"]
FACE_MODEL_URL = f"https://github.com/deepinsight/insightface/releases/download/v0.7/{FACE_MODEL_NAME}.zip"
FACE_MODEL_DIR = BASE_DIR / "models" / FACE_MODEL_NAME
FACE_ZIP_PATH = FACE_MODEL_DIR.parent / f"{FACE_MODEL_NAME}.zip"
FACE_REQUIRED_FILES = [
    "1k3d68.onnx",
    "2d106det.onnx",
    "det_10g.onnx",
    "genderage.onnx",
    "w600k_r50.onnx"
]


def _ensure_model_exists(model_path, required_files, model_url, zip_path) -> Path:
    """Ensure the buffalo_l model is downloaded and extracted."""
    if model_path.exists() and all((model_path / f).exists() for f in required_files):
        return model_path

    model_path.mkdir(parents=True, exist_ok=True)

    print("Downloading buffalo_l model...")
    response = requests.get(model_url, stream=True)
    with open(zip_path, "wb") as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)

    print("Extracting model...")
    with zipfile.ZipFile(zip_path, "r") as zip_ref:
        zip_ref.extractall(model_path)

    zip_path.unlink()
    print("Model is ready.")
    return model_path


def load_face_model() -> FaceAnalysis:
    """Load the buffalo_l model using InsightFace."""
    model_dir = _ensure_model_exists(
        model_path=FACE_MODEL_DIR,
        required_files=FACE_REQUIRED_FILES,
        model_url=FACE_MODEL_URL,
        zip_path=FACE_ZIP_PATH
    )
    model = FaceAnalysis(name=str(model_dir), providers=FACE_MODEL_PROVIDERS)
    model.prepare(ctx_id=0)
    return model
