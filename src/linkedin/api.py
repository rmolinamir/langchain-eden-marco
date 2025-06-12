import json
import os
from typing import Any

import requests
from langchain_community.tools.tavily_search import TavilySearchResults


def minimal_profile(data: dict[str, Any]) -> dict[str, Any]:
    """Remove empty values and specific fields from a dictionary."""
    return {
        key: value
        for key, value in data.items()
        if value not in ([], "", None)
        and key not in ("certifications", "testScores", "volunteeringExperiences")
    }


def mocked_linkedin_profile() -> dict[str, Any]:
    """Get Robert Molina's LinkedIn profile from local JSON file."""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.join(current_dir, "./mocks/robert_molina_linkedin.json")

    with open(json_path) as f:
        data: dict[str, Any] = json.load(f).get("person", {})

    return data


def get_linkedin_profile(
    linkedin_profile_url: str, mock: bool = True
) -> dict[str, Any]:
    """Get a LinkedIn profile."""
    if mock:
        return minimal_profile(mocked_linkedin_profile())

    api_endpoint = "https://api.scrapin.io/enrichment/profile"
    params = {
        "apikey": os.environ.get("SCRAPING_IO_API_KEY"),
        "linkedInUrl": linkedin_profile_url,
    }
    response = requests.get(api_endpoint, params=params)
    data: dict[str, Any] = response.json().get("person", {})
    return minimal_profile(data)


def search_linkedin_profile(search_query: str) -> Any:
    """Find a LinkedIn profile URL given a full name."""
    search = TavilySearchResults(api_key=os.environ.get("TAVILY_API_KEY"))
    return search.run(f"site:linkedin.com {search_query}")
