from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field


class Summary(BaseModel):
    """Summary of the person's background and experience."""

    summary: str = Field(description="A summary of the person's work experience")
    interesting_facts: list[str] = Field(description="Two interesting facts about them")
    recent_work_experience: str = Field(
        description="The most recent work experience (based on the positions rather than the summary)"
    )
    estimated_earnings: str = Field(
        description="Estimate how much they might earn based on that experience"
    )
    upskilling: str = Field(
        description="Recommend upskilling aligned with their experience that may help them increase total compensation."
    )


summary_output_parser = PydanticOutputParser(pydantic_object=Summary)
