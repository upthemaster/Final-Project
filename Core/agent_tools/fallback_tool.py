from langchain.tools import tool
@tool
def fallback_tool(user_input: str) -> str:
    """
    Use when query is outside Sunbeam scope.
    This is a FINAL response.
    """
    return (
        "Sorry, I can help only with Sunbeam-related information "
        "such as courses, branches, or internships."
    )
