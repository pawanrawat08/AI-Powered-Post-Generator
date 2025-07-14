import streamlit as st
from few_shot import FewShotPosts
from post_generator import generate_post

# Constants for dropdown options
POST_LENGTH_OPTIONS = ["Short", "Medium", "Long"]
LANGUAGE_OPTIONS = ["English", "Hinglish"]


def run_post_generator_app():
    """
    Streamlit app for generating social media posts based on selected topic, length, and language.
    """
    st.subheader("AI-Powered Post Generator")

    # Layout: three side-by-side columns
    col_topic, col_length, col_language = st.columns(3)

    # Initialize tag source using FewShotPosts helper class
    tag_generator = FewShotPosts()
    available_tags = tag_generator.get_tags()

    # Topic selection dropdown
    with col_topic:
        selected_topic = st.selectbox("Select Topic", options=available_tags)

    # Length selection dropdown
    with col_length:
        selected_length = st.selectbox("Select Length", options=POST_LENGTH_OPTIONS)

    # Language selection dropdown
    with col_language:
        selected_language = st.selectbox("Select Language", options=LANGUAGE_OPTIONS)

    # Button to trigger post generation
    if st.button("Generate Post"):
        post_output = generate_post(
            tag=selected_topic,
            length=selected_length,
            language=selected_language
        )
        st.write(post_output)


if __name__ == '__main__':
    run_post_generator_app()
