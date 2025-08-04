import insightface
import numpy as np
import cv2
from app.shared.paths import get_user_dirs
from ..shared.config import (
    MODEL_NAME, 
    MODEL_PROVIDERS, 
    FACE_MATCH_THRESHOLD
)

from ..shared.utils import (
    cosine_similarity,
)

# Global model instance
model = insightface.app.FaceAnalysis(name=MODEL_NAME, providers=MODEL_PROVIDERS)
model.prepare(ctx_id=0)

def detect_faces(image: np.ndarray) -> list[dict]:
    """Returns list of (embedding, bbox, landmarks) for all detected faces."""
    faces = model.get(image)
    results = []
    for face in faces:
        results.append({
            "embedding": face.embedding,                    # np.ndarray (512,)
            "bbox": face.bbox.tolist(),                     # [x1, y1, x2, y2]
            "landmarks": face.landmark_2d_106.tolist(),     # [[x, y], ..., [x, y]]
        })
    return results

def match_face(
    embedding: np.ndarray,
    known_encodings: dict[str, np.ndarray],
    threshold: float = FACE_MATCH_THRESHOLD,
    return_score: bool = False
) -> tuple[bool, str, float | None]:
    """Matches the given embedding against known encodings."""

    best_score = -1
    best_match = None

    for name, known_embedding in known_encodings.items():
        score = cosine_similarity(embedding, known_embedding)
        if score > best_score:
            best_score = score
            best_match = name

    if best_score > (1 - threshold):
        return True, best_match, best_score if return_score else None
    return False, None, best_score if return_score else None

def crop_face(image: np.ndarray, bbox: list[int], margin: int = 10) -> np.ndarray:
    x1, y1, x2, y2 = map(int, bbox)
    h, w = image.shape[:2]
    x1 = max(x1 - margin, 0)
    y1 = max(y1 - margin, 0)
    x2 = min(x2 + margin, w)
    y2 = min(y2 + margin, h)
    return image[y1:y2, x1:x2]


def save_new_face(name: str, image: np.ndarray, embedding: np.ndarray, user_id: str) -> bool:
    """Saves the embedding and image of a known person."""
    try:
        ENCODING_DIR, FACES_DIR = get_user_dirs(user_id)
        np.save(ENCODING_DIR / f"{name}.npy", embedding)
        cv2.imwrite(str(FACES_DIR / f"{name}.jpg"), image)
        return True
    except Exception as e:
        print(f"Error saving new face: {e}")
        return False

def delete_known_face(name: str, user_id: str) -> bool:
    """Deletes face image and encoding for a known person."""
    ENCODING_DIR, FACES_DIR = get_user_dirs(user_id)
    try:
        (ENCODING_DIR / f"{name}.npy").unlink(missing_ok=True)
        (FACES_DIR / f"{name}.jpg").unlink(missing_ok=True)
        return True
    except Exception as e:
        print(f"Failed to delete face: {e}")
        return False

