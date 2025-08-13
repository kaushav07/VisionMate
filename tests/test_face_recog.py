# tests/services/test_face_utils.py
import pytest
import numpy as np
import pathlib
import cv2
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
from face_utils import (
    detect_faces,
    face_recog,
)

APP_PATH=pathlib.Path(__file__).parent.parent

def test_detect_faces():
    # Test the detect_faces function
    name="Paul"
    image_path = APP_PATH / f"dummy_user_data/pictures/{name}.jpeg"
    image = cv2.imread(str(image_path))
    faces = detect_faces(image)
    assert len(faces) > 0 
    assert 'embedding' in faces[0]
    assert 'bbox' in faces[0]
    assert 'landmarks' in faces[0]

def test_face_recog():
    # Test the face_recog function
    name = "Paul"
    image_path = APP_PATH / f"dummy_user_data/pictures/{name}.jpeg"
    image = cv2.imread(str(image_path))
    faces = detect_faces(image)
    assert len(faces) > 0
    face_embedding = faces[0]['embedding']
    
    # Assuming we have a known face embedding for comparison
    known_encodings = {
        "Paul": face_embedding  # Using the same face to guarantee a match
    }
    match_result = face_recog(face_embedding, known_encodings)
    assert match_result[0] is True
    assert match_result[1] == "Paul"
    assert match_result[2] is None

