from src.chapter_7.router_agent import router_agent

python_agent_input = """
- Generate and save in the current working directory 15 QR codes that point to https://www.robertmolina.dev.
- You have the qrcode library installed for this purpose.
- **IMPORTANT:** You should generate the QR codes in the current working directory, inside a directory called chapter_7_qr_codes.
- When you are done, include the file path of the generated QR codes as part of your response.
"""


def main():
    question = input("Enter a question: ")
    router_agent().invoke({"input": question})


if __name__ == "__main__":
    main()
