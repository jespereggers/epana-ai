import os
import random
import ast
import zipfile
import json
from token_checker import get_tokens
from datetime import datetime

# system prompt which will be added to the start of every conversation
SYSTEM_PROMPTS = [
    "Imitiere ihn, aber nicht deinen Gesprächspartner, durch Ausdruck von Persönlichkeit, Wortwahl."
]
SYSTEM_PROMPT_START = "Du bist "

# constants to start and end conversations
START_CONVO_p1 = '{"messages": [{ "role": "system", "content": "'
START_CONVO_p2 = '" }, '
START_CONVO = START_CONVO_p1 + SYSTEM_PROMPTS[0] + START_CONVO_p2
END_CONVO = "]}"
EMPTY_CONVO = START_CONVO[:-2] + END_CONVO

# factor by which the main file is bigger than the verification file
VERIFICATION_FACTOR = 10

# data paths for quick adjustments
TRAINING_PATH = "output.jsonl"
VERIFICATION_PATH = "verification.jsonl"

TOKEN_LIMIT = 3000

# name of the person in the whatsapp chat which will be replaced as 'user'
ai_name: str


def message_is_valid(message):
    if '‎' in message:
        return False
    if 'https' in message:
        return False
    if message == '.':
        return False
    return True


def get_time_gap(timestamp1, timestamp2):
    if len(timestamp1) == 0 or len(timestamp2) == 0:
        return 0

    # Convert the timestamps to datetime objects
    format_str = '%d.%m.%y %H:%M:%S'
    time1 = datetime.strptime(" ".join(timestamp1), format_str)
    time2 = datetime.strptime(" ".join(timestamp2), format_str)

    # Calculate the time difference in hours
    time_difference = (time2 - time1).total_seconds() / 3600

    return round(time_difference)


def get_dynamic_start_convo(ai_name):
    # confused why this only works when adding ai_name as function argument tbh
    system_prompt = SYSTEM_PROMPTS[random.randint(0, len(SYSTEM_PROMPTS) - 1)]
    return START_CONVO_p1 + SYSTEM_PROMPT_START + ai_name + ". " + system_prompt + START_CONVO_p2


def unzip_file(zip_file_path, extract_path):
    with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
        zip_ref.extractall(extract_path)


def chat_to_jsonl(input_file_path, output_file_path, verification_file_path) -> int:
    # assert correct file format
    if input_file_path.split(".")[-1] == "zip":
        # unzip file
        unzip_file(input_file_path, 'temp')
        input_file_path = "temp/_chat.txt"

    with (open(input_file_path, encoding='utf-8') as f):
        convos = []
        verification_convos = []
        ai_name = f.readline().split('] ')[1].split(':')[0]
        current_convo = get_dynamic_start_convo(ai_name)

        last_actor = ""
        current_message = ""
        current_timestamp = ""
        for line in f:
            # Check if the line contains only whitespace characters
            if line.strip():
                try:

                    # don't delete!!! throws exception for lines without timestamp
                    line.split("]", 1)[1]

                    # splitting the line after the timestamp
                    splits = line.split("]", 1)
                    # splitting after the "," to get the date only
                    timestamp = [splits[0].split(",", 1)[0][1:].replace("[", ""), splits[0].split(",", 1)[1][1:]]
                    # strip to remove whitespace
                    content = splits[1].strip()

                    # ignore first loop where last_actor is still "". Hopefully not breaking anythin 🙄
                    # ... seems alrighty!
                    # checking for "LRM" to avoid the unusable lines
                    if not last_actor == "" and message_is_valid(current_message):
                        # add the actor and the message with the needed format
                        current_message = current_message.replace('"', "")
                        current_convo += '{"role": "' + last_actor + '", "content": "' + current_message.strip() + '"}, '

                        # cut convo into
                        convo_as_dict: dict = ast.literal_eval(current_convo[:-2] + "]}")

                        if get_time_gap(current_timestamp, timestamp) >= 28 or get_tokens([convo_as_dict]) > 3500:
                            current_convo = current_convo[:-2] + END_CONVO

                            # check for valid convos
                            if 'user' in current_convo and 'assistant' in current_convo:
                                # check to which list the conversation should be added
                                if (VERIFICATION_FACTOR * len(verification_convos)) > len(convos):
                                    convos.append(current_convo)
                                else:
                                    verification_convos.append(current_convo)
                            current_convo = get_dynamic_start_convo(ai_name)
                        current_timestamp = timestamp

                    # split the content at ':' and strip the whitespace to get the content
                    current_message = content.split(":", 1)[1].strip()

                    # split the content at ':' to get the user
                    if content.split(":", 1)[0] == ai_name:
                        current_actor = "assistant"
                    else:
                        current_actor = "user"

                    last_actor = current_actor
                # an IndexError occurs if there is no ']' found to split at. in this case, the message
                # had a '\n' in it and this line was actually a part of the message, so we stitch them together
                except IndexError:
                    # .strip to remove \n
                    current_message = current_message.strip() + " " + line

        # remove the last ", "
        current_convo = current_convo[:-2] + END_CONVO
        # filter out empty convos
        if not current_convo == EMPTY_CONVO:
            convos.append(current_convo)

        # assert each convo ends with message of assistant
        for i in range(0, len(convos)):
            convo_as_dict = json.loads(convos[i])
            if convo_as_dict["messages"][-1]["role"] == "user":
                convo_as_dict["messages"].append({"role": "assistant", "content": ""})
                convos[i] = json.dumps(convo_as_dict)

        for i in range(0, len(verification_convos)):
            convo_as_dict = json.loads(verification_convos[i])
            if convo_as_dict["messages"][-1]["role"] == "user":
                convo_as_dict["messages"].append({"role": "assistant", "content": ""})
                verification_convos[i] = json.dumps(convo_as_dict)

        output = '\n'.join(convos)
        verify = '\n'.join(verification_convos)

        # write convos and verification_convos to output files
        with open(output_file_path, "w", encoding='utf-8') as file:
            file.write(output)
        with open(verification_file_path, 'w', encoding='utf-8') as file:
            file.write(verify)
    return 1

    # FIXME not working with the current impl of the flask app
    # clean up epana directory
    # os.remove('temp/_chat.txt')
    # os.rmdir('temp')


if __name__ == '__main__':
    chat_to_jsonl("temp/_chat.txt", TRAINING_PATH, VERIFICATION_PATH)
