import os
from dotenv import load_dotenv
import logging
from openai import OpenAI
import time


class Assistant:
    def __init__(self, api_key=None, assistant_id=None):
        load_dotenv()
        if not api_key and not os.getenv("OPENAI_KEY"):
            raise ValueError("OPENAI_KEY not found in .env file")
        if not assistant_id and not os.getenv("ASSISTANT_ID"):
            raise ValueError("ASSISTANT_ID not found in .env file")

        self.client = OpenAI(api_key=os.getenv("OPENAI_KEY"), max_retries=3)
        self.thread_id = self.initialize_thread()

    def initialize_thread(self):
        _thread = self.client.beta.threads.create()
        logging.debug(_thread)
        return _thread.id

    def list_messages(self):
        _messages = self.client.beta.threads.messages.list(thread_id=self.thread_id)
        logging.debug(_messages.data)
        return _messages.data

    def send_message(self, message):
        # await run completion
        self.client.beta.threads.messages.create(
            thread_id=self.thread_id, content=message, role="user"
        )
        assistant = self.client.beta.assistants.retrieve(assistant_id=os.getenv("ASSISTANT_ID"))  # type: ignore
        run = self.client.beta.threads.runs.create(
            thread_id=self.thread_id, assistant_id=assistant.id
        )
        self.await_completion(run.id)
        messages = self.list_messages()
        return messages[0]

    def await_completion(self, run_id):
        run = self.client.beta.threads.runs.retrieve(
            thread_id=self.thread_id, run_id=run_id
        )
        while run.status in ["queued", "in_progress", "cancelling"]:
            time.sleep(1)
            run = self.client.beta.threads.runs.retrieve(
                thread_id=self.thread_id, run_id=run.id
            )
