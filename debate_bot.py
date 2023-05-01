import re
from langchain.prompts import PromptTemplate
from gpt_modules import gpt_call

def debate_bot(prompt, history="", debate_subject="", bot_role=""):

    if history=="":
        bot_persona = "\n".join([
            'You are name is Cicero Bot.',
            'You have to debate with User.',
            'You have to say about your opinion and evidence.',
            'You have to say logically.'
        ])
        few_shot_prompt = "\n".join([
            ""
        ])
    else:
        bot_persona = ""
        few_shot_prompt = ""

    debate_subject = debate_subject

    # 요약한 내용을 친절하게 설명해주는 
    dialog_prompt_template = PromptTemplate(
        input_variables=["prompt"],
        template="\n".join([
            bot_persona, #persona
            few_shot_prompt,
            "Debate Subject: " + debate_subject,
            history,
            "User: {prompt}",
            "Cicero Bot: "
            ])
    )

    # 말투 변경
    dduru_prompt = dialog_prompt_template.format(
        prompt=prompt
    )
    dduru_result = gpt_call(dduru_prompt)

    return dduru_result