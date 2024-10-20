Epana Chat - AI That Clones Personality

#### Video Demo
https://www.youtube.com/watch?v=l9Tkm3w2xTM

#### Description
Chat exports are a kind of personalized data everyone can access.
Epana AI learns from your chats and continues the conversation by imitating your friend (indeed kinda scary!)

We have built a simple routine around 
(1) chat-archive to training-material conversion,
(2) fine-tuning custom models and
(3) database management so that everyone can have fun without any pre-experience in computer science!

Impactful decisions in design:
- Building Flask App: Flask is lightweight, simple and was taught right in the CS50 courses.
- OpenAI API: according to multiple leaderbords on the web, OpenAI is still leading in the AI race. API is simple and operates on pay-as-you-use. 

Learn more: https://jespereggers.com/epana-ai/

# Explaination of meaningful files and directories
#### `epanaFlask/app.py`
Runs Flask app, all navigation is binded to code placed right there.
This file only works with a variety of packages, such as datetime, json, os, flask and sqlite3.
It connects to the database epana.db and routes  index, chat, models, create_model, size_too_big, new_create_model, 
upload_file, account, change_password, change_tier, login, register, logout and api/model_creator.

#### `epanaFlask/chat_converter.py`
Converts exportet Chats from WhatsApp into training material for OpenAI.
Important information can be extracted due to unified constrains. 
For example, each line is ordered like this: [date] [name of whoever sent message] [message].
It loops through every line and rearranges it into OpenAIs jsonl formatting. 

#### `epanaFlask/epana.db`
Stores users, finetuning-jobs etc.

#### `epanaFlask/finetuning_for_flask.py`
Communication with OpenAI for creating fine-tuned versions of specific LLMs.

#### `epanaFlask/helpers.py`
Generalized functions required from multiple instances, most importantly app.py.

#### `epanaFlask/information.py`
Pulls existing models and finetuning-jobs from OpenAI.

#### `epanaFlask/playground.py`
Runs the actual conversation with OpenAI. (used to be an experimental playground)

#### `epanaFlask/token_checker.py`
Used for cost estimations, basically meassures tokens for calculation.

#### `epanaFlask/setup_epana_db.py`
Creates multiple tables to store in database file for first run:
- input_files: storage for uploaded chat-archieves.
- models: pre-existing and custom made models.
- finetuning-jobs: all currently running training for fine-tuned models.
- output-files: storage for converted chats.
- tiers: list of all assignable tiers (currently free and paid)
- users: storage of all user-accounts

This setup finishes by inserting default values into critical databases.

#### `epanaFlask/file_uploads`
Within this folder, Epana will store temporary files, such as converted version of a WhatsApp chat export.

# Experimental
Some features of the future are not fully implemented yet. 
Works with PayPal (simple and widely used).

#### `other_python_files/payments.py`
This will serve a paid-tier subscription plan to cover heavy API-cost. 

# User Interface
Background to every tab in the current UI.

#### `epanaFlask/templates/chat.html`
The user selects a model (which has previously been created on the models-tab).
Site now features a simple chat interface with dark- and light-green bubbles.

#### `epanaFlask/templates/models.html`
Features option to 
(1) upload a file, which is then being converted into training material formatted according to OpenAI docs.
(2) create a model, which uploads pre-shared training material right to OpenAI, opening a finetuning-job.
Please not that step (2) might take a few minutes to complete.

#### `epanaFlask/templates/account.html`
Each account is linked to an e-mail adress and assigned a tier (which is 'free' by default)
As this service includes possibly heavy API-cost, we built the foundation to indroduced a paid-tier.
Both password and tier are changable. Also works for paid tier, even though an actual payment-system is not yet fully implemented

#### `epanaFlask/templates/logout.html`
Trivial. User can logout.

# Prompting
At this point in german, as model upload only works for german formatted files.

#### Commanding Prompt (german)
"Imitiere ihn, aber nicht deinen Gesprächspartner, durch Ausdruck von Persönlichkeit, Wortwahl."

#### System Prompt (german)
"Du bist [Name]. Lerne zu handeln durch Wortwahl, charakteristische Eigenschaften und Erinnerung an Inhalt
Pleae note that making the fine-tuned AI remember actual content of a conversation has been one of the biggest challenges.

# Next steps
- New character creator
- Introducing paid tier
- upgrading to newer GPT-models
- store conversations, maybe using OpenAI thread-object (therefore not retransmitting entire convo on each request)
- new chat UI
- prompt engineering
