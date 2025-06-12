"""Main entry point for the application."""

import os

from chapter_1.main import main as chapter_1_main
from chapter_2.main import main as chapter_2_main


def get_env_var(name: str) -> str | None:
    """Get environment variable with error handling."""
    try:
        return os.environ[name]
    except KeyError:
        print(f"Warning: Environment variable {name} not set")
        return None


def main() -> None:
    """Main function that handles chapter selection and execution."""
    my_var = get_env_var("MY_VARIABLE")
    if my_var:
        print(f"MY_VARIABLE: {my_var}")

    while True:
        chapter = input("Enter the chapter number (1/2) or 'q' to quit: ").strip()

        if chapter.lower() == "q":
            break

        if chapter not in {"1", "2"}:
            print("Invalid chapter number. Please enter 1 or 2.")
            continue

        try:
            if chapter == "1":
                chapter_1_main()
            else:  # chapter must be "2" due to validation above
                chapter_2_main()
        except Exception as e:
            print(f"Error running chapter {chapter}: {e}")


if __name__ == "__main__":
    main()
