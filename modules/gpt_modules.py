import openai
import streamlit as st

from dotenv import dotenv_values

config = dotenv_values(".env")

if config:
    openai.organization = config.get('OPENAI_ORGANIZATION')
    openai.api_key = config.get('OPENAI_API_KEY')
else:
    openai.organization = st.secrets['OPENAI_ORGANIZATION']
    openai.api_key = st.secrets['OPENAI_API_KEY']


def gpt_call(prompt, role="user"):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
                    {"role": role, "content": prompt},
                ]
    )
    output_text = response["choices"][0]["message"]["content"]

    return output_text


def gpt_call_context(messages):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )
    output_text = response["choices"][0]["message"]["content"]

    # raise RuntimeError
    return output_text