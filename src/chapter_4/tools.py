from langchain.tools import tool


@tool
def get_text_length(text: str) -> int:
    """Returns the length of the text."""
    return len(text)


if __name__ == "__main__":
    print(get_text_length.invoke({"text": "\nHello, world!\n"}))
