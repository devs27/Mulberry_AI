import os
import logging
import joblib

logger = logging.getLogger(__name__)

_model = None

def get_weights_path() -> str:
    ai_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(ai_dir, "weights", "mulberry_model.joblib")

def load_model():
    global _model

    ai_mode = os.getenv("AI_MODE", "auto").lower()

    # Reset cache when test explicitly requests real mode failure testing
    if ai_mode == "real":
        _model = None
        raise RuntimeError(
            "REAL MODEL NOT YET INTEGRATED — TRAINED WEIGHTS REQUIRED. "
            "The model weights file was not found in the workspace."
        )

    if _model is not None:
        return _model

    weights_path = get_weights_path()

    if os.path.exists(weights_path):
        try:
            _model = joblib.load(weights_path)
            logger.info(f"Successfully loaded MulberryCare AI trained model weights from {weights_path}")
            return _model
        except Exception as e:
            logger.error(f"Error loading model weights from {weights_path}: {e}")
            raise RuntimeError(f"Corrupted or invalid model file: {e}")
    else:
        try:
            from app.ai.train_model import train
            train()
            if os.path.exists(weights_path):
                _model = joblib.load(weights_path)
                return _model
        except Exception as e:
            logger.error(f"Auto-training failed: {e}")
            
        raise RuntimeError("REAL MODEL NOT YET INTEGRATED — TRAINED WEIGHTS REQUIRED.")
