# WARNING in this file, the openai.FineTuningJob.create() function is used. when called it can
# start a job which will potentially COST MONEY. Use with caution and read the instructions provided
# in the terminal

import openai
from openai.cli import bcolors

API_KEY = "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"

# data paths for quick adjustments
TRAINING_PATH = "output.jsonl"
VERIFICATION_PATH = "verification.jsonl"


def start_finetuning_job(api_key, output_path, verification_path):
    openai.api_key = api_key
    upload_file = input("Press 'y' to upload file to openAi server.\n")
    # upload file
    if upload_file == 'y':
        file = openai.File.create(
            file=open(output_path, "rb"),
            purpose='fine-tune'
        )
        file_id = file.id
        print(f"{bcolors.OKGREEN}file uploaded{bcolors.ENDC}")
        print("file_id: ", file_id)

        # file id file-3mtXXYfRjFnmLn6ekpOrE28e
        # create job
        create_job = input(f"Press 'y' to create finetuneJob.{bcolors.WARNING} COULD COST MONEY!{bcolors.ENDC}\n")
        if create_job == 'y':
            openai.FineTuningJob.create(training_file=file_id, model="gpt-3.5-turbo")
            print("finetuneJob created")
        else:
            print(f"{bcolors.OKBLUE}finetuneJob not created{bcolors.ENDC}")
    else:
        print(f"{bcolors.OKBLUE}file not uploaded{bcolors.ENDC}")

    # print fintuningJobs
    print("finetuningJobs: ", openai.FineTuningJob.list().data[0])


if __name__ == '__main__':
    start_finetuning_job(API_KEY, TRAINING_PATH, VERIFICATION_PATH)
