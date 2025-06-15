from langchain import hub
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains.retrieval import create_retrieval_chain
from langchain_community.vectorstores import FAISS
from langchain_ollama import ChatOllama, OllamaEmbeddings


def main() -> None:
    embeddings = OllamaEmbeddings(model="nomic-embed-text")

    vectorstore = FAISS.load_local(
        "chapter_5_faiss_index", embeddings, allow_dangerous_deserialization=True
    )
    llm = ChatOllama(model="llama3.1:8b")

    retrieval_qa_chat_prompt = hub.pull("langchain-ai/retrieval-qa-chat")
    combine_docs_chain = create_stuff_documents_chain(llm, retrieval_qa_chat_prompt)
    retrieval_chain = create_retrieval_chain(
        retriever=vectorstore.as_retriever(), combine_docs_chain=combine_docs_chain
    )

    # Initialize conversation history
    chat_history: list[dict[str, str]] = []

    while True:
        question = input("> Enter a question (or /bye to exit): ")
        if question == "/bye":
            break

        # Add the current question to chat history
        chat_history.append({"role": "user", "content": question})

        # Include chat history in the chain's input
        response = retrieval_chain.invoke(
            input={"input": question, "chat_history": chat_history}
        )

        answer: str = response.get("answer")
        print("\n\n", answer.strip(), "\n\n")

        # Add the model's response to chat history
        chat_history.append({"role": "assistant", "content": answer})


if __name__ == "__main__":
    main()
