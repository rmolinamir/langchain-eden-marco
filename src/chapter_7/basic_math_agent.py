from langchain.agents import AgentExecutor, create_tool_calling_agent, tool
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama


@tool
def add(a: int, b: int) -> int:
    """Add two numbers."""
    print(f"Adding {a} and {b}")
    return a + b


@tool
def subtract(a: int, b: int) -> int:
    """Subtract two numbers."""
    print(f"Subtracting {a} and {b}")
    return a - b


@tool
def multiply(a: int, b: int) -> int:
    """Multiply two numbers."""
    print(f"Multiplying {a} and {b}")
    return a * b


@tool
def divide(a: int, b: int) -> int:
    """Divide two numbers."""
    print(f"Dividing {a} and {b}")
    return a / b


def basic_math_agent(input: str) -> str:
    llm = ChatOllama(model="mistral-nemo:12b")
    tools = [add, subtract, multiply, divide]
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", "You are a helpful assistant"),
            ("placeholder", "{chat_history}"),
            ("human", "{input}"),
            ("placeholder", "{agent_scratchpad}"),
        ]
    )

    agent = create_tool_calling_agent(llm=llm, tools=tools, prompt=prompt)
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

    return agent_executor.invoke({"input": input}).get("output")


if __name__ == "__main__":
    answer = basic_math_agent("What is 37 multiplied by 349?")
    print("Answer:", answer)
