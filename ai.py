import requests
import os

CLAUDE_API_KEY = os.getenv("CLAUDE_API_KEY")

def get_ai_response(question, temperature, humidity, heat_index, pm25):
    prompt = f"""
    You are AirGuard, an AI assistant that gives personalized, concise advice 
    for people with asthma or allergies based on air conditions.

    Current readings:
    - Temperature: {temperature}°F
    - Humidity: {humidity}%
    - Heat Index: {heat_index}°F
    - PM2.5: {pm25} μg/m³

    User question or advice request: "{question}"

    Respond with one or two actionable sentences.
    """

    response = requests.post(
        "https://api.anthropic.com/v1/messages",
        headers={
            "x-api-key": CLAUDE_API_KEY,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json"
        },
        json={
            "model": "claude-haiku-4-5-20251001",
            "max_tokens": 150,
            "messages": [{"role": "user", "content": prompt}]
        }
    )

    try:
        data = response.json()
        return data["content"][0]["text"]
    except Exception as e:
        print("Error with Claude API:", e, response.text)
        return "Sorry, AirGuard couldn't fetch advice right now."
