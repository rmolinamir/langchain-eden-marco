from csv_agent import csv_agent
from langchain import hub
from langchain.agents import AgentExecutor, Tool, create_react_agent
from langchain_ollama import ChatOllama
from python_agent import python_agent

instructions = """
- You are a a router agent that can route questions to the appropriate agent.
- **IMPORTANT:** You must follow the RAG format or else you will run into output parsing errors.
"""


python_agent_description = """
Use when transforming natural language into python code and executing it, returning the output of the code execution.
**IMPORTANT:** ONLY accepts natural language as the action input.
"""

csv_agent_description = """
Use when answering questions about the data in the Game of Thrones episodes CSV dataset.
**IMPORTANT:** ONLY accepts natural language as the action input.
"""


def router_agent() -> AgentExecutor:
    base_prompt = hub.pull("langchain-ai/react-agent-template")

    llm = ChatOllama(model="llama3.2:3b", temperature=0)
    prompt = base_prompt.partial(instructions=instructions)
    tools = [
        Tool(
            name="csv_agent",
            description=csv_agent_description,
            func=csv_agent,
        ),
        Tool(
            name="python_agent",
            description=python_agent_description,
            func=python_agent,
        ),
    ]

    agent = create_react_agent(
        llm=llm,
        prompt=prompt,
        tools=tools,
    )

    return AgentExecutor(
        agent=agent, tools=tools, verbose=True, handle_parsing_errors=True
    )
