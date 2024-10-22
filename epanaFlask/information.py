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
