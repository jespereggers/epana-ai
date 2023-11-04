# Needed it to print the finetuningJobs

import openai

API_KEY = "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"

openai.api_key = API_KEY

for entry in openai.FineTuningJob.list().data:
    print(entry)
    print(entry["fine_tuned_model"])


def get_model_ids():
    model_ids = []
    for entry in openai.FineTuningJob.list().data:
        model_ids.append(entry["fine_tuned_model"])
    return model_ids


def finetuning_job_succeded(api_key, job_id):
    openai.api_key = api_key
    job = openai.FineTuningJob.retrieve(job_id)
    return job["status"] == "succeeded"


def get_model_id(api_key, job_id):
    openai.api_key = api_key
    job = openai.FineTuningJob.retrieve(job_id)
    return job["fine_tuned_model"]
