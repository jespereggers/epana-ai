import os
import openai


def askBot(api_key, model_id, current_conversation, user_prompt):
    # Set OpenAI API key
    openai.api_key = api_key

    # Generate response based on prompt
    response = openai.ChatCompletion.create(
        model=model_id,
        messages=current_conversation,
        temperature=1,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )

    current_conversation.append(response.choices[0].message)
    return response.choices[0].message


if __name__ == '__main__':
    askBot("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", "ft:gpt-3.5-turbo-0613:personal::88BtAC5L")
