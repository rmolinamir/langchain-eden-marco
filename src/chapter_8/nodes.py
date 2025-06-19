from langgraph.graph import MessagesState
from langgraph.prebuilt import ToolNode

from src.chapter_8.react import llm, tools

SYSTEM_PROMPT = """
You are a helpful assistant that can use tools to answer questions.
"""


def reason(state: MessagesState) -> MessagesState:
    """
    Run the agent reasoning about the user's query.
    """
    response = llm.invoke(
        input=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT,
            },
            *state.get("messages"),
        ]
    )

    return {"messages": [response]}


tool_node = ToolNode(tools)

if __name__ == "__main__":
    reason(MessagesState(messages=[]))
