import os
import sys

os.environ["CHROMA_TELEMETRY"] = "False"
os.environ["ANONYMIZED_TELEMETRY"] = "False"

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.append(BASE_DIR)

from langchain_openai import ChatOpenAI

from Core.agent_tools.greeting_tool import greeting_tool
from Core.agent_tools.sunbeam_rag_tool import sunbeam_rag_tool
from Core.agent_tools.fallback_tool import fallback_tool


llm = ChatOpenAI(
    model="google_gemma-3-4b-it",
    base_url="http://localhost:1234/v1",
    api_key="not-needed",
    temperature=0.2
)


def router(user_input: str) -> str:
    """
    Routes user input to the correct tool.
    Greeting is matched safely (no substring bugs like 'hi' in 'with').
    """
    q = user_input.lower().strip()
    words = q.split()

    if len(words) <= 3 and any(
        w in {"hi", "hello", "hey", "thanks", "bye"} for w in words
    ):
        return greeting_tool.invoke(user_input)

    if any(
        w in {
            "sunbeam", "course", "courses",
            "branch", "branches",
            "internship", "internships",
            "fee", "fees",
            "schedule", "batch", "batches"
        }
        for w in words
    ):
        return sunbeam_rag_tool.invoke(user_input)

    return fallback_tool.invoke(user_input)


if __name__ == "__main__":
    print("🤖 Sunbeam Chatbot (router + tools, stable mode)\n")

    while True:
        user_input = input("You: ").strip()

        if user_input.lower() in {"exit", "quit"}:
            break

        response = router(user_input)
        print(f"\nBot: {response}\n")
