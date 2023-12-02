import streamlit as st
import time


USER_AVATAR = "👱‍♂️"
ASSISTANT_AVATAR = "🤖"


def main():
    st.set_page_config(page_title="Chatbot", page_icon="🤖")
    st.title("Chatbot")

    display_chat_messages_history()

    if user_input := st.chat_input("Your Message ?"):
        st.session_state.chat_history.append({"role": "user", "content": user_input})

        with st.chat_message("user", avatar=USER_AVATAR):
            st.markdown(user_input)

        with st.chat_message("assistant", avatar=ASSISTANT_AVATAR):
            assistant_message_placeholder = st.empty()
            assistant_full_response = ""

            with st.spinner("Wait for it..."):
                assistant_response = get_bot_response(user_input)

            for chunk in assistant_response.split():
                assistant_full_response += chunk + " "
                time.sleep(0.05)

                assistant_message_placeholder.markdown(assistant_full_response + "▌")

            assistant_message_placeholder.markdown(assistant_full_response)

        bot_response = get_bot_response(user_input)
        st.session_state.chat_history.append(
            {"role": "assistant", "content": bot_response}
        )


def display_chat_messages_history() -> None:
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    for message in st.session_state.chat_history:
        with st.chat_message(
            message["role"],
            avatar=ASSISTANT_AVATAR if message["role"] == "assistant" else USER_AVATAR,
        ):
            st.markdown(message["content"])


def get_bot_response(user_input: str) -> str:
    time.sleep(2)

    assistant_response = "Echo: " + user_input

    return assistant_response


if __name__ == "__main__":
    main()
