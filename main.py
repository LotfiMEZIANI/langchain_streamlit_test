import streamlit as st
import time

from langchain.agents import AgentExecutor
from langchain.agents.agent_types import AgentType
from langchain_experimental.agents.agent_toolkits import create_csv_agent
from langchain.chat_models import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

USER_AVATAR = "👱‍♂️"
ASSISTANT_AVATAR = "🤖"

USER_AUTHORISATION_LEVEL_1 = "level 1"
USER_AUTHORISATION_LEVEL_2 = "level 2"

docs_authorisation_map = {
    USER_AUTHORISATION_LEVEL_1: ["./info_level1.csv"],
    USER_AUTHORISATION_LEVEL_2: ["./info_level1.csv", "./info_level2.csv"],
}


def main():
    st.set_page_config(page_title="Chatbot", page_icon="🤖")
    st.title("Chatbot")

    user_authorization_level = display_sidebar_and_get_user_authorisation_level()

    if (
        "agent" not in st.session_state
        or user_authorization_level != st.session_state.user_authorization_level
    ):
        initialise_agent(user_authorization_level)

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

        st.session_state.chat_history.append(
            {"role": "assistant", "content": assistant_full_response}
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


def initialise_agent(user_authorisation_level: str) -> None:
    st.session_state.user_authorization_level = user_authorisation_level
    st.session_state.agent = generate_agent(st.session_state.user_authorization_level)


def display_sidebar_and_get_user_authorisation_level() -> str:
    with st.sidebar:
        with st.form(key="my_form"):
            user_authorization_level = st.selectbox(
                label="Select the user's authorization level",
                options=[
                    USER_AUTHORISATION_LEVEL_1,
                    USER_AUTHORISATION_LEVEL_2,
                ],
            )

            if submit_button := st.form_submit_button(label="Submit"):
                st.session_state.chat_history = []

            return user_authorization_level


def generate_agent(authorisation_level: str) -> AgentExecutor:
    return create_csv_agent(
        ChatOpenAI(temperature=0, model="gpt-3.5-turbo-0613"),
        docs_authorisation_map[authorisation_level],
        verbose=True,
        agent_type=AgentType.OPENAI_FUNCTIONS,
    )


def get_bot_response(user_input: str) -> str:
    return st.session_state.agent.run(
        f""" Have a conversation with a human, answering the following questions as best you can for the given cvs 
        file based one the key and the value column. 
        Give direct answer without any explanations or notes.
        Use markdown syntax If you don't know the answer, just say that you don't know.
    
    conversation history:
    {[(message["role"] + ": " + message["content"]) for message in st.session_state.chat_history] }
    ---
    
    question: {user_input}
    """
    )


if __name__ == "__main__":
    main()
