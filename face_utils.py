import insightface
import numpy as np, math
import cv2
from load_model import load_face_model

# Global model instance
model = load_face_model()
FACE_MATCH_THRESHOLD = 0.6

def cosine_similarity(vec_a: list[float], vec_b: list[float]) -> float:
    """
    Calculate cosine similarity between two vectors.

    Args:
        vec_a: First vector as a list of numbers.
        vec_b: Second vector as a list of numbers.

    Returns:
        Cosine similarity value between -1 and 1.
    """
    # Check length
    if len(vec_a) != len(vec_b):
        raise ValueError("Vectors must be of the same length.")

    # Dot product
    dot_product = sum(a * b for a, b in zip(vec_a, vec_b))
    
    # Norms (magnitudes)
    norm_a = math.sqrt(sum(a * a for a in vec_a))
    norm_b = math.sqrt(sum(b * b for b in vec_b))

    if norm_a == 0 or norm_b == 0:
        raise ValueError("Vectors must not be zero-length.")

    return dot_product / (norm_a * norm_b)

def detect_faces(image: np.ndarray) -> list[dict]:
    """Returns list of (embedding, bbox, landmarks) for all detected faces."""
    faces = model.get(image)
    results = []
    for face in faces:
        results.append({
            "embedding": face.embedding,                    
            "bbox": face.bbox.tolist(),                     
            "landmarks": face.landmark_2d_106.tolist(),     
        })
    return results

def face_recog(
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
