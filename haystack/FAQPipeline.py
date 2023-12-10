import os
import streamlit as st
from haystack.document_stores import ElasticsearchDocumentStore
from haystack.nodes import EmbeddingRetriever
from haystack.pipelines import FAQPipeline
from haystack.utils import fetch_archive_from_http
import pandas as pd
import logging

# Configuration and Constants
LOGGING_FORMAT = "%(asctime)s - %(levelname)s - %(name)s -  %(message)s"
LOGGING_LEVEL = logging.INFO
HAYSTACK_LOGGING_LEVEL = logging.INFO

# Load configurations from environment variables or use default values
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2")
USE_GPU = os.getenv("USE_GPU", "True") == "True"
SCALE_SCORE = os.getenv("SCALE_SCORE", "False") == "True"
DATA_URL = os.getenv("DATA_URL", "https://s3.eu-central-1.amazonaws.com/deepset.ai-farm-qa/datasets/documents/small_faq_covid.csv.zip")
DATA_DIR = os.getenv("DATA_DIR", "data/tutorial4")

def setup_logging():
    logging.basicConfig(format=LOGGING_FORMAT, level=LOGGING_LEVEL)
    logger = logging.getLogger("haystack")
    logger.setLevel(HAYSTACK_LOGGING_LEVEL)
    return logger

def create_document_store():
    return ElasticsearchDocumentStore()

def create_retriever(document_store):
    return EmbeddingRetriever(
        document_store=document_store,
        embedding_model=EMBEDDING_MODEL,
        use_gpu=USE_GPU,
        scale_score=SCALE_SCORE,
    )

def fetch_and_process_data(url, output_dir, retriever):
    fetch_archive_from_http(url=url, output_dir=output_dir)
    df = pd.read_csv(f"{output_dir}/small_faq_covid.csv")
    df.fillna(value="", inplace=True)
    df["question"] = df["question"].str.strip().str.lower()
    questions = df["question"].values
    embeddings = retriever.embed_queries(queries=questions)
    df["embedding"] = embeddings.tolist()
    return df.rename(columns={"question": "content"}).to_dict(orient="records")

def index_documents(document_store, documents):
    document_store.write_documents(documents)

def create_faq_pipeline(retriever):
    return FAQPipeline(retriever=retriever)

def validate_user_input(input_str):
    if len(input_str) == 0:
        raise ValueError("Input cannot be empty.")
    return input_str

def streamlit_app(pipe, logger):
    st.title("COVID-19 FAQ Bot")
    user_query = st.text_input("Ask a question about COVID-19")
    if user_query:
        try:
            user_query = validate_user_input(user_query)
            prediction = pipe.run(query=user_query, params={"Retriever": {"top_k": 1}})
            answers = prediction["answers"]
            if answers:
                st.write("Answer:", answers[0].answer)
            else:
                st.write("Sorry, I couldn't find an answer to your question.")
        except Exception as e:
            logger.error(f"Error processing query: {str(e)}")
            st.error("An error occurred: " + str(e))

def main():
    logger = setup_logging()
    document_store = create_document_store()
    retriever = create_retriever(document_store)
    documents = fetch_and_process_data(DATA_URL, DATA_DIR, retriever)
    index_documents(document_store, documents)
    pipe = create_faq_pipeline(retriever)
    streamlit_app(pipe, logger)

if __name__ == "__main__":
    main()