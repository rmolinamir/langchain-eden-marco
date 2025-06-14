import os

from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_core.documents import Document
from langchain_ollama import OllamaEmbeddings
from langchain_pinecone import PineconeVectorStore
from langchain_text_splitters import RecursiveCharacterTextSplitter


def load_pdf_documents(pdf_path: str) -> list[Document]:
    """
    Load the PDF documents from the given path.
    """
    loader = PyPDFLoader(file_path=pdf_path, mode="page")
    docs = loader.load()
    return docs


def split_documents(docs: list[Document]) -> list[Document]:
    """
    Split the documents into smaller chunks.
    """
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    return text_splitter.split_documents(docs)


def get_embeddings() -> OllamaEmbeddings:
    """
    Embed the documents.
    """
    return OllamaEmbeddings(model="nomic-embed-text")


def save_embeddings(docs: list[Document], embeddings: OllamaEmbeddings) -> None:
    """
    Save the embeddings to Pinecone.
    """
    index_name = os.getenv("PINECONE_CHAPTER_5_INDEX_NAME")
    batch_size = 100

    for i in range(0, len(docs), batch_size):
        batch = docs[i : i + batch_size]
        print(
            f"Processing batch {i // batch_size + 1} of {(len(docs) + batch_size - 1) // batch_size}"
        )
        PineconeVectorStore.from_documents(
            documents=batch,
            embedding=embeddings,
            index_name=index_name,
        )


def main() -> None:
    """
    Main function to run the ingestion process.
    I'm embedding Project 2025 for the RAG pipeline.
    Why Project 2025? Because it's so retarded I want to see how the LLM handles it.
    """
    current_dir = os.path.dirname(os.path.abspath(__file__))
    pdf_path = os.path.join(current_dir, "./files/project_2025.pdf")

    docs = load_pdf_documents(pdf_path=pdf_path)
    print("Loaded PDF: ", len(docs))

    split_docs = split_documents(docs=docs)
    print("Split documents: ", len(split_docs))

    save_embeddings(docs=split_docs, embeddings=get_embeddings())
    print("Saved embeddings to Pinecone!")


if __name__ == "__main__":
    load_dotenv()
    main()
