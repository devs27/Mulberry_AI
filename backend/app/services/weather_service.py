import random
from typing import List, Dict


def get_weather(village: str) -> Dict[str, any]:
    """
    Simulates weather based on village name hashing for deterministic testing,
    unless an external provider API is configured.
    """
    # Seed with village name to get consistent weather for the same location
    seed_str = (village or "default_village").lower().strip()
    # Simple hash of string to seed random generator
    seed_val = sum(ord(char) * (idx + 1) for idx, char in enumerate(seed_str))
    random.seed(seed_val)

    temp = round(random.uniform(21.0, 32.5), 1)
    humidity = round(random.uniform(55.0, 88.0), 1)
    rainfall = round(random.uniform(0.0, 10.0), 1)

    # Determine condition
    if rainfall > 4.0:
        condition_en = "Rainy"
        condition_ta = "மழை"
    elif humidity > 78.0:
        condition_en = "Humid / Overcast"
        condition_ta = "அதிக ஈரப்பதம் / மேகமூட்டம்"
    elif temp > 29.0:
        condition_en = "Sunny"
        condition_ta = "வெயில்"
    else:
        condition_en = "Clear"
        condition_ta = "தெளிவான வானிலை"

    return {
        "temp": temp,
        "humidity": humidity,
        "rainfall": rainfall,
        "condition": {
            "en": condition_en,
            "ta": condition_ta
        }
    }


def calculate_disease_risk(weather: Dict[str, any]) -> List[Dict[str, any]]:
    """
    Runs agricultural rules based on weather conditions to forecast disease risk.
    """
    temp = weather["temp"]
    humidity = weather["humidity"]
    rainfall = weather["rainfall"]

    risks = []

    # 1. Leaf Rust Risk
    if 22.0 <= temp <= 30.0 and humidity > 75.0:
        rust_level = "High"
        rust_reason_en = f"Warm temperature ({temp}°C) and high humidity ({humidity}%) create an ideal environment for Leaf Rust germination."
        rust_reason_ta = f"வெப்பநிலை ({temp}°C) மற்றும் அதிக ஈரப்பதம் ({humidity}%) இலை துரு நோய் முளைப்பதற்கு ஏற்ற சூழலை உருவாக்குகின்றன."
    elif 20.0 <= temp <= 32.0 and humidity > 70.0:
        rust_level = "Moderate"
        rust_reason_en = f"Moderate temperatures ({temp}°C) and humidity ({humidity}%) may encourage rust spreading."
        rust_reason_ta = f"மிதமான வெப்பநிலை ({temp}°C) மற்றும் ஈரப்பதம் ({humidity}%) துரு நோய் பரவுவதை ஊக்குவிக்கலாம்."
    else:
        rust_level = "Low"
        rust_reason_en = "Current weather conditions do not favor Leaf Rust spore development."
        rust_reason_ta = "தற்போதைய வானிலை துரு நோய் வித்திகள் வளர்வதற்கு சாதகமாக இல்லை."

    risks.append({
        "disease": "Leaf Rust",
        "disease_ta": "இலை துரு நோய்",
        "risk_level": rust_level,
        "reason": {
            "en": rust_reason_en,
            "ta": rust_reason_ta
        },
        "disclaimer": {
            "en": "This is a weather-based risk warning, not a confirmed leaf diagnosis.",
            "ta": "இது வானிலை அடிப்படையிலான நோய் அபாய எச்சரிக்கை மட்டுமே, உறுதிப்படுத்தப்பட்ட இலை நோய் கண்டறிதல் அல்ல."
        }
    })

    # 2. Leaf Spot Risk
    if 24.0 <= temp <= 32.0 and (rainfall > 3.0 or humidity > 80.0):
        spot_level = "High"
        spot_reason_en = f"Warm temperatures ({temp}°C) and wet conditions (rainfall: {rainfall}mm, humidity: {humidity}%) promote Leaf Spot fungal spread."
        spot_reason_ta = f"வெப்பநிலை ({temp}°C) மற்றும் ஈரமான நிலை (மழை: {rainfall}மிமீ, ஈரப்பதம்: {humidity}%) இலைப்புள்ளி பூஞ்சை பரவுவதை ஊக்குவிக்கிறது."
    elif 22.0 <= temp <= 34.0 and humidity > 68.0:
        spot_level = "Moderate"
        spot_reason_en = f"Humid climate ({humidity}%) increases the chance of Leaf Spot spores distribution."
        spot_reason_ta = f"ஈரப்பதமான காலநிலை ({humidity}%) இலைப்புள்ளி வித்திகள் விநியோகிக்கப்படுவதற்கான வாய்ப்பை அதிகரிக்கிறது."
    else:
        spot_level = "Low"
        spot_reason_en = "Environmental factors are currently unfavourable for Leaf Spot propagation."
        spot_reason_ta = "சுற்றுச்சூழல் காரணிகள் தற்போது இலைப்புள்ளி நோய் பெருக்கத்திற்கு சாதகமற்றவை."

    risks.append({
        "disease": "Leaf Spot",
        "disease_ta": "இலைப்புள்ளி நோய்",
        "risk_level": spot_level,
        "reason": {
            "en": spot_reason_en,
            "ta": spot_reason_ta
        },
        "disclaimer": {
            "en": "This is a weather-based risk warning, not a confirmed leaf diagnosis.",
            "ta": "இது வானிலை அடிப்படையிலான நோய் அபாய எச்சரிக்கை மட்டுமே, உறுதிப்படுத்தப்பட்ட இலை நோய் கண்டறிதல் அல்ல."
        }
    })

    # 3. Powdery Mildew Risk
    if 20.0 <= temp <= 28.0 and humidity > 70.0:
        mildew_level = "High"
        mildew_reason_en = f"Cooler warm weather ({temp}°C) and high humidity ({humidity}%) highly promote Powdery Mildew development."
        mildew_reason_ta = f"குளிர்ச்சியான வெப்ப காலநிலை ({temp}°C) மற்றும் அதிக ஈரப்பதம் ({humidity}%) சாம்பல் நோய் வளர்ச்சியை பெரிதும் ஊக்குவிக்கின்றன."
    elif 18.0 <= temp <= 30.0 and humidity > 65.0:
        mildew_level = "Moderate"
        mildew_reason_en = f"Weather conditions (Temp: {temp}°C, Humidity: {humidity}%) moderately favor powdery mildew formation."
        mildew_reason_ta = f"வானிலை நிலைமைகள் (வெப்பநிலை: {temp}°C, ஈரப்பதம்: {humidity}%) சாம்பல் நோய் உருவாவதை மிதமாக ஆதரிக்கின்றன."
    else:
        mildew_level = "Low"
        mildew_reason_en = "Current weather parameters do not favor Powdery Mildew spreading."
        mildew_reason_ta = "தற்போதைய வானிலை அளவீடுகள் சாம்பல் நோய் பரவுவதற்கு சாதகமாக இல்லை."

    risks.append({
        "disease": "Powdery Mildew",
        "disease_ta": "சாம்பல் நோய்",
        "risk_level": mildew_level,
        "reason": {
            "en": mildew_reason_en,
            "ta": mildew_reason_ta
        },
        "disclaimer": {
            "en": "This is a weather-based risk warning, not a confirmed leaf diagnosis.",
            "ta": "இது வானிலை அடிப்படையிலான நோய் அபாய எச்சரிக்கை மட்டுமே, உறுதிப்படுத்தப்பட்ட இலை நோய் கண்டறிதல் அல்ல."
        }
    })

    return risks
