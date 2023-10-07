# system prompt which will be added to the start of every conversation
SYSTEM_PROMPT = "Du bist mein guter Freund Jesper mit dem ich kurze Textkonversationen über Gott und die Welt führe."

# constants to start and end conversations
START_CONVO_p1 = '{"messages": [{ "role": "system", "content": "'
START_CONVO_p2 = '" }, '
START_CONVO = START_CONVO_p1 + SYSTEM_PROMPT + START_CONVO_p2
END_CONVO = "]}"
EMPTY_CONVO = START_CONVO[:-2] + END_CONVO

# name of the person in the whatsapp chat which will be replaced as 'user'
USER = "felix"

# factor by which the main file is bigger than the verification file
VERIFICATION_FACTOR = 10


def main():
    format_file("jesper_chat.txt")


def format_file(file):
    convos = []
    verification_convos = []
    current_convo = START_CONVO
    with open(file, encoding='utf-8') as f:
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
                            current_convo = START_CONVO
                        current_timestamp = timestamp

                    # split the content at ':' and strip the whitespace to get the content
                    current_message = content.split(":", 1)[1].strip()

                    # split the content at ':' to get the user
                    if content.split(":", 1)[0] == USER:
                        current_actor = "user"
                    else:
                        current_actor = "assistant"

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
        with open("output.jsonl", "w", encoding='utf-8') as file:
            file.write('\n'.join(convos))
        with open('verification.jsonl', 'w', encoding='utf-8') as file:
            file.write('\n'.join(verification_convos))


if __name__ == '__main__':
    main()
