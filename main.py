# constants to start and end conversations
START_CONVO_p1 = '{"messages": [{ "role": "system", "content": "'
SYSTEM_PROMPT = "Du bist mein guter Freund Jesper mit dem ich kurze Textkonversationen über Gott und die Welt führe."
START_CONVO_p2 = '" }, '
START_CONVO = START_CONVO_p1 + SYSTEM_PROMPT + START_CONVO_p2
END_CONVO = "]}"
USER = "felix"


def main():
    format_file("test.txt")


def format_file(file):
    convos = []
    formatted = START_CONVO
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
                        formatted += '{"role": "' + last_actor + '", "content": "' + current_message.strip() + '"}, '

                        # check for the end of a convo
                        if current_timestamp and timestamp and (not current_timestamp == timestamp):
                            formatted = formatted[:-2] + END_CONVO
                            convos.append(formatted)
                            formatted = START_CONVO
                        current_timestamp = timestamp

                    current_message = content.split(":", 1)[1].strip()

                    if content.split(":", 1)[0] == USER:
                        current_actor = "user"
                    else:
                        current_actor = "assistant"

                    last_actor = current_actor

                except IndexError:
                    # .strip to remove \n
                    current_message = current_message.strip() + " " + line

        # remove the last ", "
        formatted = formatted[:-2] + END_CONVO
        if not formatted == '{"messages":]}':
            convos.append(formatted)

        with open("output.json", "w", encoding='utf-8') as file:
            file.write('\n'.join(convos))


if __name__ == '__main__':
    main()
