import time
import re
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI()
assistant = client.beta.assistants.retrieve(
    assistant_id="asst_PZVM3XAS1O7UtY4IA4F4QwSP"
)
thread = client.beta.threads.create()


def wait_on_run(run, thread):
    while run.status == "queued" or run.status == "in_progress":
        run = client.beta.threads.runs.retrieve(
            thread_id=thread.id,
            run_id=run.id,
        )
        time.sleep(0.5)
    return run


while True:
    content = input("Enter your message : ")
    message = client.beta.threads.messages.create(
        thread_id=thread.id, role="user", content=content
    )

    run = client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=assistant.id,
    )

    wait_on_run(run, thread)

    messages = client.beta.threads.messages.list(
        thread_id=thread.id, order="asc", after=message.id
    )
    response_text = ""
    for message in messages:
        for c in message.content:
            response_text += c.text.value
    clean_text = re.sub("【.*?】", "", response_text)
    print(clean_text)
