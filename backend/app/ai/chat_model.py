import os
import json
import urllib.request
from typing import Optional, Dict, List
from urllib.error import URLError, HTTPError

SYSTEM_PROMPT = """You are Ask MulberryCare, an action-oriented farmer decision support assistant for sericulture and mulberry agriculture.

Your goal is to provide practical, grounded responses generated using retrieved agricultural context and safety validation.

{farmer_profile_section}
{diagnosis_context_section}
{conversation_history_section}

Supplied MulberryCare Verified Knowledge:
{context}

Farmer's Current Question:
{question}

Instructions:
1. Grounded Factual Truth: Use ONLY the supplied MulberryCare knowledge as your source. Never invent pesticides, chemical dosages, mixing ratios, spray quantities, or market price guarantees.
2. Structure: For agricultural, disease, pest, or cultivation issues, format your answer clearly with:
   🌿 POSSIBLE ISSUE / FOCUS: Short explanation
   WHY: 1-2 bullet points on causes/triggers
   WHAT TO DO NOW: 2-3 practical, numbered steps
   ⚠️ WATCH FOR: Warning signs or secondary risks
   👨🌾 WHEN TO SEEK EXPERT HELP: Advice on when to consult an extension officer
   For simple factual queries, provide a direct, concise explanation.
3. Language: Respond fluently and naturally in {language_label} (farmer-friendly phrasing, not robotic or word-for-word translation).
4. Insufficient Knowledge: If the supplied knowledge does not contain enough verified information, state:
   "I don't have enough verified information to safely guide this case. Please consult a qualified sericulture extension officer."
"""


def generate_response(
    question: str,
    context: str,
    language: str,
    farmer_profile: Optional[Dict] = None,
    diagnosis_context: Optional[Dict] = None,
    session_history: Optional[List[Dict]] = None
) -> str:
    """
    Generates a grounded RAG response.
    Calls Gemini API if GEMINI_API_KEY is configured and reachable.
    Falls back gracefully to a verified structured local response when offline or unconfigured.
    """
    api_key = os.getenv("GEMINI_API_KEY")
    model_name = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")
    lang_label = "Tamil" if language == "ta" else "English"

    # 1. Format Farmer Profile Context
    farmer_profile_section = ""
    if farmer_profile:
        parts = []
        if farmer_profile.get("name"):
            parts.append(f"Name: {farmer_profile['name']}")
        if farmer_profile.get("variety"):
            parts.append(f"Mulberry Variety: {farmer_profile['variety']}")
        if farmer_profile.get("village"):
            parts.append(f"Village/Location: {farmer_profile['village']}")
        if parts:
            farmer_profile_section = "Farmer Profile Context:\n" + "\n".join(parts) + "\n"

    # 2. Format Diagnosis Context
    diagnosis_context_section = ""
    if diagnosis_context and diagnosis_context.get("disease"):
        conf_str = f"{diagnosis_context.get('confidence')}%" if diagnosis_context.get("confidence") else "Unknown"
        var_str = f", Variety: {diagnosis_context.get('variety')}" if diagnosis_context.get("variety") else ""
        diagnosis_context_section = (
            f"Active Recent Leaf Diagnosis:\n"
            f"- Disease: {diagnosis_context['disease']}\n"
            f"- Confidence: {conf_str}{var_str}\n"
        )

    # 3. Format Short-Term Conversation History (last 3-5 turns)
    conversation_history_section = ""
    if session_history and len(session_history) > 0:
        recent_turns = session_history[-4:]
        history_lines = []
        for msg in recent_turns:
            role = "Farmer" if msg.get("role") == "user" else "Assistant"
            content = msg.get("content", "").replace("\n", " ").strip()
            if content:
                history_lines.append(f"{role}: {content[:150]}")
        if history_lines:
            conversation_history_section = "Recent Conversation History:\n" + "\n".join(history_lines) + "\n"

    if api_key:
        prompt = SYSTEM_PROMPT.format(
            farmer_profile_section=farmer_profile_section,
            diagnosis_context_section=diagnosis_context_section,
            conversation_history_section=conversation_history_section,
            context=context,
            question=question,
            language_label=lang_label
        )
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={api_key}"

        payload = {
            "contents": [{
                "parts": [{
                    "text": prompt
                }]
            }],
            "generationConfig": {
                "temperature": 0.2,
                "topP": 0.95,
                "maxOutputTokens": 1000
            }
        }

        try:
            req = urllib.request.Request(
                url,
                data=json.dumps(payload).encode("utf-8"),
                headers={"Content-Type": "application/json"},
                method="POST"
            )
            with urllib.request.urlopen(req, timeout=10) as response:
                res_data = json.loads(response.read().decode("utf-8"))
                candidates = res_data.get("candidates", [])
                if candidates:
                    parts = candidates[0].get("content", {}).get("parts", [])
                    if parts:
                        text = parts[0].get("text", "").strip()
                        if text:
                            return text
        except (HTTPError, URLError, Exception) as e:
            # Fall back to verified structured local template
            pass

    # Verified Local fallback response (offline & test-safe)
    # If context is already structured, return context directly with expert note
    if language == "ta":
        return f"{context}\n\n⚠️ தேவைப்பட்டால் உங்கள் பகுதி பட்டு வளர்ச்சித்துறை கள அலுவலரை அணுகவும்."
    return f"{context}\n\n⚠️ For on-field assistance, consult your local sericulture extension officer."
