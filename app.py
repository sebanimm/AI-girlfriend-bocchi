import time
import re
from dotenv import load_dotenv
from openai import OpenAI
import streamlit as st

load_dotenv()

client = OpenAI()
assistant = client.beta.assistants.retrieve(
    assistant_id="asst_PZVM3XAS1O7UtY4IA4F4QwSP"
)


def wait_on_run(run, thread):
    while run.status == "queued" or run.status == "in_progress":
        run = client.beta.threads.runs.retrieve(
            thread_id=thread.id,
            run_id=run.id,
        )
        time.sleep(0.5)
    return run


if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []

st.title("AI 여친 봇치와 대화하기")

st.image("image.png", use_column_width=True)

content = st.text_input("메시지 적기:")

if st.button("봇치에게 메세지 보내기"):
    if content:
        thread = client.beta.threads.create()

        message = client.beta.threads.messages.create(
            thread_id=thread.id, role="user", content=content
        )

        run = client.beta.threads.runs.create(
            thread_id=thread.id,
            assistant_id=assistant.id,
        )

        run = wait_on_run(run, thread)

        messages = client.beta.threads.messages.list(
            thread_id=thread.id, order="asc", after=message.id
        )

        response_text = ""
        for message in messages:
            for c in message.content:
                response_text += c.text.value

        clean_text = re.sub(r"【.*?】", "", response_text)

        st.session_state.chat_history.append(("User", content))
        st.session_state.chat_history.append(("Assistant", clean_text))

for role, message in st.session_state.chat_history:
    if role == "당신":
        st.text_area("당신:", value=message, height=100, key=f"user_{message}")
    else:
        st.text_area("봇치:", value=message, height=100, key=f"assistant_{message}")
