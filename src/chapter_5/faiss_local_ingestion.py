import os

from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import FAISS
from langchain_ollama import OllamaEmbeddings
from langchain_text_splitters import CharacterTextSplitter


def main() -> None:
    current_dir = os.path.dirname(os.path.abspath(__file__))
    pdf_path = os.path.join(current_dir, "./files/project_2025.pdf")
    loader = PyPDFLoader(file_path=pdf_path, mode="page")
    text_splitter = CharacterTextSplitter(
        chunk_size=1000, chunk_overlap=200, separator="\n"
    )

    docs = text_splitter.split_documents(documents=loader.load())
    embeddings = OllamaEmbeddings(model="nomic-embed-text")

    FAISS.from_documents(docs, embeddings).save_local("faiss_index")


if __name__ == "__main__":
    main()
