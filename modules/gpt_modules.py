import openai
import os

from dotenv import dotenv_values

config = dotenv_values(".env")

openai.organization = config.get('OPENAI_ORGANIZATION')
openai.api_key = config.get('OPENAI_API_KEY')

# openai.organization = os.environ['OPENAI_ORGANIZATION']
# openai.api_key = os.environ['OPENAI_API_KEY']

def gpt_call(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
                    {"role": "user", "content": prompt},
                ]
    )
    output_text = response["choices"][0]["message"]["content"]

    return output_text