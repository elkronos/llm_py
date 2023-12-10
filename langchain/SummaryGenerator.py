import streamlit as st
import asyncio
import re
from langchain import OpenAI
from langchain.docstore.document import Document
from langchain.text_splitter import CharacterTextSplitter
from langchain.chains.summarize import load_summarize_chain
import tiktoken
import PyPDF2

# Constants and Configuration
MODEL_NAME = "gpt-3.5-turbo"
CHAIN_TYPE = 'map_reduce'

# Streamlit app setup
st.set_page_config(page_title='🦜🔗 Text Summarization App')
st.title('🦜🔗 Text Summarization App')

# Pre-processing function
def preprocess_text(text):
    # Remove extra spaces, special characters, etc.
    text = re.sub(r'\s+', ' ', text)  # Remove extra whitespace
    text = re.sub(r'[^\w\s]', '', text)  # Remove special characters
    return text

# Post-processing function
def postprocess_summary(summary):
    # Implement any post-processing steps here
    summary = summary.strip()  # Remove leading/trailing whitespace
    # Add any additional post-processing as required
    return summary

# Function to generate summarized response asynchronously
async def generate_response_async(txt, api_key, summarization_style, summarization_length):
    try:
        llm = OpenAI(temperature=0, openai_api_key=api_key)
        text_splitter = CharacterTextSplitter.from_tiktoken_encoder(MODEL_NAME)
        texts = text_splitter.split_text(preprocess_text(txt))
        docs = [Document(page_content=t) for t in texts]
        chain = load_summarize_chain(llm, chain_type=CHAIN_TYPE, style=summarization_style, length=summarization_length)
        summary = await asyncio.wrap_future(chain.run(docs))
        return postprocess_summary(summary)
    except Exception as e:
        return str(e)

# Function to read uploaded file content
def read_uploaded_file(uploaded_file):
    if uploaded_file is not None:
        if uploaded_file.name.endswith('.txt'):
            return uploaded_file.read().decode('utf-8')
        elif uploaded_file.name.endswith('.pdf'):
            try:
                with open(uploaded_file, 'rb') as f:
                    pdf_reader = PyPDF2.PdfFileReader(f)
                    text = [pdf_reader.getPage(i).extractText() for i in range(pdf_reader.numPages)]
                return ' '.join(text)
            except Exception as e:
                return f"Error reading PDF file: {e}"
    return None

# Streamlit app setup for file upload
st.subheader('Upload your document')
uploaded_file = st.file_uploader('Choose a file', type=['txt', 'pdf'])
if uploaded_file is not None:
    file_content = read_uploaded_file(uploaded_file)
    if file_content:
        # Process the file content
        with st.spinner('Processing the uploaded document...'):
            response = asyncio.run(generate_response_async(file_content, st.session_state.api_key, 'default_style', 'default_length'))
            st.session_state.last_response = response
            st.info(st.session_state.last_response)

# Cache the responses
@st.cache(allow_output_mutation=True)
def cached_response(txt, api_key, style, length):
    return generate_response_async(txt, api_key, style, length)

# Form for text input and API key
with st.form('summarize_form', clear_on_submit=False):
    if st.session_state.api_key is None:
        st.session_state.api_key = st.text_input('OpenAI API Key', type='password')
    summarization_style = st.selectbox('Select Summarization Style', ['default_style', 'other_styles'])
    summarization_length = st.selectbox('Select Summarization Length', ['default_length', 'other_lengths'])

    submitted = st.form_submit_button('Submit')
    if submitted and st.session_state.api_key.startswith('sk-'):
        with st.spinner('Calculating...'):
            response = asyncio.run(cached_response(txt_input, st.session_state.api_key, summarization_style, summarization_length))
            st.session_state.last_response = response

# Display and save results
if 'last_response' in st.session_state and st.session_state.last_response:
    st.info(st.session_state.last_response)
    with open("summary.txt", "w") as file:
        file.write(st.session_state.last_response)
    st.download_button('Download Summary', 'summary.txt', 'summary.txt')
