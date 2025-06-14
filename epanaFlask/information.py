# Needed it to print the finetuningJobs
import environment as env

from openai import OpenAI


def get_model_ids():
    client = OpenAI(api_key=env.API_KEY)

    model_ids = []
    for entry in client.fine_tuning.jobs.list().data:
        model_ids.append(entry.fine_tuned_model)
    return model_ids


def get_finetuning_job(job_id):
    client = OpenAI(api_key=env.API_KEY)
    job = client.fine_tuning.jobs.retrieve(job_id)
    return job


def get_model_id(job_id):
    client = OpenAI(api_key=env.API_KEY)

    job = client.fine_tuning.jobs.retrieve(job_id)
    return job.fine_tuned_model


def create_thread():
    client = OpenAI(api_key=env.API_KEY)

    empty_thread = client.beta.threads.create()
    return empty_thread


def create_msg(thread_id, role, content):
    client = OpenAI(api_key=env.API_KEY)

    thread_message = client.beta.threads.messages.create(
        thread_id,
        role=role,
        content=content,
    )
    return thread_message
