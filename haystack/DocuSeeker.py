import os
import logging
import asyncio
import openai
import streamlit as st
from typing import Optional
from haystack.document_stores import ElasticsearchDocumentStore
from haystack.nodes import BM25Retriever
from haystack.pipelines import DocumentSearchPipeline
from elasticsearch import Elasticsearch
from redis import Redis
from redis_cache import RedisCache
from decouple import config

# Logging Configuration
logging.basicConfig(level=logging.INFO)

# Configuration and Initialization Classes
class Config:
    """Class for managing environment configurations."""
    @staticmethod
    def get_env_variable(name: str, default: Optional[str] = None) -> str:
        return config(name, default=default)

class ServiceInitializer:
    """Class for initializing external services like Elasticsearch and Redis."""
    @staticmethod
    def init_elasticsearch() -> ElasticsearchDocumentStore:
        host = Config.get_env_variable('ELASTICSEARCH_HOST', 'localhost')
        username = Config.get_env_variable('ELASTICSEARCH_USERNAME', '')
        password = Config.get_env_variable('ELASTICSEARCH_PASSWORD', '')
        use_ssl = Config.get_env_variable('ELASTICSEARCH_USE_SSL', 'True') == 'True'
        verify_certs = Config.get_env_variable('ELASTICSEARCH_VERIFY_CERTS', 'True') == 'True'
        return ElasticsearchDocumentStore(host=host,
                                          username=username,
                                          password=password,
                                          index="document",
                                          client=Elasticsearch(
                                              hosts=[host],
                                              http_auth=(username, password),
                                              use_ssl=use_ssl,
                                              verify_certs=verify_certs
                                          ))

    @staticmethod
    def init_redis() -> RedisCache:
        host = Config.get_env_variable('REDIS_HOST', 'localhost')
        return RedisCache(redis_client=Redis(host=host))

# Streamlit UI Enhancements
def display_search_interface() -> Optional[str]:
    """Displays the Streamlit UI for document search."""
    st.title("Enterprise Document Search Engine")
    query = st.text_input("Enter your search query:")
    if st.button("Search"):
        return query
    return None

# OpenAI LLM Query Processing
def process_query_with_llm(query: str) -> str:
    """
    Enhances the search query using OpenAI's GPT-4.
    """
    openai.api_key = Config.get_env_variable('OPENAI_API_KEY')
    try:
        response = openai.Completion.create(
            engine="text-davinci-003",  # or another appropriate engine
            prompt=f"Enhance this search query for better results: '{query}'",
            max_tokens=50
        )
        return response.choices[0].text.strip()
    except Exception as e:
        logging.error(f"Error in processing query with LLM: {e}")
        return query  # Fallback to the original query in case of any error

# Asynchronous Operations
async def async_search(query: str, pipeline: DocumentSearchPipeline) -> dict:
    """Perform asynchronous document search."""
    enhanced_query = process_query_with_llm(query)
    return await asyncio.to_thread(
        lambda: pipeline.run(query=enhanced_query, params={"Retriever": {"top_k": 10}})
    )

# Main Application
def main():
    # Initialize services
    document_store = ServiceInitializer.init_elasticsearch()
    cache = ServiceInitializer.init_redis()

    # Initialize retriever with caching
    retriever = BM25Retriever(document_store=document_store, cache=cache)

    # Initialize pipeline
    pipeline = DocumentSearchPipeline(retriever)

    # Streamlit interface
    query = display_search_interface()

    if query:
        try:
            # Execute search asynchronously with caching
            result = asyncio.run(async_search(query, pipeline))

            # Display results with pagination
            page_number = st.number_input(label="Page Number", min_value=1, value=1)
            start = (page_number - 1) * 10
            end = start + 10

            for i, doc in enumerate(result["documents"][start:end], start=start):
                st.write(f"**Document {i+1}:** {doc.content}")

        except Exception as e:
            logging.error("An error occurred", exc_info=True)
            st.error(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()