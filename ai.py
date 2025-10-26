import requests
import os

CLAUDE_API_KEY = os.getenv("CLAUDE_API_KEY")
MODEL = "claude-sonnet-4-5-20250929"

def get_ai_response(question, temperature, humidity, heat_index, pm25):
    prompt = f"""
You are AirGuard, an AI assistant that gives concise, actionable advice
for people with asthma or allergies based on air conditions.

Current readings:
- Temperature: {temperature}°F
- Humidity: {humidity}%
- Heat Index: {heat_index}°F
- PM2.5: {pm25} μg/m³

User question or advice request: "{question}"

Respond in one or two actionable sentences.
"""

    try:
        response = requests.post(
            "https://api.anthropic.com/v1/messages",
            headers={
                "x-api-key": CLAUDE_API_KEY,
                "anthropic-version": "2023-06-01",
                "Content-Type": "application/json"
            },
            json={
                "model": MODEL,
                "messages": [{"role": "user", "content": prompt}],
                "max_tokens": 150
            }
        )

        # Debugging info
        print("Status code:", response.status_code)
        print("Response text:", response.text)

        data = response.json()
        # Claude 4.5 returns the AI text in data["content"][0]["text"]
        return data["content"][0]["text"].strip() or "AI did not return a message."

    except Exception as e:
        print("Error with Claude API:", e, getattr(response, "text", ""))
        return "Sorry, AirGuard couldn't fetch advice right now."
