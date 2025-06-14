from typing import Any

from langchain.agents.format_scratchpad.log import format_log_to_str
from langchain.agents.output_parsers.react_single_input import (
    ReActSingleInputOutputParser,
)
from langchain.tools import BaseTool
from langchain_core.agents import AgentAction, AgentFinish
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import Runnable
from langchain_core.tools import render_text_description
from langchain_ollama import ChatOllama

from chapter_4.callbacks import AgentCallbackHandler

from .tools import get_text_length

template = """
Answer the following questions as best you can. You have access to the following tools:

{tools}

Use the following format:

Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question

You must evaluate which tool to use and answer the question logically. Think step-by-step by planning with interleaving THOUGHT, ACTION, and OBSERVATION steps.
Repeat the process until the ACTION leads to a correct answer or you realize that neither your tools nor internal knowledge is enough to answer the question.
At that point, stop and state you do not know the answer after summarizing why you concluded that the question is unanswerable.

Begin!

Question: {input}
Thought: {agent_scratchpad}
"""


def find_tool(tools: list[BaseTool], tool_name: str) -> BaseTool:
    """Find a tool by name."""
    return next(filter(lambda t: t.name == tool_name, tools))


def main() -> None:
    """Main function."""
    tools = [get_text_length]

    prompt = PromptTemplate.from_template(template=template).partial(
        tools=render_text_description(tools),
        tool_names=", ".join([t.name for t in tools]),
    )

    llm = ChatOllama(
        model="llama3.1:8b",
        temperature=0.0,
        verbose=True,
        stop=["\nObservation"],
        callbacks=[AgentCallbackHandler()],
    )

    intermediate_steps: list[tuple[AgentAction, str]] = []

    agent: Runnable[Any, Any] = (
        {
            "input": lambda x: x["input"],
            "agent_scratchpad": lambda x: format_log_to_str(x["agent_scratchpad"]),
        }
        | prompt
        | llm
        | ReActSingleInputOutputParser()
    )

    agent_step_count = 0
    agent_loop_limit = 20

    while True:
        print(f"\n\n***Loop: {agent_step_count + 1}***\n\n")

        agent_step = agent.invoke(
            input={
                "input": "What is the length of the string: Hello, world!",
                "agent_scratchpad": intermediate_steps,
            },
        )
        agent_step_count += 1

        if isinstance(agent_step, AgentAction):
            tool_name = agent_step.tool
            tool_input = agent_step.tool_input
            tool = find_tool(tools=tools, tool_name=tool_name)
            observation = tool.invoke(str(tool_input))
            intermediate_steps.append((agent_step, observation))
        elif isinstance(agent_step, AgentFinish):
            print(agent_step.return_values)
            break
        elif agent_step_count >= agent_loop_limit:
            print(f"Agent loop limit of {agent_loop_limit} reached.")
            break


if __name__ == "__main__":
    main()
