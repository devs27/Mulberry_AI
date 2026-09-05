from PIL import Image

def preprocess_image(image_path: str, target_size=(224, 224)) -> Image.Image:
    """
    Preprocess image for CNN models (ResNet, MobileNet, etc.):
    - Convert channels to RGB to strip alpha transparency.
    - Resize to expected input dimensions (default 224x224).
    """
    img = Image.open(image_path)
    if img.mode != "RGB":
        img = img.convert("RGB")
    img = img.resize(target_size)
    return img
