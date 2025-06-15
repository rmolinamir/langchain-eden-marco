"""
This script is used to ingest the documents into FAISS.
Note that it takes a while to run.
"""

import os

from dotenv import load_dotenv
from langchain_community.document_loaders import DirectoryLoader
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from langchain_ollama import OllamaEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter


def load_documents(path: str) -> list[Document]:
    """
    Load the documents from the given path.
    """
    loader = DirectoryLoader(path, glob="**/*.html", show_progress=True)
    docs = loader.load()
    return docs


def split_documents(docs: list[Document]) -> list[Document]:
    """
    Split the documents into smaller chunks.
    """
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=600, chunk_overlap=50)
    return text_splitter.split_documents(docs)


def get_embeddings() -> OllamaEmbeddings:
    """
    Get the embeddings model.
    """
    return OllamaEmbeddings(model="nomic-embed-text")


def save_embeddings(docs: list[Document], embeddings: OllamaEmbeddings) -> None:
    """
    Save the embeddings to FAISS local storage.
    """
    FAISS.from_documents(docs, embeddings).save_local("chapter_6_faiss_index")


def main() -> None:
    """
    Main function to run the ingestion process.
    I'm embedding Project 2025 for the RAG pipeline.
    Why Project 2025? Because it's so retarded I want to see how the LLM handles it.
    """
    path = os.path.join(os.getcwd(), "chapter_6_langchain_docs/python.langchain.com")
    docs = load_documents(path=path)
    print("Loaded documents: ", len(docs))

    split_docs = split_documents(docs=docs)
    print("Split documents: ", len(split_docs))

    # Update the source URL to the actual URL of the documentation.
    for doc in split_docs:
        doc.metadata["source"] = doc.metadata["source"].replace(
            path, "https://python.langchain.com"
        )

    save_embeddings(docs=split_docs, embeddings=get_embeddings())
    print("Saved embeddings to FAISS local storage!")


if __name__ == "__main__":
    load_dotenv()
    main()
