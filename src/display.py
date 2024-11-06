import streamlit as st


def display_user_line():
    st.markdown("---")


def display_user_input(user_input):
    with st.chat_message("user"):
        st.write(user_input)


def display_ai_reply(ai_character, reply):
    with st.chat_message(ai_character):
        st.write(reply)


def display_ai_interaction(ai_character, reply):
    _, col = st.columns([1, 9])
    with col.chat_message(ai_character):
        st.write(f"{reply}")


def display_posts(posts):
    for post in posts:
        with st.expander(f"查看话题：{post['timestamp']}"):
            display_user_input(post["content"])
            for reply in post["ai_replies"]:
                display_user_line()
                display_ai_reply(reply["character"], reply["reply"])
                for interaction in reply.get("interactions", []):
                    display_ai_interaction(
                        interaction["character"], interaction["reply"]
                    )
