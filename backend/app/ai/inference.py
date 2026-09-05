import os
import logging
from PIL import Image
from app.ai.model_loader import load_model, get_weights_path
from app.ai.feature_extractor import extract_features
from app.ai.predictor import predict as mock_predict

logger = logging.getLogger(__name__)

def predict(image_path: str) -> dict:
    """
    Leaf disease diagnosis inference function.
    Reads image, extracts features, predicts class and confidence score.
    Returns: {"disease": str, "confidence": float}
    """
    ai_mode = os.getenv("AI_MODE", "auto").lower()

    if ai_mode == "mock":
        return mock_predict(image_path)

    # In test_real_model_failure, os.environ["AI_MODE"] == "real" and expects failure if model can't be loaded
    # If weights_path doesn't exist or is mocked out, load_model raises RuntimeError
    weights_path = get_weights_path()
    if ai_mode == "real" and not os.path.exists(weights_path):
        raise RuntimeError("REAL MODEL NOT YET INTEGRATED — TRAINED WEIGHTS REQUIRED.")

    try:
        model = load_model()
        if model is None:
            return mock_predict(image_path)

        with Image.open(image_path) as img:
            features = extract_features(img)
            
        features = features.reshape(1, -1)

        probabilities = model.predict_proba(features)[0]
        classes = model.classes_

        best_idx = int(probabilities.argmax())
        predicted_disease = str(classes[best_idx])
        confidence = float(probabilities[best_idx])

        return {
            "disease": predicted_disease,
            "confidence": round(confidence, 2)
        }

    except Exception as e:
        if ai_mode == "real":
            raise RuntimeError(f"Real model inference failure: {e}")
        logger.warning(f"Real model inference failed ({e}), falling back to mock predictor...")
        return mock_predict(image_path)
