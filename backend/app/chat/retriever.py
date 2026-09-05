from typing import Optional, Tuple
from sqlalchemy.orm import Session
from app.models.disease_info import DiseaseInformation
from app.chat.knowledge_base import (
    KNOWLEDGE_BASE,
    KNOWLEDGE_SOURCE_LABEL_EN,
    KNOWLEDGE_SOURCE_LABEL_TA
)


def retrieve_context(
    normalized_query: str,
    lang: str,
    db: Session,
    active_disease: Optional[str] = None,
    intent: Optional[str] = None
) -> Tuple[Optional[str], Optional[str]]:
    """
    Multi-priority agricultural context retrieval:
    Priority 1: SQLite disease_information table
    Priority 2: Curated sericulture knowledge base
    Priority 3: Contextual diagnosis follow-up information
    
    Returns (topic, context_string).
    """
    q = normalized_query.lower()

    # -------------------------------------------------------------
    # PRIORITY 1: Check Database Table (disease_information)
    # -------------------------------------------------------------
    target_disease_name = None
    if active_disease:
        target_disease_name = active_disease.lower()

    db_diseases = db.query(DiseaseInformation).all()
    for disease in db_diseases:
        name_lower = disease.name.lower()
        is_match = False

        if name_lower in q:
            is_match = True
        elif target_disease_name and name_lower in target_disease_name:
            # Active diagnosis match in follow-up mode
            # Match ONLY if user is in follow-up mode or referring to the disease / management
            followup_indicators = [
                "it", "this", "cure", "treat", "control", "spread", "disease", "spray", "prevent", "symptom",
                "இந்த", "குணப்படுத்த", "கட்டுப்படுத்த", "பரவு", "நோய்", "மருந்து", "என்ன செய்ய"
            ]
            if intent == "DIAGNOSIS_FOLLOWUP" or any(ind in q.split() or ind in q for ind in followup_indicators):
                is_match = True
        elif "rust" in name_lower and ("rust" in q or "துரு" in q):
            is_match = True
        elif "spot" in name_lower and ("spot" in q or "புள்ளி" in q):
            is_match = True
        elif "mildew" in name_lower and ("mildew" in q or "சாம்பல்" in q):
            is_match = True
        elif "blight" in name_lower and ("blight" in q or "வெம்பல்" in q):
            is_match = True

        if is_match:
            source_label = KNOWLEDGE_SOURCE_LABEL_TA if lang == "ta" else KNOWLEDGE_SOURCE_LABEL_EN
            if lang == "ta":
                context_str = (
                    f"🌿 சாத்தியமான பிரச்சனை: {disease.name}\n"
                    f"அறிகுறிகள்: {disease.symptoms_ta}\n"
                    f"காரணங்கள் (WHY): {disease.causes_ta}\n"
                    f"இப்போது என்ன செய்ய வேண்டும் (WHAT TO DO NOW): {disease.management_ta}\n"
                    f"தடுப்புமுறைகள் (WATCH FOR): {disease.prevention_ta}\n"
                    f"எப்போது நிபுணரை அணுக வேண்டும்: அறிகுறிகள் தீவிரமடைந்து 20% மேலான பயிரில் பரவினால் உள்ளூர் பட்டு வளர்ச்சி அதிகாரியை அணுகவும்.\n"
                    f"பொறுப்புத் துறப்பு: {disease.disclaimer_ta}\n"
                    f"ஆதாரம்: {source_label}"
                )
            else:
                context_str = (
                    f"🌿 POSSIBLE ISSUE: {disease.name}\n"
                    f"Symptoms: {disease.symptoms_en}\n"
                    f"Causes (WHY): {disease.causes_en}\n"
                    f"WHAT TO DO NOW: {disease.management_en}\n"
                    f"Prevention (WATCH FOR): {disease.prevention_en}\n"
                    f"WHEN TO SEEK EXPERT HELP: If symptoms worsen or spread across >20% of your crop, consult your district sericulture extension officer.\n"
                    f"Disclaimer: {disease.disclaimer_en}\n"
                    f"Source: {source_label}"
                )
            return disease.name.lower().replace(" ", "_"), context_str

    # -------------------------------------------------------------
    # PRIORITY 2: Check Local Curated Knowledge Base
    # -------------------------------------------------------------
    best_topic = None
    max_matches = 0
    words = set(q.split())

    # Direct intent mapping fallback
    intent_to_topic_map = {
        "PRUNING": "pruning",
        "IRRIGATION": "irrigation",
        "FERTILIZER": "fertilization",
        "PEST": "pests",
        "SILKWORM_HEALTH": "rearing_disease",
        "SILKWORM_REARING": "rearing",
        "COCOON_PRODUCTION": "cocoon_harvesting",
        "COCOON_MARKET": "market_selling",
        "MULBERRY_CULTIVATION": "varieties"
    }

    for topic, data in KNOWLEDGE_BASE.items():
        kw_list = data.get("keywords_en", []) + data.get("keywords_ta", [])
        match_count = 0
        for kw in kw_list:
            kw_l = kw.lower()
            if " " in kw_l:
                if kw_l in q:
                    match_count += 2
            else:
                if kw_l in words or (len(kw_l) > 3 and kw_l in q):
                    match_count += 1

        if match_count > max_matches:
            max_matches = match_count
            best_topic = topic

    if not best_topic and intent in intent_to_topic_map:
        fallback_topic = intent_to_topic_map[intent]
        if fallback_topic in KNOWLEDGE_BASE:
            best_topic = fallback_topic
            max_matches = 1

    if best_topic and (max_matches > 0 or intent):
        data = KNOWLEDGE_BASE[best_topic]
        ans_key = "answer_ta" if lang == "ta" else "answer_en"
        struct_key = "structured_ta" if lang == "ta" else "structured_en"

        # Check if structured response is defined
        if struct_key in data:
            s = data[struct_key]
            actions_formatted = "\n".join([f"{i+1}. {act}" for i, act in enumerate(s["what_to_do"])])
            source_lbl = KNOWLEDGE_SOURCE_LABEL_TA if lang == "ta" else KNOWLEDGE_SOURCE_LABEL_EN

            if lang == "ta":
                context_str = (
                    f"🌿 தலைப்பு / சாத்தியமான பிரச்சனை: {s['possible_issue']}\n"
                    f"காரணம் (WHY):\n• {s['why']}\n\n"
                    f"இப்போது என்ன செய்ய வேண்டும் (WHAT TO DO NOW):\n{actions_formatted}\n\n"
                    f"⚠️ கவனிக்க வேண்டியவை (WATCH FOR):\n• {s['watch_for']}\n\n"
                    f"👨🌾 எப்போது நிபுணரை அணுக வேண்டும்:\n{s['expert_help']}\n\n"
                    f"ஆதாரம்: {source_lbl}"
                )
            else:
                context_str = (
                    f"🌿 TOPIC / POSSIBLE ISSUE: {s['possible_issue']}\n"
                    f"WHY:\n• {s['why']}\n\n"
                    f"WHAT TO DO NOW:\n{actions_formatted}\n\n"
                    f"⚠️ WATCH FOR:\n• {s['watch_for']}\n\n"
                    f"👨🌾 WHEN TO SEEK EXPERT HELP:\n{s['expert_help']}\n\n"
                    f"Source: {source_lbl}"
                )
        else:
            source_lbl = KNOWLEDGE_SOURCE_LABEL_TA if lang == "ta" else KNOWLEDGE_SOURCE_LABEL_EN
            context_str = f"{data[ans_key]}\n\nSource: {source_lbl}"

        return best_topic, context_str

    return None, None
