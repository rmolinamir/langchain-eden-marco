import streamlit
import streamlit_chat
from langchain import hub
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains.history_aware_retriever import create_history_aware_retriever
from langchain.chains.retrieval import create_retrieval_chain
from langchain_community.vectorstores import FAISS
from langchain_ollama import ChatOllama, OllamaEmbeddings


def answer_question(question: str) -> dict[str, str]:
    """
    Answer a question using the LangChain library.
    """
    embeddings = OllamaEmbeddings(model="nomic-embed-text")

    vectorstore = FAISS.load_local(
        "chapter_6_faiss_index", embeddings, allow_dangerous_deserialization=True
    )
    llm = ChatOllama(model="llama3.1:8b")

    retrieval_qa_chat_prompt = hub.pull("langchain-ai/retrieval-qa-chat")
    combine_docs_chain = create_stuff_documents_chain(
        llm=llm, prompt=retrieval_qa_chat_prompt
    )

    rephrase_prompt = hub.pull("langchain-ai/chat-langchain-rephrase")
    history_aware_retriever = create_history_aware_retriever(
        llm=llm,
        prompt=rephrase_prompt,
        retriever=vectorstore.as_retriever(),
    )

    retrieval_chain = create_retrieval_chain(
        retriever=history_aware_retriever, combine_docs_chain=combine_docs_chain
    )

    response = retrieval_chain.invoke(
        input={
            "input": question,
            "chat_history": streamlit.session_state.chat_history,
        }
    )

    return {
        "query": response["input"],
        "result": response["answer"],
        "source_documents": response["context"],
    }


def format_sources(sources: set[str]) -> str:
    """
    Format the sources from the answer_question function.
    """
    sources_list = list(sources)
    sources_list.sort()
    return "\n".join(f"{i + 1}. {source}" for i, source in enumerate(sources_list))


def format_response(answer: dict[str, str]) -> str:
    """
    Format the response from the answer_question function.
    """
    sources = {doc.metadata["source"] for doc in answer.get("source_documents")}
    return f"{answer.get('result')}\n\nSources:\n{format_sources(sources)}"


# Set Matrix/hacker CLI theme
streamlit.set_page_config(
    page_title="LangGPT - Matrix CLI",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS for hacker CLI theme with sticky input and link wrapping
streamlit.markdown(
    """
    <style>
    /* Main theme */
    html, body, [data-testid="stAppViewContainer"] {
        background-color: #000 !important;
        color: #00ff00 !important;
        font-family: 'Fira Mono', 'Consolas', monospace !important;
    }
    /* Chat messages */
    .stChatMessage, .stChatMessageContent {
        background-color: #181c1b !important;
        color: #00ff00 !important;
        border: 1px solid #00ff00 !important;
        font-family: 'Fira Mono', 'Consolas', monospace !important;
    }
    /* Sidebar */
    .stSidebar, .stSidebarContent {
        background-color: #111 !important;
        color: #00ff00 !important;
        border-right: 2px solid #00ff00 !important;
    }
    /* Text elements */
    .stMarkdown, .stMetric, .stHeader, .stSubheader {
        color: #00ff00 !important;
        font-family: 'Fira Mono', 'Consolas', monospace !important;
    }
    /* Links */
    a {
        color: #00ff00 !important;
        text-decoration: underline;
        word-break: break-all !important;
        white-space: pre-wrap !important;
        overflow-wrap: break-word !important;
    }
    /* Input container at bottom */
    [data-testid="stForm"] {
        position: fixed !important;
        bottom: 0 !important;
        left: 0 !important;
        right: 0 !important;
        background: #000 !important;
        padding: 1rem !important;
        z-index: 999999 !important;
        border-top: 2px solid #00ff00 !important;
    }
    /* Input styling */
    .stTextInput input {
        background-color: #000 !important;
        color: #00ff00 !important;
        border: 1.5px solid #00ff00 !important;
        font-family: 'Fira Mono', 'Consolas', monospace !important;
        padding: 0.5rem !important;
    }
    /* Add padding to main content to prevent overlap with fixed input */
    .main > div {
        padding-bottom: 100px !important;
    }
    /* Hide default streamlit branding */
    #MainMenu, footer, header {display: none !important;}
    </style>
    """,
    unsafe_allow_html=True,
)

streamlit.header("LangGPT")

# Initialize session state
if (
    "questions_history" not in streamlit.session_state
    or "answers_history" not in streamlit.session_state
    or "chat_history" not in streamlit.session_state
):
    streamlit.session_state.questions_history = []
    streamlit.session_state.answers_history = []
    streamlit.session_state.chat_history = []

# Display chat history
if streamlit.session_state.questions_history:
    for question, answer in zip(
        streamlit.session_state.questions_history,
        streamlit.session_state.answers_history,
        strict=False,
    ):
        streamlit_chat.message(question, is_user=True)
        streamlit_chat.message(answer)

# Add sidebar with conversation stats
with streamlit.sidebar:
    streamlit.markdown("### Conversation Stats")
    streamlit.markdown("---")

    # Calculate stats
    total_messages = len(streamlit.session_state.get("questions_history", []))
    total_words = sum(
        len(q.split()) for q in streamlit.session_state.get("questions_history", [])
    )

    # Display stats
    streamlit.metric("Total Messages", total_messages)
    streamlit.metric("Total Words", total_words)

    if total_messages > 0:
        avg_words = total_words / total_messages
        streamlit.metric("Avg. Words per Message", f"{avg_words:.1f}")

    streamlit.markdown("---")
    streamlit.markdown("### Model Info")
    streamlit.markdown("🤖 llama3.1:8b")
    streamlit.markdown("📚 FAISS Vector Store")

# Input form at the bottom
with streamlit.form(key="chat_form", clear_on_submit=True):
    cols = streamlit.columns([0.05, 0.95])
    with cols[0]:
        streamlit.markdown("$", unsafe_allow_html=True)
    with cols[1]:
        prompt = streamlit.text_input(
            "Message",
            key="user_input",
            label_visibility="collapsed",
            placeholder="Type your question and press Enter...",
        )
    submit = streamlit.form_submit_button(
        label="Send", type="primary", use_container_width=True
    )

# Process the input
if submit and prompt:
    with streamlit.spinner("Thinking..."):
        answer = answer_question(prompt)
        response = format_response(answer)

        # Update session state
        streamlit.session_state.questions_history.append(prompt)
        streamlit.session_state.answers_history.append(response)
        streamlit.session_state.chat_history.append({"role": "user", "content": prompt})
        streamlit.session_state.chat_history.append(
            {"role": "assistant", "content": response}
        )

        # Rerun to update the UI
        streamlit.rerun()
