# services/gemini_service.py

import os
import json
from google import genai
from google.genai.types import GenerateContentConfig

def extract_query_details(message):

    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        raise Exception("GEMINI_API_KEY not found in environment variables.")

    client = genai.Client(api_key=api_key)

    prompt = f"""
    Extract:
    - intent
    - city
    - year

    Return ONLY valid JSON.
    Do not explain.

    User Query: "{message}"
    """

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
            config=GenerateContentConfig(
                temperature=0
            )
        )

        return json.loads(response.text)

    except Exception as e:
        print("Gemini Error:", e)
        return None