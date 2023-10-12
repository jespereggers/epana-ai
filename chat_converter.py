import os
import random
import zipfile

# system prompt which will be added to the start of every conversation
SYSTEM_PROMPTS = [
    "Eigne dir Wortwahl, Charaktereigenschaften und Erinnerung an besprochene Inhalte an."
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

# name of the person in the whatsapp chat which will be replaced as 'user'
ai_name: str

def get_dynamic_start_convo(ai_name):
    # confused why this only works when adding ai_name as function argument tbh
    system_prompt = SYSTEM_PROMPTS[random.randint(0, len(SYSTEM_PROMPTS) - 1)]
    return START_CONVO_p1 + SYSTEM_PROMPT_START + ai_name + ". " + system_prompt + START_CONVO_p2


def unzip_file(zip_file_path, extract_path):
    with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
        zip_ref.extractall(extract_path)


def chat_to_jsonl(file, output_path, verification_path):
    # assert correct file format
    if file.split(".")[-1] == "zip":
        # unzip file
        unzip_file(file, 'temp')
        file = "temp/_chat.txt"

    with open(file, encoding='utf-8') as f:
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
                    timestamp = splits[0].split(",", 1)[0][1:]
                    # strip to remove whitespace
                    content = splits[1].strip()

                    # ignore first loop where last_actor is still "". Hopefully not breaking anythin 🙄
                    # ... seems alrighty!
                    # checking for "LRM" to avoid the unusable lines
                    if not last_actor == "" and not '‎' in current_message:
                        # add the actor and the message with the needed format
                        current_message = current_message.replace('"', "")
                        current_convo += '{"role": "' + last_actor + '", "content": "' + current_message.strip() + '"}, '

                        # check for the end of a convo
                        if current_timestamp and timestamp and (not current_timestamp == timestamp):
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

        # write convos and verification_convos to output files
        with open(output_path, "w", encoding='utf-8') as file:
            file.write('\n'.join(convos))
        with open(verification_path, 'w', encoding='utf-8') as file:
            file.write('\n'.join(verification_convos))

    # clean up epana directory
    os.remove('temp/_chat.txt')
    os.rmdir('temp')

if __name__ == '__main__':
    chat_to_jsonl("chat.zip", TRAINING_PATH, VERIFICATION_PATH)
