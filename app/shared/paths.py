# app/shared/paths.py
"""
This module defines paths and utility functions for managing user directories in the VisionMate application.
"""

from pathlib import Path
from app.main import BASE_DIR

DATA_DIR = BASE_DIR / "data"
USERS_DIR = DATA_DIR / "users"


def get_user_dirs(user_id: str):
    user_dir = USERS_DIR / user_id
    encodings_dir = user_dir / "encodings"
    faces_dir = user_dir / "known_faces"
    encodings_dir.mkdir(parents=True, exist_ok=True)
    faces_dir.mkdir(parents=True, exist_ok=True)
    return encodings_dir, faces_dir
