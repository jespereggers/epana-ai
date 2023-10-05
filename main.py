# constants to start and end conversations
START_CONVO = '{"messages": ['
END_CONVO = "]}"
LEFTOUT_MSG_GER = ["Dokument weggelassen", "Sticker weggelassen", "Anhang weggelassen", "Bild weggelassen"]


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
            if line.strip():  # Check if the line contains only whitespace characters
                try:

                    # don't delete!!! throws exception for lines without timestamp
                    line.split("]", 1)[1]

                    # splitting the line after the timestamp
                    splits = line.split("]", 1)
                    # splitting after the "," to get the date only
                    timestamp = splits[0].split(",", 1)[0][1:]
                    # strip to remove whitespace
                    content = splits[1].strip()

                    # check if message-type is text (instead of documents, stickers etc.)
                    is_text = True
                    for msg in LEFTOUT_MSG_GER:  # currently only checking for german keywords
                        if msg in current_message:
                            is_text = False

                    # ignore first loop where last_actor is still "". Hopefully not breaking anythin 🙄
                    if not last_actor == "" and is_text:
                        # add the actor and the message with the needed format
                        formatted += '{"role": "' + last_actor + '", "content": "' + current_message.strip() + '"}, '

                        # check for the end of a convo
                        if current_timestamp and timestamp and (not current_timestamp == timestamp):
                            formatted = formatted[:-2] + END_CONVO
                            convos.append(formatted)
                            formatted = START_CONVO
                        current_timestamp = timestamp

                    current_message = content.split(":", 1)[1].strip()
                    current_actor = content.split(":", 1)[0]
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
