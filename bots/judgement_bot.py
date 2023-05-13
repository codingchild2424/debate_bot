from modules.gpt_modules import gpt_call
from langchain.prompts import PromptTemplate

def debate_judgement(debate_history):

    judgement_prompt = "\n".join([
        "!!Instruction!",
        "You are now the judge of this debate. Evaluate the debate according to the rules below.",
        "Rule 1. Decide between the USER and BOT.",
        "Rule 2. Summarize the debate as a whole and what each debater said.",
        "Rule 3. For each debater, explain what was persuasive and what made the differnce between winning and losing.",
    ])

    judgement_prompt_template = PromptTemplate(
        input_variables=["prompt"],
        template="\n".join([
            debate_history,
            judgement_prompt,
            "Judgement: "
            ])
    )
    judgement_bot_prompt = judgement_prompt_template.format(
            prompt=""
    )
    bot_response = gpt_call(judgement_bot_prompt)
    
    return bot_response