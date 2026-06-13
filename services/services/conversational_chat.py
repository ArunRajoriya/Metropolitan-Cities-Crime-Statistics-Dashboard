import os
import requests
import json

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"


def generate_chat_reply(message: str) -> str:
    """
    Generate a conversational fallback response for general questions.
    Used when structured routing cannot interpret the request.
    """

    safe_message = (message or "").strip()

    if not safe_message:
        return "Please ask a question and I will do my best to help."

    # Deterministic local fallback (guaranteed response)
    fallback = (
        "I can help with crime statistics, trends, city comparisons, "
        "juvenile and age-group analysis, and general guidance. "
        f"You asked: '{safe_message}'. "
        "Please share more details if you want a dataset-driven breakdown."
    )

    # If no API key → always return deterministic fallback
    if not GROQ_API_KEY:
        return fallback

    try:
        response = requests.post(
            GROQ_URL,
            headers={
                "Authorization": f"Bearer {GROQ_API_KEY}",
                "Content-Type": "application/json",
            },
            json={
                "model": "llama-3.1-8b-instant",
                "messages": [
                    {
                        "role": "system",
                        "content": (
                            "You are a helpful AI assistant for a crime analytics dashboard. "
                            "Answer clearly and concisely. "
                            "If the user asks outside crime analytics, still provide a useful response."
                        ),
                    },
                    {"role": "user", "content": safe_message},
                ],
                "temperature": 0.4,
                "max_tokens": 300,
            },
            timeout=10,
        )

        if response.status_code != 200:
            return fallback

        try:
            result = response.json()
        except json.JSONDecodeError:
            return fallback

        choices = result.get("choices")
        if not choices:
            return fallback

        content = choices[0].get("message", {}).get("content", "").strip()

        return content if content else fallback

    except requests.Timeout:
        return "The AI service took too long to respond. Please try again."

    except requests.RequestException:
        return fallback

    except Exception:
        return fallback