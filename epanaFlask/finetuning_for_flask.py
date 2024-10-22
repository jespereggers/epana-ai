from openai import OpenAI


# Define bcolors manually
class Colors:
    OKGREEN = '\033[92m'
    ENDC = '\033[0m'


def start_finetuning_job(api_key, output_path, verification_path):
    client = OpenAI(api_key=api_key)

    # upload file
    output_file = client.files.create(
        file=open(output_path, "rb"),
        purpose='fine-tune'
    )
    output_file_id = output_file.id
    print(f"{Colors.OKGREEN}file uploaded{Colors.ENDC}")
    print("file_id: ", output_file_id)

    # upload verification file
    verification_file = client.files.create(
        file=open(verification_path, "rb"),
        purpose='fine-tune'
    )
    verification_file_id = verification_file.id

    # create job
    client.fine_tuning.jobs.create(training_file=output_file_id, validation_file=verification_file_id,
                                model="gpt-3.5-turbo")
    print("finetuneJob created")

    # print finetuning jobs
    print("finetuningJobs: ", client.fine_tuning.jobs.list().data[0])
    return client.fine_tuning.jobs.list().data[0]
