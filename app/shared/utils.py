"""
This file contains utility functions for the VisionMate application. Common utility methods are defined here.
"""
import numpy as np
from app.shared.paths import get_user_dirs
from pathlib import Path

def clear_user_data(user_id: str) -> bool:
    """Deletes all known faces and encodings for a user."""
    try:
        ENCODING_DIR, FACES_DIR = get_user_dirs(user_id)
        for file in ENCODING_DIR.glob("*"):
            file.unlink()
        for file in FACES_DIR.glob("*"):
            file.unlink()
        return True
    except Exception as e:
        print(f"Error clearing user data: {e}")
        return False


def list_known_faces(user_id: str) -> list[str]:
    """Returns list of all known face names for a user."""
    ENCODING_DIR, _ = get_user_dirs(user_id)
    return [f.stem for f in ENCODING_DIR.glob("*.npy")]


def load_known_encodings(user_id: str) -> dict:
    """Returns dict of {name: embedding (np.ndarray)}."""
    known_encodings = {}
    encodings_dir, _ = get_user_dirs(user_id)
    for file in encodings_dir.glob("*.npy"):
        name = file.stem
        embedding = np.load(file)
        known_encodings[name] = embedding
    return known_encodings

def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

