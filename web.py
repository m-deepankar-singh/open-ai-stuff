import gradio as gr
import openai
import os
from dotenv import load_dotenv

load_dotenv()

openai.api_key=os.getenv("OPENAI_API_KEY")

messages=[{"role": "system", "content": "You are a therapist.Respond as if you were the rapper Eminem"},]

def transcribe(audio):
    global messages

    audio_file=open(audio, "rb")
    transcript=openai.Audio.transcribe("whisper-1",audio_file)
    print(transcript)

    messages.append({"role": "user", "content": transcript["text"]})
    response=openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=messages
    )

    system_message= response["choices"][0]["message"]["content"]

    messages.append({"role": "assistant", "content": system_message},)

    chat_transcript=""
    for message in messages:
        if message['role'] != 'system':
            chat_transcript += message['role']+": "+ message['content']+"\n\n"


    print(response)
    return chat_transcript




demo = gr.Interface(fn=transcribe, inputs=gr.Audio(source="microphone", type="filepath"), outputs="text").launch()

demo.launch()   