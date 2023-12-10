# llm_py
 Examples of large language model applications using streamlit and Haystack, Hugging Face, and LangChain.

## Haystack

### `DocuSeeker.py` (Enterprise Document Search Engine)
- **Elasticsearch Integration:** Manages and queries documents.
- **Redis Caching:** Efficient data retrieval.
- **Streamlit UI:** User-friendly search interface.
- **OpenAI GPT-4 Enhancement:** Improves search query results.
- **Asynchronous Operations:** Enhances performance with asynchronous searches.
### Usage
- **DocuSeeker.py:** Users input search queries and receive relevant document results.

### `FAQPipeline.py` (Streamlit-based Question Answering Application; using COVID-19 data as an example)
- **Elasticsearch Document Store:** Efficient storage and retrieval of FAQ data.
- **Embedding Retriever with MiniLM:** Utilizes sentence-transformers for semantic search.
- **Streamlit Interface:** Interactive web app for querying COVID-19 FAQs.
- **FAQ Pipeline:** Integrates retriever with Streamlit for real-time answers.
- **Error Handling:** Robust user input validation and error management.
### Usage
- **COVID-19 FAQ Bot:** Users can ask questions about COVID-19 and get instant answers.


## Hugging face

### `HuggingFaceExplorer.py` - Hugging Face Model Management Tool
- **Leaderboard Access:** Retrieves top models based on downloads from Hugging Face.
- **Dynamic Filtering and Sorting:** Customizable sorting and filtering of model data.
- **Model Download:** Direct download functionality for specific Hugging Face models.
- **Search Integration:** Ability to search for models based on specific criteria.
- **Robust Error Handling:** Catches and handles potential errors efficiently.
### Usage
- **ModelManager:** Users can view, filter, sort, download, and search for AI models from Hugging Face's expansive library.

### `TranslationAssistant.py` - (Real-time Language Translation Tool)
- **Translation Pipeline:** Helsinki-NLP models from Hugging Face.
- **Streamlit Interface:** Intuitive UI for language selection and text input.
- **Multi-language Support:** Translates between languages like English, Spanish, French, etc.
- **Real-time Translation:** Instant text translation with status feedback.
- **Error Handling:** Logs translation failures.
- **Feedback Mechanism:** User input and suggestions.
- **Session Management:** Tracks user interactions.
### Usage
- **TranslationAssistant.py:** Users select languages, input text, and receive translations.


## LangChain

### `VirtualAssistant.py` (Advanced Virtual Assistant)
- **LangChain Integration:** Generates contextual responses.
- **OpenAI API Key Management:** Secure API key access.
- **Dynamic Context Handling:** Session-based context history.
- **Input Sanitization:** Ensures security of user inputs.
- **Streamlit Interface:** User-friendly front-end for queries and responses.
- **Error Logging:** Troubleshooting and application integrity.
### Usage
- **VirtualAssistant.py:** Users input queries, receive contextual responses, and manage session history.
