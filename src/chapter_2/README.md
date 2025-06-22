# Chapter 2: LinkedIn Profile Analysis

This chapter demonstrates a more advanced use of LangChain by implementing a LinkedIn profile analysis system. The implementation showcases various LangChain features including agents, output parsing, and API integrations.

## Overview

The system analyzes LinkedIn profiles by:

1. Looking up LinkedIn profiles using an agent-based approach
2. Extracting profile information
3. Generating structured analysis using custom output parsers

## Implementation Structure

The implementation is organized into several components:

    ```
    chapter_2/
    ├── linkedin/
    │   ├── agent.py      # LinkedIn profile lookup agent
    │   ├── api.py        # LinkedIn API integration
    │   └── mocks/        # Mock data for testing
    ├── chain.py          # Main chain implementation
    ├── main.py          # Entry point
    └── output_parsers.py # Custom Pydantic output parsers
    ```

## Key Components

### 1. Output Parser (`output_parsers.py`)

Uses Pydantic for structured output parsing:

    ```python
    class Summary(BaseModel):
        summary: str
        interesting_facts: list[str]
        recent_work_experience: str
        estimated_earnings: str
        upskilling: str
    ```

### 2. LinkedIn Agent (`linkedin/agent.py`)

Implements an agent that:

- Takes a person's name, company, and job title
- Searches for their LinkedIn profile
- Returns the profile URL

Key features:

- Uses ReAct framework for agent implementation
- Integrates with search tools
- Handles complex search queries

### 3. LinkedIn API Integration (`linkedin/api.py`)

Provides functions for:

- Profile data retrieval
- Mock data handling
- Data cleaning and formatting

### 4. Main Chain (`chain.py`)

Orchestrates the entire process:

1. Profile lookup using the agent
2. Data retrieval from LinkedIn
3. Analysis generation using the LLM
4. Structured output creation

## Usage Example

    ```python
    def main() -> None:
        chain(
            full_name="Robert Molina",
            company_name="PayPal",
            job_title="Software Engineer",
        )
    ```

## Running the Example

1. Set up required environment variables:

        ```bash
        export TAVILY_API_KEY="your_key_here"
        export SCRAPING_IO_API_KEY="your_key_here"  # Optional for real API usage
        ```

2. Run the example:

        ```bash
        python -m src.chapter_2.main
        ```

## Features Demonstrated

1. **Agent Implementation**
   - ReAct framework usage
   - Tool integration
   - Complex decision making

2. **Output Parsing**
   - Pydantic models
   - Structured data handling
   - Type validation

3. **API Integration**
   - External API usage
   - Mock data handling
   - Error handling

4. **Chain Orchestration**
   - Multi-step processing
   - Data transformation
   - Result formatting

## Learning Outcomes

- How to implement LangChain agents
- Working with custom output parsers
- Integrating external APIs
- Handling mock data for testing
- Building complex chains with multiple components
- Using the ReAct framework for agent development
