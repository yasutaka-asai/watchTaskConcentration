import os
from openai import OpenAI

def test_api_connection():
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("OPENAI_API_KEY environment variable not set.")
        return

    client = OpenAI(api_key=api_key)
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": "Hello"}]
        )
        print(f"API connection successful. Response: {response.choices[0].message.content}")
    except Exception as e:
        print(f"API connection failed: {e}")

if __name__ == "__main__":
    test_api_connection()
