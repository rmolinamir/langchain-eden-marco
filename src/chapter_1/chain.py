from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_ollama import ChatOllama

template = """
You are a helpful assistant. Answer the following question:
{question}
"""


def chain() -> None:
    """
    This is a simple example of how to use the LangChain library to create a chain of prompts and a model.
    This chain uses the Ollama model to generate a response to the user's question.
    """

    prompt = PromptTemplate(
        input_variables=["question"],
        template=template,
    )

    llm = ChatOllama(model="deepseek-r1:8b", temperature=0.0)

    chain = prompt | llm | StrOutputParser()

    response = chain.invoke(input={"question": "What is the capital of Spain?"})

    print(response)
