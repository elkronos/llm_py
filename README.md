# llm_py
 Examples of large language model applications using streamlit and Haystack, Hugging Face, and LangChain.

#### DocuSeeker.py (Enterprise Document Search Engine)
Located in the 'haystack' sub-folder, DocuSeeker.py is an advanced document search application integrating Elasticsearch, Redis, Streamlit, and OpenAI's GPT-4.
- **Elasticsearch Integration:** Manages and queries documents.
- **Redis Caching:** Efficient data retrieval.
- **Streamlit UI:** User-friendly search interface.
- **OpenAI GPT-4 Enhancement:** Improves search query results.
- **Asynchronous Operations:** Enhances performance with asynchronous searches.

#### TranslationAssistant.py (Real-time Language Translation Tool)
Housed in the 'hugging face' folder, TranslationAssistant.py leverages Hugging Face's Transformers for instantaneous translations.
- **Translation Pipeline:** Helsinki-NLP models from Hugging Face.
- **Streamlit Interface:** Intuitive UI for language selection and text input.
- **Multi-language Support:** Translates between languages like English, Spanish, French, etc.
- **Real-time Translation:** Instant text translation with status feedback.
- **Error Handling:** Logs translation failures.
- **Feedback Mechanism:** User input and suggestions.
- **Session Management:** Tracks user interactions.

#### VirtualAssistant.py (Advanced Virtual Assistant)
Situated in the 'LangChain' folder, VirtualAssistant.py acts as a virtual assistant using LangChain and OpenAI's GPT models.
- **LangChain Integration:** Generates contextual responses.
- **OpenAI API Key Management:** Secure API key access.
- **Dynamic Context Handling:** Session-based context history.
- **Input Sanitization:** Ensures security of user inputs.
- **Streamlit Interface:** User-friendly front-end for queries and responses.
- **Error Logging:** Troubleshooting and application integrity.

#### Usage
- **DocuSeeker.py:** Users input search queries and receive relevant document results.
- **TranslationAssistant.py:** Users select languages, input text, and receive translations.
- **VirtualAssistant.py:** Users input queries, receive contextual responses, and manage session history.

Each application is designed with user experience and performance in mind, leveraging modern Python libraries and frameworks.
