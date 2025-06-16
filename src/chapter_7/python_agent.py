from langchain import hub
from langchain.agents import AgentExecutor, create_react_agent
from langchain_experimental.tools.python.tool import PythonREPLTool
from langchain_ollama import ChatOllama

instructions = """
- You are an agent designed to write and execute python code to answer questions.
- **IMPORTANT:** You must follow the RAG format or else you will run into output parsing errors.
- You have access to a python REPL tool, which you can use to execute python code.
- If you get an error, debug your code and try again, and only use the output of the python tool to answer questions.
- You might know the answer without writing any code, but you should still run the code to get the answer.
- If it does not seem like you can write code to answer the question, return "I don't know" as the answer.
"""


def python_agent(question: str) -> AgentExecutor:
    base_prompt = hub.pull("langchain-ai/react-agent-template")

    llm = ChatOllama(model="codestral", temperature=0)
    prompt = base_prompt.partial(instructions=instructions)
    tools = [PythonREPLTool()]

    agent = create_react_agent(
        llm=llm,
        prompt=prompt,
        tools=tools,
    )

    agent_executor = AgentExecutor(
        agent=agent, tools=tools, verbose=True, handle_parsing_errors=True
    )

    return agent_executor.invoke({"input": question})


_input = """
- Generate and save in the current working directory 15 QR codes that point to https://www.robertmolina.dev.
- You have the qrcode library installed for this purpose.
- **IMPORTANT:** You should generate the QR codes in the current working directory, inside a directory called chapter_7_qr_codes.
- When you are done, include the file path of the generated QR codes as part of your response.
"""

if __name__ == "__main__":
    python_agent(_input)
