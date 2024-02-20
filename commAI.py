import json
import os

import replicate
from dotenv import load_dotenv

load_dotenv()  # loading .env variables

# colors for the console print statements
HEADER = '\033[95m'
OKBLUE = '\033[94m'
OKCYAN = '\033[96m'
OKGREEN = '\033[92m'
WARNING = '\033[93m'
FAIL = '\033[91m'
ENDC = '\033[0m'
BOLD = '\033[1m'
UNDERLINE = '\033[4m'

# Get your api token through your replicate account
REPLICATE_API_TOKEN = os.getenv("REPLICATE_API_TOKEN")


# converts a string into a JSON format
def get_json(input_string: str):

    input_string = input_string.strip()

    try:
        json_data = json.loads(input_string)
        return json_data
    except json.JSONDecoder as e:
        print(FAIL + f"Error decoding JSON string: {e}" + FAIL)
        return None


# makes request to the model with the given prompt
def make_request(prompt: str):
    if not prompt:
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


# displays the output of the stream
# the stream should be in the proper JSON.
def display_output(stream):

    # if the stream does not have any data
    # then, just print a statement and return from the function
    if len(stream) == 0:
        print(FAIL + "No suitable output found !!!" + FAIL)
        return

    # otherwise loop through the JSON stream and
    # print the desc and commands one by one
    for data in stream:
        print(OKBLUE + data["desc"] + OKBLUE)
        print(OKGREEN + data["command"] + OKGREEN)


# asking for the question
question = input(HEADER + "Enter your query: " + HEADER)

print("\n")

# prompt which needs to submit to the model.
prompt = """
A question will be given related to linux commands, you duty is to create a JSON which indicates the sequence of commands which need to run to solve the question. 

THE OUTPUT SHOULD BE IN JSON, NO NEED TO ADD ANY OTHER CHARACTER WHICH CORRUPT THE JSON. THE JSON SHOULD HAVE ALL THE COMMANDS IN THE RIGHT SEQUENCE. DONOT WRITE ANY TEXT WHICH LIES OUTSITE THE JSON.

JSON FORMAT: [{"desc":"command_description", "command":"linux_command"}]

IF the question does not make any sence so return an empty JSON.

EXAMPLE:
let's say given question: How to display content in a folder?
output: [{"desc":"this commands displays content in the folder", "command":"ls"}]

GIVEN DATA
question: """ + question


# first, making the request to the model
output_string = make_request(prompt)

# second, then converting the string into valid JSON
output_json = get_json(output_string)

# finally, display the data
display_output(output_json)
