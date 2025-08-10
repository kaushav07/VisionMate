from fastapi import APIRouter
import numpy as np
import tempfile
import os
import cv2
from app.shared.paths import (
    get_user_dirs,
)
from app.shared.utils import (
    load_known_encodings,
    clear_user_data,
    list_known_faces,
    cosine_similarity,
)
from app.services.face_utils import (
    delete_known_face,
    save_new_face,
    detect_faces,
    match_face,
    crop_face,
)

# Endpoint API Routes
router = APIRouter()
@router.post("/add_face/{user_id}")
async def add_face(user_id: str, file: bytes):
    ...

@router.post("/face_recognition/{user_id}")
async def face_recognition(user_id: str, file: bytes):
    """Recognizes faces in the uploaded image and returns matched names."""
    ...
