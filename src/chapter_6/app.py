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


# Configure the Streamlit page with a clean, modern look
streamlit.set_page_config(
    page_title="LangGPT",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        "Get Help": None,
        "Report a bug": None,
        "About": "# LangGPT\nA modern AI chat interface powered by LangChain",
    },
)

# Initialize session state
if (
    "questions_history" not in streamlit.session_state
    or "answers_history" not in streamlit.session_state
    or "chat_history" not in streamlit.session_state
):
    streamlit.session_state.questions_history = []
    streamlit.session_state.answers_history = []
    streamlit.session_state.chat_history = []

# Create a clean layout with columns
main_container = streamlit.container()
with main_container:
    # Title with custom styling
    col1, col2 = streamlit.columns([6, 1])
    with col1:
        streamlit.title("LangGPT")
    with col2:
        streamlit.image(
            "https://api.dicebear.com/7.x/bottts/svg?seed=langgpt", width=64
        )

    # Chat container with improved spacing
    chat_container = streamlit.container()
    with chat_container:
        if streamlit.session_state.questions_history:
            for question, answer in zip(
                streamlit.session_state.questions_history,
                streamlit.session_state.answers_history,
                strict=False,
            ):
                streamlit_chat.message(
                    question, is_user=True, avatar_style="adventurer"
                )
                streamlit_chat.message(answer, avatar_style="bottts")
        else:
            streamlit.info("👋 Hello! Ask me anything about the documentation.")

# Sidebar with modern styling
with streamlit.sidebar:
    streamlit.title("Chat Info")

    # Stats in a clean card layout
    with streamlit.expander("📊 Conversation Stats", expanded=True):
        total_messages = len(streamlit.session_state.get("questions_history", []))
        total_words = sum(
            len(q.split()) for q in streamlit.session_state.get("questions_history", [])
        )

        col1, col2 = streamlit.columns(2)
        with col1:
            streamlit.metric("Messages", total_messages)
        with col2:
            streamlit.metric("Words", total_words)

        if total_messages > 0:
            avg_words = total_words / total_messages
            streamlit.metric("Avg. Words/Message", f"{avg_words:.1f}")

    # Model info in a clean card
    with streamlit.expander("🤖 Model Info", expanded=True):
        streamlit.markdown("""
        - **Model**: llama3.1:8b
        - **Embeddings**: FAISS Vector Store
        - **Framework**: LangChain
        """)

    # Add a nice divider
    streamlit.divider()

# Modern input form at the bottom
with streamlit.container():
    streamlit.divider()
    with streamlit.form(key="chat_form", clear_on_submit=True):
        col1, col2 = streamlit.columns([6, 1])
        with col1:
            prompt = streamlit.text_input(
                "Message",
                key="user_input",
                label_visibility="collapsed",
                placeholder="Ask me anything...",
            )
        with col2:
            submit = streamlit.form_submit_button(
                label="Send",
                type="primary",
                use_container_width=True,
            )

# Process the input with improved feedback
if submit and prompt:
    with streamlit.status("Thinking...") as status:
        # Show a progress message
        status.update(label="Searching documentation...", state="running")

        # Get the answer
        answer = answer_question(prompt)
        response = format_response(answer)

        # Update status
        status.update(label="Processing response...", state="running")

        # Update session state
        streamlit.session_state.questions_history.append(prompt)
        streamlit.session_state.answers_history.append(response)
        streamlit.session_state.chat_history.append({"role": "user", "content": prompt})
        streamlit.session_state.chat_history.append(
            {"role": "assistant", "content": response}
        )

        # Complete status
        status.update(label="Done!", state="complete")

    # Rerun to update the UI
    streamlit.rerun()
