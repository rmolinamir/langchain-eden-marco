from langchain import hub
from langchain.agents import AgentExecutor, create_react_agent
from langchain.prompts import PromptTemplate
from langchain_core.tools import Tool
from langchain_ollama import ChatOllama

from .api import search_linkedin_profile

PERSONA = """
You are a highly intelligent assistant capable of understanding and executing specific actions based on user requests. Your goal is to assist the user as efficiently and accurately as possible without deviating from their instructions.
"""

FORMAT_INSTRUCTIONS = """
Please follow these formatting instructions carefully:

1. If you need to perform an action to answer the user's question, use the following format:
'''
Thought: Do I need to use a tool? Yes
Action: [Specify the action]
Action Input: [Provide the necessary input for the action]
Observation: [Describe the outcome of the action]
'''

2. If you can answer the user's question without performing any additional actions, use the following format:
'''
Thought: Do I need to use a tool? No
Final Answer: [Provide your answer here]
'''

Your responses should be concise and directly address the user's query. Avoid generating new questions or unnecessary information.
"""

COMMAND = """
Given the full name {full_name}, company name {company_name}, and job title {job_title} of a person, you will
use these parameters to build a search query to obtain search results.

The search query should be in the following format:
"{full_name}, {company_name}, {job_title}"

From the search results, you will find a matching profile using the full name, company name and job title, then
you will extract the LinkedIn profile URL.

Your answer should contain only a string with the LinkedIn profile URL without any other text.

If you cannot find a LinkedIn profile URL, return an empty string.
"""

END = """
End of instructions. Please proceed with answering the user's question following the guidelines provided above.
"""

template = PERSONA + FORMAT_INSTRUCTIONS + COMMAND + END


def linkedin_lookup_agent(full_name: str, company_name: str, job_title: str) -> str:
    """Lookup a LinkedIn profile URL given a person description."""
    llm = ChatOllama(model="llama3.2:3b", temperature=0.0)

    tools = [
        Tool(
            name="Search LinkedIn Profiles",
            description="Returns LinkedIn profile URLs given a search query",
            func=search_linkedin_profile,
        )
    ]

    react_prompt = hub.pull("hwchase17/react")
    react_agent = create_react_agent(llm=llm, tools=tools, prompt=react_prompt)
    agent_executor = AgentExecutor(
        agent=react_agent, tools=tools, verbose=True, handle_parsing_errors=True
    )

    prompt_template = PromptTemplate(
        input_variables=["full_name", "company_name", "job_title"],
        template=template,
    )

    result = agent_executor.invoke(
        input={
            "input": prompt_template.format_prompt(
                full_name=full_name,
                company_name=company_name,
                job_title=job_title,
            )
        }
    )

    linkedin_url: str = result.get("output", "")

    return linkedin_url
