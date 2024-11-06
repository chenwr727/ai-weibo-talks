from openai import OpenAI

from src.config_loader import load_config

config = load_config()
client = OpenAI(
    api_key=config["openai"]["api_key"], base_url=config["openai"]["base_url"]
)
model = config["openai"]["model"]


def get_chat_completion(messages):
    if not isinstance(messages, list) or not messages:
        raise ValueError("messages must be a non-empty list")

    try:
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            max_tokens=100,
            temperature=0.9,
        )

        if (
            not response.choices
            or not hasattr(response.choices[0], "message")
            or not hasattr(response.choices[0].message, "content")
        ):
            raise ValueError("Unexpected response format")

        return response.choices[0].message.content.strip()

    except Exception as e:
        print(f"An error occurred: {e}")
        return "Sorry, I am busy now"
