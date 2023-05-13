from dotenv import dotenv_values
import openai
import os
from langchain.prompts import PromptTemplate
from modules.gpt_modules import gpt_call
import random

"""
apt-get update
apt-get install ffmpeg
"""

config = dotenv_values(".env")

openai.organization = config.get('OPENAI_ORGANIZATION')
openai.api_key = config.get('OPENAI_API_KEY')

def debate_in_sound(audio):
    os.rename(audio, audio + '.wav')
    file = open(audio + '.wav', "rb")

    # user_words
    user_prompt = openai.Audio.transcribe("whisper-1", file).text

    print("**************************************")
    print("user_audio transcription", user_prompt)
    print("**************************************")

    # 일단 테스트를 위해 고정함
    debate_subject = "In 2050, AI robots are able to replicate the appearance, conversation, and reaction to emotions of human beings. However, their intelligence still does not allow them to sense emotions and feelings such as pain, happiness, joy, and etc."

    debate_role = [
            "pro side", 
            "con side",
        ]
    user_debate_role = random.choice(debate_role)
    bot_debate_role = "".join([role for role in debate_role if role != user_debate_role])

    debate_preset = "\n".join([
            "Debate Rules: ",
            "1) This debate will be divided into pro and con",
            "2) You must counter user's arguments",
            "3) Answer logically with an introduction, body, and conclusion.\n", #add this one.
            "User debate role: " + user_debate_role,
            "Bot debate roles: " + bot_debate_role + "\n",
            "Debate subject: " + debate_subject
        ])
    
    prompt_template = PromptTemplate(
                input_variables=["prompt"],
                template="\n".join([
                    debate_preset, #persona
                    "User: {prompt}",
                    "Bot: "
                    ])
            )
    bot_prompt = prompt_template.format(
                prompt=user_prompt
            )
    response = gpt_call(bot_prompt)

    return response


def transcribe(audio):
    os.rename(audio, audio + '.wav')
    file = open(audio + '.wav', "rb")

    result = openai.Audio.transcribe("whisper-1", file).text

    return result


# gr.Interface(
#     title = 'Whisper Audio to Text with Speaker Recognition', 
#     fn=debate,
#     inputs=[
#         gr.inputs.Audio(source="microphone", type="filepath"),
#         #gr.inputs.Number(default=2, label="Number of Speakers")
#     ],
#     outputs="text"
#   ).launch()