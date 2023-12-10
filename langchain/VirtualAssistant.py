from langchain.chains import Chain
from langchain.links import OpenAICompletion
import streamlit as st
import os
import logging
import re

# Configure logging
logging.basicConfig(filename='error.log', level=logging.ERROR)

def get_openai_api_key():
    """
    Retrieves the OpenAI API key from environment variables.
    Raises an error if the key is not found.
    """
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise EnvironmentError("OPENAI_API_KEY environment variable not set.")
    return api_key

openai_api_key = get_openai_api_key()
openai_link = OpenAICompletion(api_key=openai_api_key)
chain = Chain(links=[openai_link])

def get_context(limit=6):
    """
    Retrieves a portion of the context from the session state.
    The size of the context is limited to avoid exceeding character limits.

    Args:
    limit (int): The maximum number of context pairs to retrieve.
    """
    limit = min(limit, len(st.session_state.get('context', [])) // 2)
    return "\n".join(entry[:500] for entry in st.session_state['context'][-limit*2:])

def append_to_context(user_input, assistant_response):
    """
    Appends the user input and assistant response to the session context.
    Ensures the context does not exceed a predefined size.

    Args:
    user_input (str): The user's input text.
    assistant_response (str): The assistant's response text.
    """
    sanitized_input = sanitize_input(user_input)
    sanitized_response = sanitize_input(assistant_response)
    st.session_state['context'] += [sanitized_input, sanitized_response]
    if len(st.session_state['context']) > 20:
        st.session_state['context'] = st.session_state['context'][-20:]

def sanitize_input(text):
    """
    Sanitizes the input text to prevent potential security risks.
    This includes escaping HTML special characters and removing harmful patterns.

    Args:
    text (str): The input text to be sanitized.

    Returns:
    str: The sanitized text.
    """
    text = text.replace("<", "&lt;").replace(">", "&gt;")
    harmful_patterns = [r"<script.*?>.*?</script>", r"(DROP|ALTER|INSERT|SELECT|UPDATE|DELETE)\s+.*"]
    for pattern in harmful_patterns:
        text = re.sub(pattern, "", text, flags=re.IGNORECASE)
    max_length = 1000
    return text[:max_length]

def respond_to_query(query, context_limit):
    """
    Generates a response to the user's query using the langchain.
    Handles any exceptions and logs them.

    Args:
    query (str): The user's query.
    context_limit (int): The limit for the context size.

    Returns:
    str: The generated response.
    """
    try:
        context = get_context(context_limit)
        response = chain.run(query, context=context)
        append_to_context(query, response)
        return response
    except Exception as e:
        logging.error(str(e))
        st.error(f"An error occurred. Please check the logs for details.")
        return ""

def main():
    """
    Main function to run the Streamlit application.
    Sets up the UI elements and handles interactions.
    """
    st.title("Advanced Virtual Assistant")

    if 'context' not in st.session_state:
        st.session_state['context'] = []

    user_input = st.text_input("Enter your question:", key="user_input")
    context_limit = st.slider("Context History Size", 3, 10, 6)
    clear_button = st.button("Clear Context")

    if clear_button:
        st.session_state['context'] = []

    if user_input:
        response = respond_to_query(user_input, context_limit)
        st.text_area("Response", value=response, height=100, key="response_area")

    if st.button("View/Edit Context"):
        st.text_area("Edit Context", value="\n".join(st.session_state['context']), height=300, key="context_area")

if __name__ == "__main__":
    main()