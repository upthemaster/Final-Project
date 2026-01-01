import os
import sys

os.environ["CHROMA_TELEMETRY"] = "False"
os.environ["ANONYMIZED_TELEMETRY"] = "False"

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.append(BASE_DIR)

from langchain_community.vectorstores import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings

from Prepare_Docs.prepare_documents import SunbeamJSONLoader


DATA_DIR = os.path.join(BASE_DIR, "data")
CHROMA_DIR = os.path.join(BASE_DIR, "chroma_db")


def build_vector_store():
    loader = SunbeamJSONLoader(DATA_DIR)
    documents = loader.load()
    print(f"Loaded {len(documents)} documents")

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=80
    )
    chunks = splitter.split_documents(documents)
    print(f"Created {len(chunks)} chunks")

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    vector_store = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=CHROMA_DIR
    )

    vector_store.persist()
    print("Vector store created and persisted successfully")

    return vector_store


if __name__ == "__main__":
    build_vector_store()
