import streamlit as st
import youtube_assistant_helper as yah


def main():
    st.set_page_config(page_title="Youtube Assistant", page_icon="🤖")
    st.title("Youtube Assistant")

    with st.sidebar:
        with st.form(key="my_form"):
            youtube_video_url = st.text_input(
                label="Enter a youtube video url", max_chars=150
            )
            query = st.text_area(
                label="Ask me about the video?", max_chars=150, key="query"
            )

            answer_language = st.selectbox(
                label="Anwer language",
                options=[
                    "English",
                    "Frensh",
                    "Arabic",
                ],
            )

            model = st.selectbox(
                label="Select llm model",
                options=[
                    "gpt-4-1106-preview",
                    "gpt-4",
                    "gpt-3.5-turbo",
                ],
            )

            temperature = st.slider(
                label="Select temperature",
                min_value=0.0,
                max_value=1.0,
                step=0.1,
                value=0.7,
            )

            submit_button = st.form_submit_button(label="Submit")

    if query and youtube_video_url:
        with st.spinner("Wait for it..."):
            db = yah.create_vector_db_from_youtube_url(youtube_video_url)
            response, docs = yah.get_response_from_query(
                db,
                query,
                answer_language=answer_language,
                model=model,
                temperature=temperature,
            )

            st.subheader("Answer:")
            st.markdown(response)


if __name__ == "__main__":
    main()
