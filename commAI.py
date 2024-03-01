import os
import sys
import time

from dotenv import load_dotenv
from termcolor import colored
from openai import OpenAI

load_dotenv()  # loading .env variables

# colors for the console print statements
HEADER = "magenta"
OKBLUE = "blue"
WARNING = "yellow"
OUTPUT = "green"
FAIL = "red"

# getting the openai api key from the environment variables
OPENAI_API_KEY = os.getenv("OPENAI_API")


# writing text on the console with type writer effect.
def type_write(text: str, delay: float = 0.05):

    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)

    print("\n")


# asking the question to the openai model
def ask_to_openai(system_promt: str, prompt: str) -> str:
    client = OpenAI(api_key=OPENAI_API_KEY)

    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": system_promt},
            {"role": "user", "content": prompt},
        ]
    )

    return completion.choices[0].message.content


# asking for the question
question_text = colored("commAI - Enter your query: ", "cyan")
question = input(question_text)

print(colored("Please wait...", OKBLUE))

system_prompt = """A question will be given related to linux commands, your duty is to create a concise answer and keep the output as small as possible. keep it in points and do not add any markdown."""

prompt = question

# first, asking to openai
output_string = ask_to_openai(system_prompt, prompt)

# then, writing the output
type_write(colored(output_string, OUTPUT))
