import os

from langchain_core.messages import HumanMessage
from langgraph.graph import END, MessagesState, StateGraph

from src.chapter_8.nodes import reason, tool_node

AGENT_REASON = "agent_reason"
ACT = "act"
LAST = -1


def should_continue(state: MessagesState) -> str:
    if not state.get("messages")[LAST].tool_calls:
        return END
    return ACT


flow = StateGraph(MessagesState)

flow.add_node(AGENT_REASON, reason)
flow.set_entry_point(AGENT_REASON)
flow.add_node(ACT, tool_node)
flow.add_conditional_edges(
    AGENT_REASON,
    should_continue,
    {
        END: END,
        ACT: ACT,
    },
)
flow.add_edge(ACT, AGENT_REASON)

app = flow.compile(debug=True)


def print_graph():
    """
    Print the graph to a file.
    """
    current_dir = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(current_dir, "./flow.png")
    app.get_graph().draw_mermaid_png(output_file_path=path)


if __name__ == "__main__":
    result = app.invoke(
        {
            "messages": [
                HumanMessage(
                    content="What is the weather in Tokyo? List it, then triple it."
                )
            ]
        }
    )
    print(result.get("messages")[LAST].content)
