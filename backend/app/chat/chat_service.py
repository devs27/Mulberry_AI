from typing import Optional, List, Dict
from sqlalchemy.orm import Session

from app.models.user import User
from app.models.diagnosis import Diagnosis
from app.chat.safety import (
    normalize_query,
    detect_language,
    is_off_topic,
    is_ambiguous,
    get_ambiguous_reply,
    get_off_topic_reply,
    check_pesticide_safety
)
from app.chat.intent import detect_intent, INTENTS
from app.chat.retriever import retrieve_context
from app.chat.knowledge_base import KNOWLEDGE_SOURCE_LABEL_EN, KNOWLEDGE_SOURCE_LABEL_TA
from app.ai.chat_model import generate_response


def generate_today_checklist(
    lang: str,
    farmer_profile: Dict,
    recent_diagnosis: Optional[Dict] = None
) -> str:
    """
    Generates a practical, grounded daily farm checklist.
    Combines profile, recent diagnosis, and weather risk indicators.
    Clearly marks weather indicators as '(Demo / Simulated Weather)'.
    """
    name = farmer_profile.get("name", "Farmer")
    variety = farmer_profile.get("variety", "S36")
    village = farmer_profile.get("village", "Local Farm")

    has_rust = recent_diagnosis and "rust" in recent_diagnosis.get("disease", "").lower()
    has_spot = recent_diagnosis and "spot" in recent_diagnosis.get("disease", "").lower()

    if lang == "ta":
        checklist_lines = [
            f"🌱 இன்றைய பண்ணை சரிபார்ப்பு பட்டியல் (TODAY'S FARM CHECKLIST)",
            f"பண்ணையாளர்: {name} • மல்பெரி ரகம்: {variety} • பகுதி: {village}\n",
        ]

        if has_rust or has_spot:
            dis_name = "இலை துரு நோய்" if has_rust else "இலைப்புள்ளி நோய்"
            checklist_lines.extend([
                f"☐ இலை நலம்: உங்கள் முந்தைய பதிவில் கண்டறியப்பட்ட {dis_name} அறிகுறிகள் பரவாமல் தடுக்க அடிப்புற இலைகளை கண்காணிக்கவும்.",
                f"☐ நீர் பாசனம்: இலைகளில் நீர் தெளிப்பதைத் தவிர்த்து சொட்டு நீர் அல்லது வாய்க்கால் பாசனத்தைப் பயன்படுத்தவும்."
            ])
        else:
            checklist_lines.extend([
                f"☐ இலை நலம்: மல்பெரி இலைகளில் புள்ளிகள் அல்லது சுருக்கங்கள் உள்ளதா என காலை வேளையில் ஆய்வு செய்யவும்.",
                f"☐ நீர் பாசனம்: மண் ஈரப்பதத்தை சரிபார்த்து தேவைக்கேற்ப மட்டும் நீர் பாய்ச்சவும்; நீர் தேங்காமல் பார்த்துக் கொள்ளவும்."
            ])

        checklist_lines.extend([
            f"☐ வானிலை வழிகாட்டல்: மிதமான வெப்பநிலை & 65% ஈரப்பதம் (டெமோ / மாதிரி வானிலை தரவு).",
            f"☐ பூச்சி கண்காணிப்பு: இலைகளின் அடிப்பகுதியில் மாவுப்பூச்சி அல்லது இலைப்பேன் தென்படுகிறதா என கவனிக்கவும்.",
            f"☐ பட்டுப்புழு வளர்ப்பு: வளர்ப்பு மனை வெப்பநிலை (24-26°C) மற்றும் படுக்கை சுத்தத்தை உறுதிப்படுத்தவும்.",
            f"☐ அறுவடை: பட்டுப்புழுக்களுக்கு உணவளிக்க பனி உலர்ந்த பின் காலை வேளையில் இலைகளை அறுவடை செய்யவும்.\n",
            f"👨🌾 எப்போது நிபுணரை அணுக வேண்டும்:",
            f"இலைகளில் 20% மேல் திடீர் பாதிப்பு ஏற்பட்டால் 'Check a Leaf' மூலம் புகைப்படம் எடுத்து சோதிக்கவும் அல்லது விரிவாக்க அலுவலரை தொடர்பு கொள்ளவும்.\n",
            f"ஆதாரம்: {KNOWLEDGE_SOURCE_LABEL_TA}"
        ])
    else:
        checklist_lines = [
            f"🌱 TODAY'S FARM CHECKLIST",
            f"Farmer: {name} • Mulberry Variety: {variety} • Village: {village}\n",
        ]

        if has_rust or has_spot:
            dis_name = "Leaf Rust" if has_rust else "Leaf Spot"
            conf = recent_diagnosis.get("confidence", 85)
            checklist_lines.extend([
                f"☐ Crop Health: Inspect lower foliage for {dis_name} spread (Recent Diagnosis: {dis_name} at {conf}% confidence).",
                f"☐ Irrigation Care: Avoid overhead sprinkler irrigation to prevent splashing fungal spores; use drip or furrow irrigation."
            ])
        else:
            checklist_lines.extend([
                f"☐ Crop Health: Inspect mulberry foliage for early discoloration or pest curling in morning hours.",
                f"☐ Irrigation Care: Check soil moisture before watering; ensure proper drainage to prevent root rot."
            ])

        checklist_lines.extend([
            f"☐ Weather Advisory: Moderate disease risk based on climate profile (Demo / Simulated Weather).",
            f"☐ Pest Surveillance: Inspect tender shoots for mealybugs or thrips; clip affected tips early.",
            f"☐ Silkworm Hygiene: Check rearing room cross-ventilation (24–26°C, ~70% humidity) and bed cleanliness.",
            f"☐ Feed Quality: Harvest leaves early morning after dew has dried; feed only fresh, clean leaves.\n",
            f"👨🌾 WHEN TO SEEK EXPERT HELP:",
            f"If unusual defoliation or rapid disease proliferation exceeds 20% of your crop, take a photo via 'Check a Leaf' or consult your local sericulture extension officer.\n",
            f"Source: {KNOWLEDGE_SOURCE_LABEL_EN}"
        ])

    return "\n".join(checklist_lines)


def process_chat(
    message: str,
    lang_override: Optional[str],
    default_lang: str,
    db: Session,
    current_user: Optional[User] = None,
    diagnosis_id: Optional[str] = None,
    diagnosis_context: Optional[Dict] = None,
    session_history: Optional[List[Dict]] = None
) -> dict:
    """
    Orchestrates the upgraded, context-aware Ask MulberryCare decision support pipeline:
    1. Input Validation
    2. Language & Normalization
    3. Farmer Profile & Diagnosis Context Integration
    4. Deterministic Intent Detection
    5. Chemical Safety & Ambiguity & Off-Topic Guardrails
    6. Multi-Priority RAG Retrieval
    7. Grounded, Action-Oriented Response Generation
    """
    # 1. Input Validation
    if not message or not message.strip():
        return {
            "reply": "Please type a valid question.",
            "language": "en",
            "topic": "validation_error",
            "intent": INTENTS["AMBIGUOUS"],
            "source": KNOWLEDGE_SOURCE_LABEL_EN
        }

    if len(message) > 600:
        message = message[:600]

    # 2. Normalization & Language Detection
    normalized = normalize_query(message)
    detected_lang = detect_language(message)

    if detected_lang == "ta":
        lang = "ta"
    elif lang_override in ("en", "ta"):
        lang = lang_override
    else:
        lang = default_lang if default_lang in ("en", "ta") else "en"

    # 3. Farmer Profile & Recent Diagnosis Context
    farmer_profile = {}
    active_diagnosis = None

    if current_user:
        farmer_profile["name"] = current_user.name
        farmer_profile["village"] = current_user.village or "Tamil Nadu"
        farmer_profile["preferred_language"] = current_user.preferred_language.value

        # Check explicit diagnosis context from client or DB
        if diagnosis_context and diagnosis_context.get("disease"):
            active_diagnosis = dict(diagnosis_context)
            if active_diagnosis.get("variety"):
                farmer_profile["variety"] = active_diagnosis["variety"]
        elif diagnosis_id:
            diag = db.query(Diagnosis).filter(Diagnosis.id == diagnosis_id, Diagnosis.user_id == current_user.id).first()
            if diag:
                active_diagnosis = {
                    "id": diag.id,
                    "disease": diag.disease,
                    "confidence": round(diag.confidence * 100) if diag.confidence <= 1.0 else int(diag.confidence),
                    "variety": diag.variety,
                    "timestamp": str(diag.timestamp)
                }
                farmer_profile["variety"] = diag.variety
        else:
            # Look up most recent diagnosis from history
            latest_diag = db.query(Diagnosis).filter(Diagnosis.user_id == current_user.id).order_by(Diagnosis.timestamp.desc()).first()
            if latest_diag:
                active_diagnosis = {
                    "id": latest_diag.id,
                    "disease": latest_diag.disease,
                    "confidence": round(latest_diag.confidence * 100) if latest_diag.confidence <= 1.0 else int(latest_diag.confidence),
                    "variety": latest_diag.variety,
                    "timestamp": str(latest_diag.timestamp)
                }
                farmer_profile["variety"] = latest_diag.variety

    if "variety" not in farmer_profile:
        farmer_profile["variety"] = "S36"

    # 4. Intent Classification
    active_disease_name = active_diagnosis.get("disease") if active_diagnosis else None
    intent = detect_intent(
        normalized,
        lang=lang,
        has_diagnosis_context=bool(active_disease_name),
        session_history=session_history
    )

    # 5. Strict Safety Filters (Pre-LLM)

    # 5A. Actionable Pesticide / Chemical Safety Check
    pesticide_warning = check_pesticide_safety(normalized, lang)
    if pesticide_warning:
        return {
            "reply": pesticide_warning,
            "language": lang,
            "topic": "pesticide_safety",
            "intent": "CHEMICAL_RESTRICTION",
            "source": KNOWLEDGE_SOURCE_LABEL_TA if lang == "ta" else KNOWLEDGE_SOURCE_LABEL_EN,
            "diagnosis_context": active_diagnosis
        }

    # 5B. Smart Ambiguity Check
    if is_ambiguous(normalized):
        return {
            "reply": get_ambiguous_reply(normalized, lang),
            "language": lang,
            "topic": "ambiguous",
            "intent": INTENTS["AMBIGUOUS"],
            "source": KNOWLEDGE_SOURCE_LABEL_TA if lang == "ta" else KNOWLEDGE_SOURCE_LABEL_EN,
            "diagnosis_context": active_diagnosis
        }

    # 5C. Off-Topic Check
    if is_off_topic(normalized):
        return {
            "reply": get_off_topic_reply(lang),
            "language": lang,
            "topic": "off_topic",
            "intent": INTENTS["OFF_TOPIC"],
            "source": KNOWLEDGE_SOURCE_LABEL_TA if lang == "ta" else KNOWLEDGE_SOURCE_LABEL_EN,
            "diagnosis_context": active_diagnosis
        }

    # 6. Feature: What Should I Do Today?
    if intent == INTENTS["TODAY_CHECKLIST"]:
        checklist_reply = generate_today_checklist(lang, farmer_profile, active_diagnosis)
        return {
            "reply": checklist_reply,
            "language": lang,
            "topic": "daily_checklist",
            "intent": INTENTS["TODAY_CHECKLIST"],
            "source": KNOWLEDGE_SOURCE_LABEL_TA if lang == "ta" else KNOWLEDGE_SOURCE_LABEL_EN,
            "diagnosis_context": active_diagnosis
        }

    # 7. Diagnosis Follow-up Mode
    if intent == INTENTS["DIAGNOSIS_FOLLOWUP"] and active_disease_name:
        # Check specific follow-up questions
        if "irrigate" in normalized or "water" in normalized or "தண்ணீர்" in normalized or "பாசனம்" in normalized:
            if lang == "ta":
                reply = (
                    f"உங்கள் சமீபத்திய கண்டறிதல்: {active_disease_name} ({active_diagnosis.get('confidence', 85)}% நம்பிக்கை).\n\n"
                    f"🌿 இலை நோய் உள்ளபோது நீர்ப்பாசன வழிகாட்டுதல்:\n"
                    f"1. மேல் தெளிப்பு நீர்ப்பாசனத்தைத் தவிர்க்கவும் — இலைகளில் நீர் தெறிப்பது பூஞ்சை வித்திகளை பிற இலைகளுக்கு பரப்பும்.\n"
                    f"2. சொட்டு நீர் பாசனம் அல்லது வாய்க்கால் பாசனத்தைப் பயன்படுத்தி நேரடியாக வேர்களுக்கு நீர் பாய்ச்சவும்.\n"
                    f"3. அதிகாலை வேளையில் நீர் பாய்ச்சுவது நல்லது, இதனால் மாலைக்குள் இலைப்பரப்பு உலர்வாக இருக்கும்.\n\n"
                    f"⚠️ நீர் தேங்காமல் வடிகால் வசதியை உறுதி செய்யவும்.\n\n"
                    f"ஆதாரம்: {KNOWLEDGE_SOURCE_LABEL_TA}"
                )
            else:
                reply = (
                    f"Your active diagnosis context: {active_disease_name} ({active_diagnosis.get('confidence', 85)}% confidence on {farmer_profile.get('variety', 'S36')} variety).\n\n"
                    f"🌿 Irrigation Guidance for {active_disease_name}:\n"
                    f"1. Avoid overhead sprinkler irrigation — splashing water droplets spread fungal spores across healthy foliage.\n"
                    f"2. Use drip irrigation or ground furrows so water is applied directly to the root zone.\n"
                    f"3. Irrigate early in the morning so the garden canopy stays dry through the day.\n\n"
                    f"⚠️ Ensure adequate drainage to avoid waterlogging which exacerbates root weakness.\n\n"
                    f"Source: {KNOWLEDGE_SOURCE_LABEL_EN}"
                )
            return {
                "reply": reply,
                "language": lang,
                "topic": "irrigation",
                "intent": INTENTS["DIAGNOSIS_FOLLOWUP"],
                "source": KNOWLEDGE_SOURCE_LABEL_TA if lang == "ta" else KNOWLEDGE_SOURCE_LABEL_EN,
                "diagnosis_context": active_diagnosis
            }

    # 8. RAG Context Retrieval
    topic, context = retrieve_context(
        normalized,
        lang,
        db,
        active_disease=active_disease_name,
        intent=intent
    )

    if not context:
        # Grounded response: clearly acknowledge lack of verified data
        if lang == "ta":
            insufficient_reply = (
                "இந்த வழக்கில் பாதுகாப்பான வழிகாட்ட போதுமான சரிபார்க்கப்பட்ட தகவல் என்னிடம் இல்லை. "
                "தயவுசெய்து தகுதி வாய்ந்த பட்டுப்புழு வளர்ப்பு விரிவாக்க அலுவலரை அணுகவும்."
            )
        else:
            insufficient_reply = (
                "I don't have enough verified information to safely guide this case. "
                "Please consult a qualified sericulture extension officer."
            )
        return {
            "reply": insufficient_reply,
            "language": lang,
            "topic": "unknown",
            "intent": "UNKNOWN",
            "source": KNOWLEDGE_SOURCE_LABEL_TA if lang == "ta" else KNOWLEDGE_SOURCE_LABEL_EN,
            "diagnosis_context": active_diagnosis
        }

    # 9. Grounded Response Generation
    reply = generate_response(
        message,
        context,
        lang,
        farmer_profile=farmer_profile,
        diagnosis_context=active_diagnosis,
        session_history=session_history
    )

    # In follow-up mode, prepend diagnosis acknowledgement if not already mentioned
    if intent == INTENTS["DIAGNOSIS_FOLLOWUP"] and active_disease_name and active_disease_name.lower() not in reply.lower():
        prefix = (
            f"உங்கள் சமீபத்திய கண்டறிதல்: {active_disease_name} ({active_diagnosis.get('confidence', 85)}% நம்பிக்கை).\n\n"
            if lang == "ta" else
            f"Your recent diagnosis was {active_disease_name} with {active_diagnosis.get('confidence', 85)}% confidence.\n\n"
        )
        reply = prefix + reply

    return {
        "reply": reply,
        "language": lang,
        "topic": topic,
        "intent": intent,
        "source": KNOWLEDGE_SOURCE_LABEL_TA if lang == "ta" else KNOWLEDGE_SOURCE_LABEL_EN,
        "diagnosis_context": active_diagnosis
    }
