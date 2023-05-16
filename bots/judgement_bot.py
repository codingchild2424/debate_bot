from modules.gpt_modules import gpt_call
from langchain.prompts import PromptTemplate

def debate_judgement(
        judgement_who, 
        user_debate_history, 
        bot_debate_history
        ):

    if judgement_who == 'User-Bot':

        judgement_prompt_preset = "\n".join([
            "!!Instruction!",
            "You are now the judge of this debate. Evaluate the debate according to the rules below.",
            "Rule 1. Decide between the USER and BOT.",
            "Rule 2. Summarize the debate as a whole and what each debater said.",
            "Rule 3. For each debater, explain what was persuasive and what made the differnce between winning and losing.",
        ])

        judgement_prompt = "\n".join([
                judgement_prompt_preset,
                "User: " + user_debate_history,
                "Bot: " + bot_debate_history,
                "Judgement must be logical with paragraphs.",
                "Do not show Rule",
                "Write judgement below.",
                "Judgement: "
                ])

    elif judgement_who == 'User':

        judgement_prompt_preset = "\n".join([
            "!!Instruction!",
            "You are now the judge of this debate. Evaluate the debate according to the rules below.",
            "Rule 1. Summarize the debate as a whole and each said.",
            "Rule 2. Explain what was persuasive and what made the differnce between winning and losing.",
        ])

        judgement_prompt = "\n".join([
                judgement_prompt_preset,
                "User: " + user_debate_history,
                "Judgement must be logical with paragraphs.",
                "Do not show Rule",
                "Write judgement below.",
                "Judgement: "
                ])

    elif judgement_who == 'Bot':

        judgement_prompt_preset = "\n".join([
            "!!Instruction!",
            "You are now the judge of this debate. Evaluate the debate according to the rules below.",
            "Rule 1. Summarize the debate as a whole and each said.",
            "Rule 2. Explain what was persuasive and what made the differnce between winning and losing.",
        ])

        judgement_prompt = "\n".join([
                judgement_prompt_preset,
                "Bot: " + bot_debate_history,
                "Judgement must be logical with paragraphs.",
                "Do not show Rule",
                "Write judgement below.",
                "Judgement: "
                ])

    bot_response = gpt_call(judgement_prompt)
    
    return bot_response