import re
from typing import Optional, List, Dict

INTENTS = {
    "LEAF_DISEASE": "LEAF_DISEASE",
    "MULBERRY_CULTIVATION": "MULBERRY_CULTIVATION",
    "IRRIGATION": "IRRIGATION",
    "FERTILIZER": "FERTILIZER",
    "PRUNING": "PRUNING",
    "PEST": "PEST",
    "SILKWORM_HEALTH": "SILKWORM_HEALTH",
    "SILKWORM_REARING": "SILKWORM_REARING",
    "COCOON_PRODUCTION": "COCOON_PRODUCTION",
    "COCOON_MARKET": "COCOON_MARKET",
    "WEATHER_RISK": "WEATHER_RISK",
    "DIAGNOSIS_FOLLOWUP": "DIAGNOSIS_FOLLOWUP",
    "TODAY_CHECKLIST": "TODAY_CHECKLIST",
    "GENERAL_SERICULTURE": "GENERAL_SERICULTURE",
    "OFF_TOPIC": "OFF_TOPIC",
    "AMBIGUOUS": "AMBIGUOUS"
}


def detect_intent(
    normalized_query: str,
    lang: str = "en",
    has_diagnosis_context: bool = False,
    session_history: Optional[List[Dict]] = None
) -> str:
    """
    Classifies user intent using deterministic keyword and context rules.
    Does not require an external LLM call.
    """
    q = normalized_query.lower().strip()

    # 1. Today Checklist Intent
    today_keywords = [
        "what should i do today", "what to do today", "today checklist", "today s checklist",
        "today task", "daily checklist", "farm checklist", "today farm",
        "இன்று என்ன செய்ய வேண்டும்", "இன்றைய வேலைகள்", "இன்றைய சரிபார்ப்பு", "இன்றைய பண்ணை"
    ]
    if any(k in q for k in today_keywords) or (
        ("இன்று" in q or "இன்றைய" in q) and any(w in q for w in ["செய்ய வேண்டும்", "வேலை", "பண்ணை", "சரிபார்ப்பு", "பட்டியல்"])
    ):
        return INTENTS["TODAY_CHECKLIST"]

    # 2. Diagnosis Follow-Up Intent
    # When user is continuing a discussion about a diagnosed disease (e.g., Leaf Rust/Spot)
    followup_phrases = [
        "what should i do", "what to do", "how to cure it", "how do i control it", "how to treat it",
        "will it spread", "is it dangerous", "can i irrigate", "can i spray", "how to cure this",
        "how to control this disease", "tell me about this disease",
        "என்ன செய்ய வேண்டும்", "எப்படி குணப்படுத்துவது", "எப்படி கட்டுப்படுத்துவது", "பரவுமா", "தண்ணீர் பாய்ச்சலாமா"
    ]
    if has_diagnosis_context:
        if any(p in q for p in followup_phrases) or "it" in q.split() or "this" in q.split():
            return INTENTS["DIAGNOSIS_FOLLOWUP"]

    # 3. Pruning Intent
    pruning_keywords = [
        "prune", "pruning", "cut branch", "branch cutting", "bottom pruning", "harvest cut",
        "கவாத்து", "கத்தரித்தல்", "கிளை வெட்டுதல்", "கவாத்து செய்தல்"
    ]
    if any(k in q for k in pruning_keywords):
        return INTENTS["PRUNING"]

    # 4. Irrigation Intent
    irrigation_keywords = [
        "water", "watering", "irrigation", "irrigate", "irrigating", "drip", "moisture", "waterlogging", "how often to water",
        "தண்ணீர்", "நீர்", "நீர்ப்பாசனம்", "சொட்டு நீர்", "பாய்ச்சுதல்", "ஈரப்பதம்"
    ]
    if any(k in q for k in irrigation_keywords):
        if has_diagnosis_context and ("can i irrigate" in q or "can i water" in q or "disease" in q):
            return INTENTS["DIAGNOSIS_FOLLOWUP"]
        return INTENTS["IRRIGATION"]

    # 5. Fertilizer & Manure Intent
    fertilizer_keywords = [
        "fertilizer", "fertilization", "npk", "urea", "potash", "nitrogen", "manure",
        "compost", "farmyard", "fym", "vermicompost", "organic manure",
        "உரம்", "உரமிடுதல்", "என்பிகே", "யுரியா", "பொட்டாஷ்", "தொழு உரம்", "மட்கிய உரம்", "மண்புழு உரம்"
    ]
    if any(k in q for k in fertilizer_keywords):
        return INTENTS["FERTILIZER"]

    # 6. Pest Management Intent
    pest_keywords = [
        "pest", "pests", "insect", "mealybug", "tukra", "leaf roller", "caterpillar", "thrips", "bug",
        "பூச்சி", "பூச்சிகள்", "மாவுப்பூச்சி", "துக்ரா", "இலை சுருட்டு", "கம்பளிப்புழு", "இலைப்பேன்"
    ]
    if any(k in q for k in pest_keywords):
        return INTENTS["PEST"]

    # 7. Silkworm Health & Disease Intent
    silkworm_health_keywords = [
        "worm sick", "silkworm sick", "grasserie", "flacherie", "muscardine", "pebrine",
        "dead silkworm", "dead worm", "silkworm disease", "larva sick",
        "புழு நோய்", "கிராஸரி", "பிளாசெரி", "மஸ்கார்டின்", "பெப்ரின்", "புழு இறப்பு"
    ]
    if any(k in q for k in silkworm_health_keywords):
        return INTENTS["SILKWORM_HEALTH"]

    # 8. Silkworm Rearing Intent
    silkworm_rearing_keywords = [
        "rearing", "silkworm rearing", "instar", "chawki", "moult", "bed clean", "vijetha",
        "cleaning net", "feed silkworm", "silkworm food", "chopped leaves", "rearing house",
        "வளர்ப்பு", "பட்டுப்புழு வளர்ப்பு", "சௌக்கி", "இன்ஸ்டார்", "தோல் உரித்தல்", "படுக்கை சுத்தம்", "விஜேதா"
    ]
    if any(k in q for k in silkworm_rearing_keywords):
        return INTENTS["SILKWORM_REARING"]

    # 9. Cocoon Production Intent
    cocoon_prod_keywords = [
        "cocoon harvest", "harvesting cocoon", "mounting", "chandrika", "defloss", "pupation", "pupa",
        "கூடு அறுவடை", "பட்டுக்கூடு அறுவடை", "சந்திரிகா", "கூட்டுப்புழு"
    ]
    if any(k in q for k in cocoon_prod_keywords):
        return INTENTS["COCOON_PRODUCTION"]

    # 10. Cocoon Market & Price Intent
    market_keywords = [
        "sell cocoon", "selling cocoon", "cocoon market", "price", "renditta", "shell ratio",
        "shell percentage", "ramanagara", "hosur", "reeler", "auction", "factory buy",
        "சந்தை", "கூடு விற்பனை", "பட்டுக்கூடு விலை", "ரெண்டிட்டா", "ஓடு சதவீதம்", "ஏலம்", "தொழிற்சாலை"
    ]
    if any(k in q for k in market_keywords):
        return INTENTS["COCOON_MARKET"]

    # 11. Weather Risk Intent
    weather_keywords = [
        "weather risk", "humidity risk", "climate risk", "weather alert", "disease risk forecast",
        "வானிலை ஆபத்து", "ஈரப்பதம் ஆபத்து"
    ]
    if any(k in q for k in weather_keywords):
        return INTENTS["WEATHER_RISK"]

    # 12. Leaf Disease Intent
    leaf_disease_keywords = [
        "disease", "rust", "spot", "mildew", "blight", "yellowing", "pustule",
        "cercospora", "cerotelium", "fungus", "leaf health", "leaf rot",
        "நோய்", "துரு", "புள்ளி", "சாம்பல்", "வெம்பல்", "இலை நோய்"
    ]
    if any(k in q for k in leaf_disease_keywords):
        return INTENTS["LEAF_DISEASE"]

    # 13. Mulberry Cultivation & Agronomy Intent
    cultivation_keywords = [
        "variety", "varieties", "planting", "spacing", "distance", "cuttings", "sapling",
        "soil prep", "propagate", "v1", "s36", "m5", "g4", "mr2", "kanva", "victory",
        "வகை", "வகைகள்", "நடவு", "இடைவெளி", "நாற்று", "போத்து"
    ]
    if any(k in q for k in cultivation_keywords):
        return INTENTS["MULBERRY_CULTIVATION"]

    return INTENTS["GENERAL_SERICULTURE"]
