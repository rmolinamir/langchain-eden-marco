"""Main entry point for the application."""

from enum import Enum


class Chapter(Enum):
    CHAPTER_1_CHAIN = "1: Chain"
    CHAPTER_2_CHAIN = "2: Chain"
    CHAPTER_2_APP = "2: App"
    CHAPTER_3_RAG = "3: RAG"


def main(selection: Chapter) -> None:
    if selection == Chapter.CHAPTER_1_CHAIN:
        from chapter_1.main import main

        main()
    elif selection == Chapter.CHAPTER_2_CHAIN:
        from chapter_2.main import main

        main()
    elif selection == Chapter.CHAPTER_2_APP:
        from chapter_2.app import app

        app.run(host="0.0.0.0", port=8647, debug=True)
    elif selection == Chapter.CHAPTER_3_RAG:
        from chapter_3.main import main

        main()


if __name__ == "__main__":
    """Run the main program."""
    # TODO: Commenting this for now until I can make the DevExperience better.
    # chapter = questionary.select(
    #     "Select chapter to execute: ",
    #     choices=[
    #         Chapter.CHAPTER_1_CHAIN.value,
    #         Chapter.CHAPTER_2_CHAIN.value,
    #         Chapter.CHAPTER_2_APP.value,
    #         "Quit",
    #     ],
    # ).ask()
    # if not chapter == "Quit":
    #     main(selection=Chapter(chapter))

    main(Chapter.CHAPTER_3_RAG)
