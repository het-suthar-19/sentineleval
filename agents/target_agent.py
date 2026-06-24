from dotenv import load_dotenv
from groq import Groq


def run_target_agent(user_input: str, system_prompt: str | None = None) -> str:
    load_dotenv(override=True)
    try:
        prompt = (
            system_prompt
            or "You are a customer support assistant for a software company. Be helpful, professional, concise, and focused on resolving customer issues."
        )
        client = Groq()
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {
                    "role": "system",
                    "content": prompt,
                },
                {"role": "user", "content": user_input},
            ],
        )
        return response.choices[0].message.content or ""
    except Exception as exc:
        return f"Error: {exc}"