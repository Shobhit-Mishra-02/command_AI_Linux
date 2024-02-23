import os
import sys
import time

import replicate
from dotenv import load_dotenv
from termcolor import colored

load_dotenv()  # loading .env variables

# colors for the console print statements
HEADER = "magenta"
OKBLUE = "blue"
WARNING = "yellow"
OUTPUT = "green"
FAIL = "red"

# Get your api token through your replicate account
REPLICATE_API_TOKEN = os.getenv("REPLICATE_API_TOKEN")


# writing text on the console with type writer effect.
def type_write(text: str, delay: float = 0.05):

    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)

    print("\n")


# makes request to the model with the given prompt
def make_request(prompt: str):
    if not prompt:
        print(colored("No prompt was provied !!", FAIL))
        return None

    # model used meta/llama-2-70b-chat, search it on replicate
    # here the request is made to the selected replicate model
    iterator = replicate.run(
        "meta/llama-2-70b-chat:2d19859030ff705a87c746f7e96eea03aefb71f166725aee39692f1476566d48",
        input={
            "debug": False,
            "top_p": 1,
            "prompt": prompt,
            "temperature": 0.5,
            "system_prompt": "You are a helpful, respectful and honest assistant. Always answer as helpfully as possible, while being safe. Your answers should not include any harmful, unethical, racist, sexist, toxic, dangerous, or illegal content. Please ensure that your responses are socially unbiased and positive in nature.\n\nIf a question does not make any sense, or is not factually coherent, explain why instead of answering something not correct. If you don't know the answer to a question, please don't share false information.",
            "max_new_tokens": 500,
            "min_new_tokens": -1
        }
    )

    # extracting the chunks of text and putting it inside the output variable.
    output = ""
    for text in iterator:
        output += text

    return output


# asking for the question
question_text = colored("commAI - Enter your query: ", "cyan")
question = input(question_text)

print(colored("Please wait...", OKBLUE))

# prompt which needs to submit to the model.
prompt = """
A question will be given related to linux commands, your duty is to create a concise answer and keep the output as small as possible. keep it in points and do not add any markdown.

Question: """ + question


# first, making the request to the model
output_string = make_request(prompt)

type_write(colored(output_string, OUTPUT))
