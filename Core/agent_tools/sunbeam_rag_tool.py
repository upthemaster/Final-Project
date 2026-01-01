import os
import sys

os.environ["CHROMA_TELEMETRY"] = "False"

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(BASE_DIR)

from langchain.tools import tool
from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage


# Embeddings
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# Vector store
db = Chroma(
    persist_directory=os.path.join(BASE_DIR, "chroma_db"),
    embedding_function=embeddings
)

llm = ChatOpenAI(
    model="google_gemma-3-4b-it",
    base_url="http://localhost:1234/v1",
    api_key="not-needed",
    temperature=0.2
)


@tool
def sunbeam_rag_tool(query: str) -> str:
    """
    Answers Sunbeam-related questions using ChromaDB.
    Can be used by:
    - Agent (future)
    - Direct router call (current)
    """

    docs = db.similarity_search(query, k=25)

    if not docs:
        return "I do not have that information."

    context = "\n\n".join(doc.page_content for doc in docs)

    system_prompt = (
        "You are a Sunbeam Institute assistant.\n"
        "Answer ONLY using the given context.\n"
        "If the answer is not present, say:\n"
        "\"I do not have that information.\""
    )

    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(
            content=f"Context:\n{context}\n\nQuestion:\n{query}"
        )
    ]

    response = llm.invoke(messages)
    return response.content
