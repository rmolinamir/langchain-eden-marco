"""Main entry point for the application."""

import questionary


def main() -> None:
    """Run the main program."""
    chapter = questionary.select(
        "Select chapter to execute: ", choices=["1", "2", "quit"]
    ).ask()

    if chapter == "quit":
        return

    if chapter == "1":
        from chapter_1.main import main as chapter_1_main

        chapter_1_main()
    else:
        from chapter_2.main import main as chapter_2_main

        chapter_2_main()


if __name__ == "__main__":
    main()
