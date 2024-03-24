
import os
from dotenv import load_dotenv
import logging
from openai import OpenAI
import time


load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_KEY"))


def initialize_thread():
  _thread = client.beta.threads.create();
  return _thread.id

def list_messages(thread_id):
  _messages = client.beta.threads.messages.list(thread_id=thread_id)
  return _messages.data


def await_completion(thread_id, run_id):
  run = client.beta.threads.runs.retrieve(thread_id=thread_id,run_id=run_id)
  while run.status in ['queued', 'in_progress', 'cancelling']:
    time.sleep(1) # Wait for 1 second
    run = client.beta.threads.runs.retrieve(
      thread_id=thread_id,
      run_id=run.id
    )
    
    
def send_message(thread_id, message):
  # await run completion
  _new_message = client.beta.threads.messages.create(thread_id=thread_id, content=message, role="user")
  assistant = client.beta.assistants.retrieve(assistant_id=os.getenv("ASSISTANT_ID")) # type: ignore
  run = client.beta.threads.runs.create(thread_id=thread_id, assistant_id=assistant.id)
  await_completion(thread_id, run.id)
  messages = list_messages(thread_id)
  logging.debug(messages[0])
  return messages[0]


def main():
  print("Starting the conversation")
  thread_id = initialize_thread()
  while (True):
    user_message = input("User: ")
    response = send_message(thread_id, user_message)
    content_block = response.content[0]
    if content_block.type == "text":
      print("Assistant: ", content_block.text.value)
    # elif content_block.type == "image":
    #   print("Assistant: Image received")
    else:
      print("Assistant: Unknown content type")
      
if __name__ == "__main__":
  main()
