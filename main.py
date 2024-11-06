import random
from datetime import datetime

import streamlit as st

from src.config_loader import load_config
from src.display import (
    display_ai_interaction,
    display_ai_reply,
    display_posts,
    display_user_input,
    display_user_line,
)
from src.storage import load_data, save_data
from src.utils import ai_to_ai_reply, choose_ai_character, generate_ai_reply

config = load_config()

st.set_page_config(page_title=config["app"]["title"])
st.title(config["app"]["title"])

hot_topics = config["app"]["hot_topics"]
if "posts" not in st.session_state:
    st.session_state["posts"] = load_data()
if "current_topic" not in st.session_state:
    st.session_state["current_topic"] = hot_topics[0]
for topic in hot_topics:
    if topic not in st.session_state["posts"]:
        st.session_state["posts"][topic] = []

with st.sidebar:
    st.header("热门话题")
    selected_topic = st.selectbox("选择一个话题", hot_topics)

    st.header("回复次数")
    reply_count_min = st.number_input(
        "最少回复次数", min_value=1, max_value=10, value=3
    )
    reply_count_max = st.number_input(
        "最多回复次数", min_value=reply_count_min, max_value=10, value=5
    )

    st.header("交互次数")
    comment_count_min = st.number_input(
        "最少交互次数", min_value=1, max_value=10, value=1
    )
    comment_count_max = st.number_input(
        "最多交互次数", min_value=comment_count_min, max_value=10, value=3
    )


if selected_topic != st.session_state["current_topic"]:
    st.session_state["current_topic"] = selected_topic

if "user_input" not in st.session_state:
    st.session_state.user_input = ""

user_inputs = config["app"]["user_inputs"]
user_input_columns = config["app"]["user_input_columns"]
for i in range(0, len(user_inputs), user_input_columns):
    cols = st.columns(user_input_columns)
    for j in range(user_input_columns):
        index = i + j
        if index <= len(user_inputs) - 1:
            if cols[j].button(user_inputs[index]):
                st.session_state.user_input = user_inputs[index]

user_input = st.text_input(
    "你想说点什么？", value=st.session_state.user_input, max_chars=140
)
posts = st.session_state["posts"][selected_topic].copy()
if st.button("发送") and user_input:
    new_post = {
        "content": user_input,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "ai_replies": [],
    }
    with st.expander(f"查看话题：{new_post['timestamp']}", expanded=True):
        display_user_input(new_post["content"])
        used_ai_names = set()
        for _ in range(random.randint(reply_count_min, reply_count_max)):
            display_user_line()
            ai_character = choose_ai_character(used_ai_names)
            if ai_character:
                used_ai_names.add(ai_character["name"])
                ai_reply = generate_ai_reply(
                    user_input, ai_character, selected_topic.strip("#")
                )
                display_ai_reply(ai_reply["character"], ai_reply["reply"])

                used_ai_names_replay = {ai_reply["character"]}
                interaction_count = random.randint(comment_count_min, comment_count_max)
                for _ in range(interaction_count):
                    interacting_ai = choose_ai_character(used_ai_names_replay)
                    if not interacting_ai:
                        break
                    last_reply = (
                        ai_reply["interactions"][-1]["reply"]
                        if ai_reply["interactions"]
                        else ai_reply["reply"]
                    )
                    interaction = ai_to_ai_reply(
                        user_input,
                        last_reply,
                        interacting_ai,
                        selected_topic.strip("#"),
                    )
                    interaction = {
                        "character": interacting_ai["name"],
                        "reply": interaction,
                        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    }
                    display_ai_interaction(
                        interaction["character"], interaction["reply"]
                    )
                    ai_reply["interactions"].append(interaction)
                new_post["ai_replies"].append(ai_reply)

        st.session_state["posts"][selected_topic].insert(0, new_post)
        save_data(st.session_state["posts"])

display_posts(posts)
