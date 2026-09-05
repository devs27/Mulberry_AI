import os
import uuid
from datetime import datetime
from typing import List, Optional
from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException
from sqlalchemy.orm import Session

from app.database.db import get_db
from app.models.user import User
from app.models.diagnosis import Diagnosis
from app.schemas.diagnosis import DiagnosisOut
from app.api.deps import get_current_user
from app.ai import predict

router = APIRouter(prefix="/api/diagnose", tags=["diagnose"])

# Disease advisories from verified agricultural Sericulture recommendations
ADVISORIES = {
    "Leaf Rust": {
        "en": "Apply Carbendazim (0.1%) or Mancozeb (0.2%) spray. Maintain proper pruning and spacing.",
        "ta": "கார்பென்டாசிம் (0.1%) அல்லது மான்கோசெப் (0.2%) தெளிக்கவும். சரியான கத்தரித்து இடைவெளியை பராமரிக்கவும்."
    },
    "Leaf Spot": {
        "en": "Spray Carbendazim (0.1%) or Mancozeb (0.2%) at 12-15 days interval. Collect and burn infected fallen leaves.",
        "ta": "12-15 நாட்கள் இடைவெளியில் கார்பென்டாசிம் (0.1%) அல்லது மான்கோசெப் (0.2%) தெளிக்கவும். பாதிக்கப்பட்ட இலைகளை சேகரித்து எரிக்கவும்."
    },
    "Healthy": {
        "en": "No disease detected. Continue normal cultivation practices: regular irrigation, fertilization, and weeding.",
        "ta": "நோய் எதுவும் கண்டறியப்படவில்லை. சாதாரண சாகுபடி முறைகளைத் தொடரவும்: வழக்கமான நீர்ப்பாசனம், உரமிடுதல் மற்றும் களை எடுத்தல்."
    }
}

UNCERTAIN_ADVISORY = {
    "en": "The result is uncertain. Please capture another clear image or consult an agricultural expert.",
    "ta": "முடிவு நிச்சயமற்றது. மற்றொரு தெளிவான படத்தை எடுக்கவும் அல்லது விவசாய நிபுணரை அணுகவும்."
}


@router.get("/history", response_model=List[DiagnosisOut])
def get_diagnosis_history(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Return only the authenticated farmer's diagnoses, ordered newest first
    diagnoses = (
        db.query(Diagnosis)
        .filter(Diagnosis.user_id == current_user.id)
        .order_by(Diagnosis.timestamp.desc())
        .all()
    )
    return diagnoses


@router.post("/upload")
async def upload_and_diagnose(
    file: UploadFile = File(...),
    variety: str = Form(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # 1. Validate file exists
    if not file or not file.filename:
        raise HTTPException(status_code=400, detail="No file was uploaded.")

    # 2. Allow any image file extension (JPG, PNG, WEBP, BMP, TIFF, GIF, HEIC, AVIF, PPM, etc.)
    allowed_exts = {
        ".jpg", ".jpeg", ".png", ".webp", ".bmp", ".tif", ".tiff",
        ".gif", ".heic", ".heif", ".avif", ".ppm", ".pbm", ".pgm",
        ".pnm", ".tga", ".ico", ".dng"
    }
    file_extension = os.path.splitext(file.filename)[1].lower()
    if file_extension and file_extension not in allowed_exts:
        # If extension isn't in common list, still let Pillow try to open it if content-type is image
        if not (file.content_type and file.content_type.startswith("image/")):
            raise HTTPException(status_code=400, detail="Unsupported image format. Please upload a valid image file.")

    # 3. Limit file size (Up to 100MB to support high-res DSLR/smartphone camera photos)
    MAX_FILE_SIZE = 100 * 1024 * 1024
    try:
        content = await file.read()
    except Exception:
        raise HTTPException(status_code=400, detail="Could not read uploaded file.")

    if len(content) > MAX_FILE_SIZE:
        raise HTTPException(status_code=400, detail="File size exceeds the 100MB limit.")

    if len(content) == 0:
        raise HTTPException(status_code=400, detail="Uploaded file is empty.")

    # 4. Verify actual image content using Pillow with MAX_IMAGE_PIXELS disabled (supports any resolution & size)
    from PIL import Image, ImageOps
    import io

    # Disable decompression bomb limit to support huge high-megapixel images
    Image.MAX_IMAGE_PIXELS = None

    try:
        img = Image.open(io.BytesIO(content))
        # Handle orientation if present in EXIF (e.g. smartphone camera orientation)
        try:
            img = ImageOps.exif_transpose(img)
        except Exception:
            pass

        # Convert image to RGB mode if RGBA, CMYK, P, 1, L, LA
        if img.mode != "RGB":
            img = img.convert("RGB")

    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail="Invalid or unsupported image file. Please upload a valid leaf image format."
        )

    # 5. Save image as clean JPEG/PNG for guaranteed browser display & static serving
    pil_format = (img.format or "JPEG").lower()
    if pil_format in ["png", "webp"]:
        out_ext = f".{pil_format}"
        save_format = pil_format.upper()
    else:
        out_ext = ".jpg"
        save_format = "JPEG"

    api_dir = os.path.dirname(os.path.abspath(__file__))
    backend_dir = os.path.dirname(os.path.dirname(api_dir))
    static_upload_dir = os.path.join(backend_dir, "static", "uploads")
    os.makedirs(static_upload_dir, exist_ok=True)

    unique_filename = f"{uuid.uuid4()}{out_ext}"
    save_path = os.path.join(static_upload_dir, unique_filename)

    try:
        # If image is very huge (> 4096px), optimize size for storage while preserving high detail
        max_dim = 4096
        if img.width > max_dim or img.height > max_dim:
            img.thumbnail((max_dim, max_dim), Image.Resampling.LANCZOS)
        img.save(save_path, format=save_format, quality=92, optimize=True)
    except Exception:
        raise HTTPException(status_code=500, detail="Could not save uploaded file.")

    # URL path for static serving
    image_url_path = f"/static/uploads/{unique_filename}"

    # 7. Call AI predictor with robust error handling
    try:
        prediction = predict(save_path)
    except Exception as e:
        import logging
        logging.getLogger(__name__).error(f"Inference failure: {e}", exc_info=True)
        if os.path.exists(save_path):
            os.remove(save_path)
        raise HTTPException(
            status_code=500,
            detail="AI diagnosis is temporarily unavailable. Please try again later."
        )

    disease = prediction["disease"]
    confidence = prediction["confidence"]

    # 8. Check confidence guardrail threshold
    threshold = float(os.getenv("DISEASE_MODEL_CONFIDENCE_THRESHOLD", "0.70"))
    is_uncertain = confidence < threshold

    # 9. Extract severity (Moderate for diseased + certain)
    severity: Optional[str] = None
    if not is_uncertain and disease != "Healthy":
        severity = "moderate"

    # 10. Save diagnosis record to database
    diagnosis_record = Diagnosis(
        user_id=current_user.id,
        disease=disease if not is_uncertain else "Uncertain / " + disease,
        confidence=confidence,
        variety=variety,
        timestamp=datetime.utcnow(),
        severity=severity,
        is_uncertain=is_uncertain,
        image_path=image_url_path
    )
    db.add(diagnosis_record)
    db.commit()
    db.refresh(diagnosis_record)

    # 11. Retrieve advisory strictly from database table disease_information
    from app.models.disease_info import DiseaseInformation
    if is_uncertain:
        advisory = {
            "en": UNCERTAIN_ADVISORY["en"],
            "ta": UNCERTAIN_ADVISORY["ta"],
            "disclaimer_en": "This diagnosis is AI-assisted advice. Verify physically before treatment.",
            "disclaimer_ta": "இந்த நோய் கண்டறிதல் AI-உதவியுடன் வழங்கப்பட்டவை. பயன்படுத்தும் முன் சரிபார்க்கவும்."
        }
    else:
        disease_info = db.query(DiseaseInformation).filter(DiseaseInformation.name == disease).first()
        if disease_info:
            advisory = {
                "en": disease_info.management_en,
                "ta": disease_info.management_ta,
                "disclaimer_en": disease_info.disclaimer_en,
                "disclaimer_ta": disease_info.disclaimer_ta
            }
        else:
            if disease == "Healthy":
                advisory = {
                    "en": "No disease detected. Continue normal cultivation practices: regular irrigation, fertilization, and weeding.",
                    "ta": "பயிர் ஆரோக்கியமாக உள்ளது. சாதாரண சாகுபடி முறைகளைத் தொடரவும்: வழக்கமான நீர்ப்பாசனம், உரமிடுதல் மற்றும் களை எடுத்தல்.",
                    "disclaimer_en": "This is a general advisory. Monitor your fields regularly.",
                    "disclaimer_ta": "இது ஒரு பொதுவான ஆலோசனை. உங்கள் பயிர்களை தவறாமல் கண்காணிக்கவும்."
                }
            else:
                advisory = {
                    "en": "Consult agricultural extension officer for disease details.",
                    "ta": "வகைப்படுத்தப்படாத நோய்க்கு வேளாண் விரிவாக்க அலுவலரை அணுகவும்.",
                    "disclaimer_en": "This diagnosis is AI-assisted advice. Verify physically before treatment.",
                    "disclaimer_ta": "இந்த நோய் கண்டறிதல் AI-உதவியுடன் வழங்கப்பட்டவை. பயன்படுத்தும் முன் சரிபார்க்கவும்."
                }

    return {
        "id": diagnosis_record.id,
        "disease": diagnosis_record.disease,
        "confidence": confidence,
        "variety": variety,
        "timestamp": diagnosis_record.timestamp,
        "severity": severity,
        "is_uncertain": is_uncertain,
        "image_path": image_url_path,
        "advisory": advisory
    }
