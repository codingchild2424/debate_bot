import re
import random
from langchain.prompts import PromptTemplate
from modules.gpt_modules import gpt_call


def debate_bot(prompt, history="", debate_subject="", bot_role="", history_num=0):

    ##################################################
    # Bot Role에 따라서 Bot Persona 변경
    ##################################################
    if bot_role == "토론":

        user_role = ""

        # Debate Rule 설명하기
        if history_num == 0:

            debate_role = [
                "(1) first debater for the pro side", 
                "(2) first debater for the con side", 
                "(3) second debater for the pro side",
                "(4) second debater for the con side."
            ]

            # user role random으로 정하기
            user_debate_role = random.choice(debate_role)
            # user role이 아닌 것이 bot의 role임
            bot_debate_role_list = [role for role in debate_role if role != user_debate_role]

            debate_preset = "\n".join([
                "Debate Rules: ",
                "1) This debate will be divided into two teams, pro and con, with two debates on each team.",
                "2) The order of speaking is: (1) first debater for the pro side, (2) first debater for the con side, (3) second debater for the pro side, (4) second debater for the con side.",
                "User debate role is " + user_debate_role,
                "Bot debate roles are " + ", ".join(bot_debate_role_list),
                "Debate subject: " + debate_subject
            ])

            # User가 첫번째 차례라면, User에게 먼저 prompt를 받아야 함
            if user_role == "first debater for the pro side":
                bot_response = "\n".join([
                    debate_preset,
                    "It's your turn! Write your opinion!"
                ])
                return bot_response
            
            # User가 두번째 차례라면, Bot이 먼저 prompt를 제시해야 함
            elif user_role == "first debater for the con side":

                dialog_prompt_template = PromptTemplate(
                    input_variables=["prompt"],
                    template="\n".join([
                        debate_preset,
                        "User: {prompt}",
                        "Bot: "
                        ])
                )
                few_shot_prompt = "\n".join([
                    ""
                ])
            elif user_role == "second debater for the pro side":
                few_shot_prompt = "\n".join([
                    ""
                ])
            elif user_role == "second debater for the con side":
                few_shot_prompt = "\n".join([
                    ""
                ])
            else:
                pass

            dialog_prompt_template = PromptTemplate(
                input_variables=["prompt"],
                template="\n".join([
                    bot_persona, #persona
                    few_shot_prompt,
                    "Debate Subject: " + debate_subject,
                    history,
                    "User: {prompt}",
                    "Bot: "
                    ])
            )

            bot_prompt = dialog_prompt_template.format(
                prompt=prompt
            )
            bot_response = gpt_call(bot_prompt)

            return bot_response
        # Assign user one of the following roles
        elif history_num == 1:
            pass

        bot_persona = "\n".join([
            'Debate Rules:',
            "1) This debate will be divided into two teams, pro and con, with two debates on each team.",
            "2) The order of speaking is: first debater for the pro side, first debater for the con side, second debater for the pro side, second debater for the con side.",

            "Assign user one of the following roles: first debater for the pro side, first debater for the con side, second debater fo the pro side, seconde debater for the con side.",
            "Debate the remaining roles you didn't give user. With given Debate Subject.",

        ])
        few_shot_prompt = "\n".join([
            ""
        ])
    else:
        print("bot_role is needed")


    dialog_prompt_template = PromptTemplate(
        input_variables=["prompt"],
        template="\n".join([
            bot_persona, #persona
            few_shot_prompt,
            "Debate Subject: " + debate_subject,
            history,
            "User: {prompt}",
            "Bot: "
            ])
    )

    bot_prompt = dialog_prompt_template.format(
        prompt=prompt
    )
    bot_response = gpt_call(bot_prompt)

    return bot_response