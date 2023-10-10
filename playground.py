import os
import openai


def start_convo(api_key, model_id):
    openai.api_key = api_key
    print("Enter 's' in chat to stop conversation\n")

    # Start the conversation with the system prompt
    response = openai.ChatCompletion.create(
        model=model_id,
        messages=[
            {
                "role": "user",
                "content": "Du bist mein guter Freund Jesper mit dem ich kurze Textkonversationen über Gott und die Welt führe."
            }
        ],
        temperature=1,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )

    # Provide user with response of chatbot
    print("Assistant: " + response.choices[0].message.content)

    while True:
        # Get input prompt of user
        user_prompt: str = input("User: ")
        if user_prompt == "s":
            return

        # Generate response based on prompt
        response = openai.ChatCompletion.create(
            model=model_id,
            messages=[
                {
                    "role": "user",
                    "content": user_prompt
                }
            ],
            temperature=1,
            max_tokens=256,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )

        # Provide user with response of chatbot
        print("Assistant: " + response.choices[0].message.content)


if __name__ == '__main__':
    start_convo("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", "ft:gpt-3.5-turbo-0613:personal::86iNqClH")
