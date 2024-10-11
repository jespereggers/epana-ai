import openai

# Define bcolors manually
class Colors:
    OKGREEN = '\033[92m'
    ENDC = '\033[0m'

def start_finetuning_job(api_key, output_path, verification_path):
    openai.api_key = api_key
    # upload file
    output_file = openai.File.create(
        file=open(output_path, "rb"),
        purpose='fine-tune'
    )
    output_file_id = output_file.id
    print(f"{Colors.OKGREEN}file uploaded{Colors.ENDC}")
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

    # print finetuning jobs
    print("finetuningJobs: ", openai.FineTuningJob.list().data[0])
    return openai.FineTuningJob.list().data[0]
1