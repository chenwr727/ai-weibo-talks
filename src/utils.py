import random
from datetime import datetime

from src.config_loader import load_config
from src.openai_client import get_chat_completion

config = load_config()
ai_characters = config["ai_characters"]
prompt = config["openai"]["prompt"]


def choose_ai_character(used_ai_names):
    available_ais = [ai for ai in ai_characters if ai["name"] not in used_ai_names]
    return random.choice(available_ais) if available_ais else None


def generate_ai_reply(user_input, ai_character, topic):
    messages = [
        {
            "role": "system",
            "content": f"{prompt}你是{ai_character['name']}，性格特点是：{ai_character['style']}。请用口语化、真实的方式回应用户的话，同时要紧扣'{topic}'这个话题。字数控制在50字以内。",
        },
        {"role": "user", "content": user_input},
    ]
    return {
        "character": ai_character["name"],
        "reply": get_chat_completion(messages),
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "interactions": [],
    }


def ai_to_ai_reply(user_input, previous_reply, ai_character, topic):
    messages = [
        {
            "role": "system",
            "content": f"{prompt}你是{ai_character['name']}，个性特点是：{ai_character['style']}。现在你需要用轻松、口语化的方式回应另一个AI的回复，同时不忘紧扣'{topic}'这个话题。即便参考对方的回复，仍要结合用户的原始话题，使内容不脱离。字数控制在50字以内。",
        },
        {
            "role": "user",
            "content": f"用户最初说：{user_input}\n另一个AI说：{previous_reply}",
        },
    ]
    return get_chat_completion(messages)
