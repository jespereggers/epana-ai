import os
import openai

CONVO = []
SYSTEM_PROMPT = "Du bist mein guter Freund Jesper mit dem ich kurze Textkonversationen über Gott und die Welt führe."


def start_convo(api_key, model_id):
    openai.api_key = api_key
    print("Enter 's' in chat to stop conversation\n")

    # Provide user with response of chatbot
    CONVO.append({
        "role": "user",
        "content": SYSTEM_PROMPT
    })
    while True:
        # Get input prompt of user
        user_prompt: str = input("User: ")
        if user_prompt == "s":
            return
        if len(CONVO) > 20:
            CONVO.pop(1)

        # Add user prompt to conversation
        CONVO.append({
            "role": "user",
            "content": user_prompt
        })
        print(CONVO)
        # Generate response based on prompt
        response = openai.ChatCompletion.create(
            model=model_id,
            messages=CONVO,
            temperature=1,
            max_tokens=256,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )

        # Provide user with response of chatbot
        CONVO.append(response.choices[0].message)
        print("Assistant: " + response.choices[0].message.content)


if __name__ == '__main__':
    start_convo("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", "ft:gpt-3.5-turbo-0613:personal::86iNqClH")
