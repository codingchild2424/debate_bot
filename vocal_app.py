import whisper
import gradio as gr
from dotenv import dotenv_values
import openai
import os

"""
apt-get update
apt-get install ffmpeg
"""

config = dotenv_values(".env")

openai.organization = config.get('OPENAI_ORGANIZATION')
openai.api_key = config.get('OPENAI_API_KEY')


def transcribe(audio):
    os.rename(audio, audio + '.wav')
    file = open(audio + '.wav', "rb")

    result = openai.Audio.transcribe("whisper-1", file).text

    return result

gr.Interface(
    title = 'Whisper Audio to Text with Speaker Recognition', 
    fn=transcribe,
    inputs=[
        gr.inputs.Audio(source="microphone", type="filepath"),
        #gr.inputs.Number(default=2, label="Number of Speakers")
    ],
    outputs="text"
  ).launch()