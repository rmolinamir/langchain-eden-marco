from chapter_3.app import app


def main() -> None:
    app.run(host="0.0.0.0", port=8647, debug=True)
