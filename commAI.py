import json
import os

import replicate
from dotenv import load_dotenv

load_dotenv()

REPLICATE_API_TOKEN = os.getenv("REPLICATE_API_TOKEN")


def get_json(input_string: str):
    input_string = input_string.strip()
    try:
        json_data = json.loads(input_string)
        return json_data
    except json.JSONDecoder as e:
        print(f"Error decoding JSON string: {e}")
        return None


def make_request(prompt: str):
    if not prompt:
        return None

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

    output = ""
    for text in iterator:
        output += text

    return output


def display_output(stream):
    for data in stream:
        print("Desc: ", data["desc"])
        print("Command: ", data["command"])


question = input("Enter your query: ")

prompt = """
A question will be given related to linux commands, you duty is to create a JSON which indicates the sequence of commands which need to run to solve the question. 

THE OUTPUT SHOULD BE IN JSON, NO NEED TO ADD ANY OTHER CHARACTER WHICH CORRUPT THE JSON. THE JSON SHOULD HAVE ALL THE COMMANDS IN THE RIGHT SEQUENCE. DONOT WRITE ANY TEXT WHICH LIES OUTSITE THE JSON.

JSON FORMAT: [{"desc":"command_description", "command":"linux_command"}]

EXAMPLE:
let's say given question: How to display content in a folder?
output: [{"desc":"this commands displays content in the folder", "command":"ls"}]

GIVEN DATA
question: """ + question

output_string = make_request(prompt)
output_json = get_json(output_string)
display_output(output_json)
