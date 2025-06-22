# Chapter 1: Basic LangChain Chain

This chapter introduces the fundamental concepts of LangChain by implementing a basic chain using the Ollama model.

## Overview

The implementation consists of two main files:

- `main.py`: Entry point that runs the chain
- `chain.py`: Contains the chain implementation

## Implementation Details

### Chain Implementation (`chain.py`)

The chain is built using the following components:

1. **Prompt Template**: A simple template that formats questions for the AI assistant

    ```python
      template = """
      You are a helpful assistant. Answer the following question:
      {question}
      """
    ```

2. **Model Configuration**: Uses the Ollama model with specific parameters

    ```python
    llm = ChatOllama(model="deepseek-r1:8b", temperature=0.0)
    ```

3. **Chain Construction**: Combines the prompt template, model, and output parser

    ```python
    chain = prompt | llm | StrOutputParser()
    ```

### Main Function (`main.py`)

The main function serves as the entry point and demonstrates how to use the chain:

```python
def main() -> None:
    chain()
```

## Key Features

1. **Simple Chain Structure**: Demonstrates the basic chain pattern in LangChain
2. **Prompt Template Usage**: Shows how to create and use prompt templates
3. **Output Parsing**: Uses the string output parser for straightforward responses
4. **Model Integration**: Shows integration with the Ollama model

## Learning Outcomes

- Basic structure of a LangChain chain
- How to create prompt templates
- How to integrate language models
- Basic output parsing
- How to combine components into a functional chain
