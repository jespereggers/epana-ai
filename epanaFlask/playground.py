# Eine angepasste Version des Playground-Skripts für die Verwendung in der Flask-App
from openai import OpenAI

def askBot(api_key, model_id, current_conversation):
    client = OpenAI(api_key=api_key)

    # Aktuelle API-Aufrufstruktur
    completion = client.chat.completions.create(
        model=model_id,
        messages=current_conversation
    )

    return completion.choices[0].message


if __name__ == '__main__':
    askBot(
        "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",
        "ft:gpt-3.5-turbo-0613:personal::88BtAC5L",
        [{"role": "user", "content": "Hello!"}]
    )
