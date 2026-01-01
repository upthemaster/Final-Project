from langchain.tools import tool

@tool
def greeting_tool(user_input: str) -> str:
    """
    Use ONLY when the user greets.
    This tool returns a FINAL answer.
    """
    return (
        "Hello! 👋 I'm the Sunbeam assistant.\n"
        "Ask me about courses, branches, or internships."
    )
