import os
import sys
import glob
import logging
from concurrent.futures import ThreadPoolExecutor
import numpy as np

backend_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

from app.ai.feature_extractor import extract_features_from_path

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

def process_single_image(args):
    img_path, label = args
    try:
        feats = extract_features_from_path(img_path)
        return feats, label
    except Exception as e:
        logger.warning(f"Error reading image {img_path}: {e}")
        return None

def train():
    import joblib
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.preprocessing import StandardScaler
    from sklearn.pipeline import Pipeline
    from sklearn.model_selection import train_test_split
    from sklearn.metrics import classification_report, accuracy_score

    project_root = os.path.dirname(backend_dir)
    dataset_dir = os.path.join(project_root, "Mulberry leaf dataset", "Mulberry Data")

    class_mapping = {
        "Disease Free leaves": "Healthy",
        "Leaf Rust": "Leaf Rust",
        "Leaf spot": "Leaf Spot"
    }

    if not os.path.exists(dataset_dir):
        logger.error(f"Dataset directory not found at: {dataset_dir}")
        return

    logger.info(f"Loading dataset from: {dataset_dir}")

    tasks = []
    for folder_name, target_class in class_mapping.items():
        folder_path = os.path.join(dataset_dir, folder_name)
        if not os.path.exists(folder_path):
            logger.warning(f"Class folder not found: {folder_path}")
            continue

        image_paths = []
        for ext in ("*.jpg", "*.jpeg", "*.png", "*.JPG", "*.JPEG", "*.PNG"):
            image_paths.extend(glob.glob(os.path.join(folder_path, ext)))

        # Subsample up to 150 images per class for lightning fast high-accuracy training
        if len(image_paths) > 150:
            image_paths = image_paths[:150]

        logger.info(f"Using {len(image_paths)} images for class '{target_class}' ({folder_name})")
        for p in image_paths:
            tasks.append((p, target_class))

    logger.info(f"Extracting features for {len(tasks)} dataset images in parallel...")

    X = []
    y = []

    with ThreadPoolExecutor(max_workers=8) as executor:
        results = executor.map(process_single_image, tasks)
        for res in results:
            if res is not None:
                feats, label = res
                X.append(feats)
                y.append(label)

    X = np.array(X)
    y = np.array(y)

    logger.info(f"Dataset extraction complete. Total samples: {len(X)}, Feature dimension: {X.shape[1]}")

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    pipeline = Pipeline([
        ("scaler", StandardScaler()),
        ("classifier", RandomForestClassifier(n_estimators=100, max_depth=12, random_state=42))
    ])

    logger.info("Training Random Forest model on Mulberry dataset...")
    pipeline.fit(X_train, y_train)

    y_pred = pipeline.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    logger.info(f"Model Training Accuracy on Test Set: {acc * 100:.2f}%")
    logger.info("\n" + classification_report(y_test, y_pred))

    weights_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "weights")
    os.makedirs(weights_dir, exist_ok=True)
    model_save_path = os.path.join(weights_dir, "mulberry_model.joblib")

    joblib.dump(pipeline, model_save_path)
    logger.info(f"Successfully saved MulberryCare AI trained model weights to: {model_save_path}")

if __name__ == "__main__":
    train()
