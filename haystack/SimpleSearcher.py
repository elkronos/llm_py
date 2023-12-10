import streamlit as st
import requests
import json

# Constants for Haystack API Endpoints
HAYSTACK_API_URL = "http://127.0.0.1:8000"

def upload_document(files):
    """Upload documents to Haystack with error handling and validation."""
    responses = []
    for file in files:
        # Add file validation logic here (file type, size, etc.)
        try:
            response = requests.post(
                f"{HAYSTACK_API_URL}/file-upload",
                files={"files": file},
                data={"meta": json.dumps({"filename": file.name})}
            )
            response.raise_for_status()
            responses.append(response.json())
        except requests.RequestException as e:
            responses.append({"error": str(e)})
    return responses

def query_documents(query):
    """Query documents from Haystack with error handling."""
    try:
        response = requests.post(
            f"{HAYSTACK_API_URL}/query",
            headers={"Content-Type": "application/json"},
            data=json.dumps({"query": query})
        )
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        return {"error": str(e)}

def display_results(results):
    """Display search results in a user-friendly format."""
    if results.get("error"):
        st.error(f"Error: {results['error']}")
    else:
        for doc in results.get("documents", []):
            st.write(f"ID: {doc['id']}")
            st.write(f"Content: {doc['content'][:200]}...")
            st.write(f"Score: {doc['score']}")
            st.write("---")

def main():
    st.title("Document Search with Haystack")

    # Document upload section
    st.header("Upload Documents")
    uploaded_files = st.file_uploader("Choose files", accept_multiple_files=True)
    if st.button("Upload Files"):
        if uploaded_files:
            with st.spinner('Uploading...'):
                upload_responses = upload_document(uploaded_files)
                for response in upload_responses:
                    if "error" in response:
                        st.error("Upload failed: " + response["error"])
                    else:
                        st.success("Upload successful: " + str(response))
        else:
            st.warning("Please select files to upload.")

    # Query section
    st.header("Search Documents")
    query = st.text_input("Enter your query")
    if st.button("Search"):
        if query:
            with st.spinner('Searching...'):
                query_response = query_documents(query)
                display_results(query_response)
        else:
            st.warning("Please enter a query to search.")

if __name__ == "__main__":
    main()
