import json

from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_ollama import ChatOllama

from linkedin.agent import linkedin_lookup_agent
from linkedin.api import get_linkedin_profile

template = """
Given the LinkedIn profile {linkedin_profile} about a person, I want you to:

1. Create a summary of the person's background and experience.
2. Two interesting facts about them.
3. Identify the most recent work experience (based on the positions rather than the summary) and estimate how much they might earn based on that experience.
4. Recommend upskilling aligned with their experience that may help them increase total compensation.
"""


def chain(
    full_name: str,
    company_name: str,
    job_title: str,
) -> None:
    """
    This is a simple example of how to use the LangChain library to create a chain of prompts and a model.
    This chain uses the Ollama model to generate a response to the user's question.
    """

    linkedin_profile_url = linkedin_lookup_agent(
        full_name=full_name,
        company_name=company_name,
        job_title=job_title,
    )

    print(f"LinkedIn URL: {linkedin_profile_url}")

    linkedin_profile = get_linkedin_profile(
        linkedin_profile_url=linkedin_profile_url, mock=False
    )

    print(f"LinkedIn profile: {json.dumps(obj=linkedin_profile, indent=2)}")

    if not linkedin_profile:
        raise ValueError("No LinkedIn profile found")

    print("Asking the LLM to recommend upskilling opportunities...")

    prompt = PromptTemplate(
        input_variables=["linkedin_profile"],
        template=template,
    )

    llm = ChatOllama(model="llama3.1:8b", temperature=0.0, verbose=True)

    chain = prompt | llm | StrOutputParser()

    response = chain.invoke(input={"linkedin_profile": linkedin_profile})

    print(response)
