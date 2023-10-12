# WARNING in this file, the openai.FineTuningJob.create() function is used. when called it can
# start a job which will potentially COST MONEY. Use with caution

# TODO: add verification file and start the finetuning job with the verification file

import openai
from openai.cli import bcolors


def start_finetuning_job(api_key, output_path, verification_path):
    openai.api_key = api_key
    # upload file
    file = openai.File.create(
        file=open(output_path, "rb"),
        purpose='fine-tune'
    )
    file_id = file.id
    print(f"{bcolors.OKGREEN}file uploaded{bcolors.ENDC}")
    print("file_id: ", file_id)

    # create job
    openai.FineTuningJob.create(training_file=file_id, model="gpt-3.5-turbo")
    print("finetuneJob created")

    # print fintuningJobs
    print("finetuningJobs: ", openai.FineTuningJob.list().data[0])
    return openai.FineTuningJob.list().data[0]
