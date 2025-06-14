"""Main entry point for the application."""

import importlib
import sys
from enum import Enum

import questionary


class Chapter(Enum):
    CHAPTER_1 = "1: LangChain Introduction"
    CHAPTER_2 = "2: Chains and Agents"
    CHAPTER_3 = "3: AI-driven Application"
    CHAPTER_4 = "4: RAG"
    CHAPTER_5 = "5: RAG and Embeddings"


def main(selection: Chapter) -> None:
    chapter_map = {
        Chapter.CHAPTER_1: "chapter_1",
        Chapter.CHAPTER_2: "chapter_2",
        Chapter.CHAPTER_3: "chapter_3",
        Chapter.CHAPTER_4: "chapter_4",
        Chapter.CHAPTER_5: "chapter_5",
    }
    chapter_module = importlib.import_module(f"{chapter_map[selection]}.main")
    chapter_module.main()


if __name__ == "__main__":
    """Run the main program."""
    if len(sys.argv) > 1:
        try:
            chapter_num = int(sys.argv[1])
            if 1 <= chapter_num <= 5:
                chapter = list(Chapter)[chapter_num - 1]
                main(selection=chapter)
            else:
                print("Please provide a chapter number between 1 and 5")
        except ValueError:
            print("Please provide a valid chapter number")
    else:
        chapter = questionary.select(
            "Select chapter to execute: ",
            choices=[
                Chapter.CHAPTER_1.value,
                Chapter.CHAPTER_2.value,
                Chapter.CHAPTER_3.value,
                Chapter.CHAPTER_4.value,
                Chapter.CHAPTER_5.value,
                "Quit",
            ],
        ).ask()

        if chapter != "Quit":
            # Find the Chapter enum member that matches the selected value
            selected_chapter = next((c for c in Chapter if c.value == chapter), None)
            if selected_chapter:
                main(selection=selected_chapter)
