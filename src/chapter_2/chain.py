from langchain.prompts import PromptTemplate
from langchain_ollama import ChatOllama

from src.chapter_2.linkedin.agent import linkedin_lookup_agent
from src.chapter_2.linkedin.api import get_linkedin_profile
from src.chapter_2.output_parsers import Summary, summary_output_parser

summary_template = """
Given the LinkedIn profile about a person:

{linkedin_profile}

I want you to:

1. Create a summary of the person's background and experience.
2. Two interesting facts about them.
3. Identify the most recent work experience (based on the positions rather than the summary) and estimate how much they might earn based on that experience.
4. Recommend upskilling aligned with their experience that may help them increase total compensation.

Your response should be in the following format:

{format_instructions}
"""


def chain(
    full_name: str,
    company_name: str,
    job_title: str,
) -> tuple[Summary, str]:
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
        # Remove mock=True if you want to use the real LinkedIn profile
        linkedin_profile_url=linkedin_profile_url,
        mock=True,
    )

    if not linkedin_profile:
        raise ValueError("No LinkedIn profile found")

    prompt = PromptTemplate(
        input_variables=["linkedin_profile"],
        template=summary_template,
        partial_variables={
            "format_instructions": summary_output_parser.get_format_instructions()
        },
    )

    llm = ChatOllama(model="llama3.1:8b", temperature=0.0, verbose=True)

    chain = prompt | llm | summary_output_parser

    response: Summary = chain.invoke(input={"linkedin_profile": linkedin_profile})

    return response, linkedin_profile.get("photoUrl", "")
