import os
import random

# Get the confidence threshold from the environment (default: 0.70)
CONFIDENCE_THRESHOLD = float(os.getenv("DISEASE_MODEL_CONFIDENCE_THRESHOLD", "0.70"))

DISEASE_CLASSES = [
    {"disease": "Leaf Rust", "confidence_range": (0.75, 0.98)},
    {"disease": "Healthy", "confidence_range": (0.80, 0.99)},
    {"disease": "Leaf Spot", "confidence_range": (0.72, 0.95)},
    # Simulated uncertain prediction to test the confidence safety guardrail
    {"disease": "Unidentified / Low Confidence Spot", "confidence_range": (0.45, 0.65)}
]


def predict(image_path: str) -> dict:
    """
    Mock predictor function to be replaced by the teammate's real model.
    Preserves signature: predict(image_path) -> {"disease": str, "confidence": float}
    """
    # Pick a random classification case
    result_class = random.choice(DISEASE_CLASSES)
    min_conf, max_conf = result_class["confidence_range"]
    confidence = round(random.uniform(min_conf, max_conf), 2)

    return {
        "disease": result_class["disease"],
        "confidence": confidence
    }
