import time

from openai import OpenAI


class AssistantManager:
    def __init__(self, api_key, assistant_id):
        self.client = OpenAI(api_key=api_key)
        self.assistant = self.client.beta.assistants.retrieve(assistant_id)

    def handle_message(self, thread_id, user_message):
        self.create_thread_message(thread_id, user_message)
        self.create_run(thread_id)
        return self.get_answer(thread_id)

    def create_thread(self):
        return self.client.beta.threads.create()

    def create_thread_message(self, thread_id, user_message):
        self.client.beta.threads.messages.create(
            thread_id=thread_id,
            role="user",
            content=user_message,
        )

    def create_run(self, thread_id):
        run = self.client.beta.threads.runs.create(
            thread_id=thread_id, assistant_id=self.assistant.id
        )
        while run.status == "queued" or run.status == "in_progress":
            time.sleep(1)
            run = self.client.beta.threads.runs.retrieve(
                thread_id=thread_id, run_id=run.id
            )
        if run.status == "failed":
            raise Exception("Run failed with error: " + run.last_error.message)

    def get_answer(self, thread_id):
        resp = self.client.beta.threads.messages.list(thread_id=thread_id)
        return resp.data[0].content[0].text.value

    def transcribe_audio(self, audio_file_path):
        with open(audio_file_path, "rb") as audio_file:
            return self.client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file,
            ).text
