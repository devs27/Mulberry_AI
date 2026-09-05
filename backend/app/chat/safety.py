import re

# Off-topic words that indicate a completely unrelated conversation
OFF_TOPIC_KEYWORDS = [
    "python", "java", "c++", "javascript", "code", "programming", "mathematics", "math",
    "calculator", "joke", "jokes", "recipe", "recipes", "movie", "movies", "song", "songs",
    "president", "election", "politics", "stock", "bitcoin", "crypto", "cryptocurrency",
    "games", "play", "football", "cricket match", "hollywood", "bollywood",
    "mars", "planet", "space", "moon", "galaxy", "universe"
]

# Conceptual/educational terms that are SAFE to discuss
SAFE_CONCEPTUAL_PATTERNS = [
    r"\bwhat is (a |an )?(fungicide|pesticide|insecticide|disinfectant|bio-pesticide|neem oil)\b",
    r"\bdefine (fungicide|pesticide|insecticide)\b",
    r"\bmeaning of (fungicide|pesticide|insecticide)\b",
    r"\bwhy (should |do )?(silkworm|silkworms).*protect.*(chemical|residue|pesticide)\b",
    r"\bwhat are (fungicides|pesticides|insecticides)\b",
    r"\bபூச்சிக்கொல்லி என்றால் என்ன\b",
    r"\bபூஞ்சைக்கொல்லி என்றால் என்ன\b"
]

# Actionable chemical dosage / mixing ratio / brand request keywords (RESTRICTED)
RESTRICTED_CHEMICAL_KEYWORDS_EN = [
    "dosage", "dose", "chemical dose", "ml per litre", "ml/l", "gm/l", "grams per litre",
    "mixing ratio", "spray ratio", "how many ml", "how many grams", "how much chemical",
    "how many times should i spray", "how many times to spray", "spray quantity",
    "chemical brand", "chemical brands", "pesticide brand", "fungicide brand",
    "insecticide brand", "chemical recipe", "chemical spray schedule",
    "give pesticide dosage", "give chemical dosage", "recommend pesticide brand"
]

RESTRICTED_CHEMICAL_KEYWORDS_TA = [
    "மருந்தளவு", "இரசாயன அளவு", "கலவை விகிதம்", "அடர்த்தி", "எத்தனை மிலி",
    "எத்தனை கிராம்", "எத்தனை முறை தெளிக்க வேண்டும்", "பிராண்ட்", "இரசாயன பிராண்ட்",
    "பூச்சிக்கொல்லி பிராண்ட்", "மருந்து தெளிக்கும் அளவு"
]


def normalize_query(query: str) -> str:
    """
    Cleans punctuation, lowercases, and reduces multiple spaces.
    Preserves Tamil unicode characters (U+0B80 to U+0BFF).
    """
    if not query:
        return ""
    q = query.lower().strip()
    # Remove punctuation while preserving Tamil and alphanumeric characters
    q = re.sub(r"[^\w\s\u0b80-\u0bff]", " ", q)
    # Collapse multiple spaces
    q = re.sub(r"\s+", " ", q).strip()
    return q


def detect_language(query: str) -> str:
    """
    Detects if the query is in Tamil or English by scanning for Tamil unicode ranges.
    Tamil Unicode block is U+0B80 to U+0BFF (decimal 2944 to 3071).
    """
    for char in query:
        if 2944 <= ord(char) <= 3071:
            return "ta"
    return "en"


def is_off_topic(normalized_query: str) -> bool:
    """
    Checks if the query is clearly off-topic.
    """
    words = normalized_query.split()
    for word in words:
        if word in OFF_TOPIC_KEYWORDS:
            return True

    # Standalone general weather queries without sericulture anchor
    if "weather" in words or "forecast" in words:
        agri_words = ["mulberry", "silk", "leaf", "disease", "farm", "crop", "risk", "sericulture"]
        if not any(w in normalized_query for w in agri_words):
            return True

    # If the query is very short and has zero relevance to sericulture/farming
    agri_anchors = [
        "variety", "spacing", "water", "irrigation", "compost", "manure", "fertilizer", "pruning", "weed",
        "harvest", "feeding", "rearing", "disease", "rust", "spot", "mildew", "blight", "silkworm", "cocoon",
        "market", "sell", "quality", "reeler", "reeling", "plant", "sapling", "fici", "leaf", "leaves",
        "chawki", "instar", "moult", "chandrika", "vijetha", "mealybug", "tukra", "thrips", "caterpillar",
        "வகை", "இடைவெளி", "நீர்", "பாசனம்", "உரம்", "கவாத்து", "களை", "அறுவடை", "உணவளி", "வளர்ப்பு",
        "நோய்", "துரு", "புள்ளி", "சாம்பல்", "புழு", "கூடு", "சந்தை", "விற்பனை", "தரம்", "இலை", "தண்ணீர்",
        "சௌக்கி", "சந்திரிகா", "விஜேதா", "பூச்சி"
    ]

    if len(words) > 0:
        has_anchor = any(anchor in normalized_query for anchor in agri_anchors)
        if not has_anchor and len(words) <= 2:
            return True

    return False


def is_ambiguous(normalized_query: str) -> bool:
    """
    Detects vague single-word or under-specified questions that require clarification.
    """
    vague_patterns = [
        r"^leaves$", r"^leaf$", r"^yellow$", r"^spots$", r"^spots on leaves$", r"^yellowing$",
        r"^disease$", r"^plant$", r"^silkworm$", r"^silkworms$", r"^cocoon$", r"^worms$",
        r"^yellow leaves$", r"^yellowing leaves$", r"^leaf disease$", r"^worms sick$",
        r"^worm sick$", r"^sick worms$", r"^silkworms sick$",
        r"^இலை$", r"^இலைகள்$", r"^மஞ்சள்$", r"^புள்ளிகள்$", r"^நோய்$", r"^மஞ்சள் இலைகள்$",
        r"^புழு$", r"^புழுக்கள்$", r"^புழு நோய்$"
    ]
    for pattern in vague_patterns:
        if re.match(pattern, normalized_query):
            return True
    return False


def get_ambiguous_reply(normalized_query: str, lang: str = "en") -> str:
    """
    Provides structured, guided multiple-choice questions to help the farmer clarify
    rather than simply refusing. Includes 'fertilizer, pests, or disease' anchor.
    """
    q = normalized_query.lower()

    # Yellowing ambiguity
    if "yellow" in q or "மஞ்சள்" in q:
        if lang == "ta":
            return (
                "மல்பெரி இலைகளில் மஞ்சள் நிறம் எங்கு காணப்படுகிறது என்பதை தெளிவாக தெரிவிக்கவும் (உரம், பூச்சி அல்லது நோய்):\n"
                "① இளம் தளிர்களில் மட்டும் உள்ளதா?\n"
                "② அடிப்புற முதிர்ந்த இலைகளில் உள்ளதா?\n"
                "③ செடி முழுவதும் பரவியுள்ளதா?\n"
                "④ புள்ளிகள் அல்லது துரு போன்ற துகள்களுடன் உள்ளதா?"
            )
        return (
            "Please tell me whether the issue is related to leaves, fertilizer, pests, or disease:\n"
            "Is the yellowing on:\n"
            "① Young leaves (top tender shoots)\n"
            "② Older leaves (bottom mature foliage)\n"
            "③ Most of the plant uniformly\n"
            "④ Accompanied by spots or rust pustules?"
        )

    # Spots ambiguity
    if "spot" in q or "புள்ளி" in q:
        if lang == "ta":
            return (
                "இலைகளில் உள்ள புள்ளிகளின் தன்மையை தெளிவாக தெரிவிக்கவும் (உரம், பூச்சி அல்லது நோய்):\n"
                "① பழுப்பு நிற வட்டப் புள்ளிகளா?\n"
                "② கருப்பு நிற கருகிய திட்டுகளா?\n"
                "③ வெள்ளை நிற மாவுப் படலமா (சாம்பல் நோய்)?\n"
                "④ துரு போன்ற ஆரஞ்சு/பழுப்பு நிற துகள்களா?\n"
                "⑤ வேறு ஏதேனும் அறிகுறிகளா?"
            )
        return (
            "Please tell me whether the issue is related to leaves, fertilizer, pests, or disease:\n"
            "Are the spots:\n"
            "① Brown circular spots with dark rings (possible Leaf Spot)\n"
            "② Black or dark necrotic patches\n"
            "③ White/powdery powdery coating on surface (possible Powdery Mildew)\n"
            "④ Rust-colored / reddish-brown raised pustules (possible Leaf Rust)\n"
            "⑤ Something else?"
        )

    # Silkworms sick ambiguity
    if any(w in q for w in ["worm", "worms", "silkworm", "புழு"]):
        if lang == "ta":
            return (
                "பட்டுப்புழுக்களில் நீங்கள் காணும் அறிகுறிகளை தெரிவிக்கவும் (வளர்ப்பு, பூச்சி அல்லது நோய்):\n"
                "① உடல் மென்மையாகி அழுகுதல் (பிளாசெரி)\n"
                "② சுண்ணாம்பு போன்று வெண்மையாக கடினமாதல் (மஸ்கார்டின்)\n"
                "③ உடல் உப்பி பால் போன்ற திரவம் வடிதல் (கிராஸரி)\n"
                "④ இலைகளை உண்ணாமல் மந்தமாக இருத்தல்\n"
                "⑤ பிற அறிகுறிகள்"
            )
        return (
            "Please tell me what symptoms you observe in your silkworms (fertilizer, pests, or disease):\n"
            "① Body becoming soft and rotting (possible Flacherie)\n"
            "② White powder/chalky stiff body (possible Muscardine)\n"
            "③ Swelling/milky fluid appearance (possible Grasserie)\n"
            "④ Poor feeding and sluggish movement\n"
            "⑤ Other symptoms"
        )

    # General default ambiguity
    if lang == "ta":
        return (
            "மல்பெரி சாகுபடி மற்றும் பட்டுப்புழு வளர்ப்பு குறித்து நான் உதவ முடியும். "
            "இலைகள், நீர்ப்பாசனம், உரம், பூச்சி அல்லது நோய் தொடர்பான பிரச்சினையை தெளிவாக தெரிவிக்கவும்."
        )
    return (
        "I can help with mulberry cultivation and sericulture. "
        "Please tell me whether the issue is related to leaves, watering, fertilizer, pests, or disease."
    )


def get_off_topic_reply(lang: str) -> str:
    """Standard off-topic refusal reply."""
    if lang == "ta":
        return "மல்பெரி சாகுபடி மற்றும் பட்டுப்புழு வளர்ப்பு குறித்து மட்டுமே என்னால் உதவ முடியும்."
    return "I can help only with mulberry cultivation and sericulture."


def check_pesticide_safety(normalized_query: str, lang: str) -> str:
    """
    Distinguishes safe conceptual inquiries from restricted chemical brand/dosage/mixing requests.
    Returns restriction message if the user asks for actionable chemical dosages or brand recommendations.
    """
    q = normalized_query.lower()

    # First check: Is it an educational / conceptual question?
    is_safe_conceptual = any(re.search(pattern, q) for pattern in SAFE_CONCEPTUAL_PATTERNS)
    # Check if asking for dosage or brand specifically
    has_dosage_intent = any(k in q for k in ["dosage", "dose", "ml", "gram", "ratio", "concentration", "spray how many", "brand"])

    if is_safe_conceptual and not has_dosage_intent:
        return None  # Allow safe educational question to proceed to RAG

    # Check for restricted actionable chemical keywords
    is_restricted = False
    if lang == "ta":
        is_restricted = any(k in q for k in RESTRICTED_CHEMICAL_KEYWORDS_TA)
    else:
        is_restricted = any(k in q for k in RESTRICTED_CHEMICAL_KEYWORDS_EN)

    # Also catch direct "pesticide" or "chemical" queries that ask "how much" or "give" or "spray"
    if not is_restricted:
        chemical_nouns = ["pesticide", "fungicide", "insecticide", "chemical", "spray"]
        action_verbs = ["give", "how much", "how many", "recommend", "apply", "use", "brand", "dose"]
        if any(cn in q for cn in chemical_nouns) and any(av in q for av in action_verbs):
            is_restricted = True

    if is_restricted:
        if lang == "ta":
            return (
                "இரசாயன மருந்தளவு, கலவை விகிதம் அல்லது தெளிக்கும் வழிமுறைகளை என்னால் வழங்க முடியாது. "
                "அனுமதிக்கப்பட்ட தயாரிப்பு வழிகாட்டுதலைப் பின்பற்றவும் அல்லது தகுதி வாய்ந்த பட்டுப்புழு வளர்ப்பு அலுவலரை அணுகவும்."
            )
        return (
            "I can't provide chemical dosage, mixing ratios, or application instructions. "
            "Please follow the approved product label/advisory or consult a qualified sericulture officer."
        )

    return None
