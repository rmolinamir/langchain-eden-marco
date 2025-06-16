import os

from langchain.agents import AgentExecutor, AgentType
from langchain_experimental.agents import create_csv_agent
from langchain_ollama import ChatOllama


def csv_agent(input: str) -> AgentExecutor:
    llm = ChatOllama(model="deepseek-r1:8b", temperature=0)

    current_dir = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(current_dir, "./files/game_of_thrones_episodes_data.csv")

    agent_executor = create_csv_agent(
        llm=llm,
        path=path,
        verbose=True,
        allow_dangerous_code=True,
        agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        agent_executor_kwargs={
            "handle_parsing_errors": True,
        },
    )

    return agent_executor.invoke({"input": input})


_questions = [
    "What is the episode with the highest number of deaths?",
    "What is the episode with the highest viewership?",
    "What is the season with the highest average rating?",
    "What is the season with the highest average viewership?",
]

if __name__ == "__main__":
    for question in _questions:
        csv_agent(question)
