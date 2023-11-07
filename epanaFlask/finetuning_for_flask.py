# WARNING in this file, the openai.FineTuningJob.create() function is used. when called it can
# start a job which will potentially COST MONEY. Use with caution

# TODO: add verification file and start the finetuning job with the verification file

import openai
from openai.cli import bcolors


def start_finetuning_job(api_key, output_path, verification_path):
    openai.api_key = api_key
    # upload file
    output_file = openai.File.create(
        file=open(output_path, "rb"),
        purpose='fine-tune'
    )
    output_file_id = output_file.id
    print(f"{bcolors.OKGREEN}file uploaded{bcolors.ENDC}")
    print("file_id: ", output_file_id)

    # upload verification file
    verification_file = openai.File.create(
        file=open(verification_path, "rb"),
        purpose='fine-tune'
    )
    verification_file_id = verification_file.id

    # create job
    openai.FineTuningJob.create(training_file=output_file_id, validation_file=verification_file_id,
                                model="gpt-3.5-turbo")
    print("finetuneJob created")

    # print fintuningJobs
    print("finetuningJobs: ", openai.FineTuningJob.list().data[0])
    return openai.FineTuningJob.list().data[0]
