import re
import random
from langchain.prompts import PromptTemplate
from modules.gpt_modules import gpt_call


def debate_bot(prompt, history="", debate_subject="", bot_role="", history_num=0):

    print("prompt", prompt)

    ##################################################
    # Bot Role에 따라서 Bot Persona 변경
    ##################################################
    if bot_role == "토론":

        # Debate Rule 설명하기
        if history_num == 0:
            print("history_num", history_num)

            user_role = ""
            bot_response = ""

            debate_role = [
                "first debater for the pro side", 
                "first debater for the con side", 
                "second debater for the pro side",
                "second debater for the con side"
            ]

            # user role random으로 정하기
            user_debate_role = random.choice(debate_role)
            # user role이 아닌 것이 bot의 role임
            bot_debate_role_list = [role for role in debate_role if role != user_debate_role]

            print("user_debate_role", user_debate_role)
            print("bot_debate_role_list", bot_debate_role_list)

            debate_preset = "\n".join([
                "Debate Rules: ",
                "1) This debate will be divided into two teams, pro and con, with two debates on each team.",
                "2) The order of speaking is: first debater for the pro side, first debater for the con side, second debater for the pro side, second debater for the con side.\n",
                "User debate role: " + user_debate_role,
                "Bot debate roles: " + ", ".join(bot_debate_role_list) + "\n",
                "Debate subject: " + debate_subject
            ])

            # User가 첫번째 차례라면, User에게 먼저 prompt를 받아야 함
            if user_debate_role == debate_role[0]:
                #print("user_debate_role", user_debate_role)
                bot_preset = "\n".join([
                    debate_preset + "\n",
                    "It's your turn! Write your opinion!"
                ])
                bot_response = bot_preset
                print("bot_response", bot_response)
                #return bot_response
            
            # User가 두번째 차례라면, Bot이 1번째 차례에 대한 response를 만들고, 사용자의 답변을 받아야 함
            elif user_debate_role == debate_role[1]:

                bot_preset = "\n".join([
                    debate_preset,
                ])

                first_prompt_template = PromptTemplate(
                    input_variables=["prompt"],
                    template="\n".join([
                        bot_preset, #persona
                        "{prompt}",
                        debate_role[0] + ": "
                        ])
                )
                first_bot_prompt = first_prompt_template.format(
                    prompt=""
                )
                first_response = gpt_call(first_bot_prompt)

                bot_response = "\n".join([
                    bot_preset + "\n",
                    "First debater for the pro side: " + first_response + "\n",
                    "It's your turn! Write your opinion!"
                ])

            # User가 세번째 차례라면, Bot이 1, 2번째 차례에 대한 response를 만들고, 사용자의 답변을 받아야 함
            elif user_debate_role == debate_role[2]:

                bot_preset = "\n".join([
                    debate_preset,
                ])
                # first
                first_prompt_template = PromptTemplate(
                    input_variables=["prompt"],
                    template="\n".join([
                        bot_preset, #persona
                        "{prompt}",
                        debate_role[0] + ": ",
                        ])
                )
                first_bot_prompt = first_prompt_template.format(
                    prompt=""
                )
                first_response = gpt_call(first_bot_prompt)

                # second
                second_prompt_template = PromptTemplate(
                    input_variables=["first_prompt"],
                    template="\n".join([
                        bot_preset, #persona
                        debate_role[0] + ": " + "{first_prompt}",
                        debate_role[1] + ": "
                        ])
                )
                second_bot_prompt = second_prompt_template.format(
                    first_prompt=first_response
                )
                second_response = gpt_call(second_bot_prompt)

                bot_response = "\n".join([
                    bot_preset + "\n",
                    "First debater for the pro side: " + first_response + "\n",
                    "First debater for the con side: " + second_response + "\n",
                    "It's your turn! Write your opinion!"
                ])


            elif user_debate_role == debate_role[3]:

                bot_preset = "\n".join([
                    debate_preset,
                ])

                # first
                first_prompt_template = PromptTemplate(
                    input_variables=["prompt"],
                    template="\n".join([
                        bot_preset, #persona
                        "{prompt}",
                        debate_role[0] + ": ",
                        ])
                )
                first_bot_prompt = first_prompt_template.format(
                    prompt=""
                )
                first_response = gpt_call(first_bot_prompt)

                # second
                second_prompt_template = PromptTemplate(
                    input_variables=["first_prompt"],
                    template="\n".join([
                        bot_preset, #persona
                        debate_role[0] + ": " + "{first_prompt}",
                        debate_role[1] + ": "
                        ])
                )
                second_bot_prompt = second_prompt_template.format(
                    first_prompt=first_response
                )
                second_response = gpt_call(second_bot_prompt)

                # third
                third_prompt_template = PromptTemplate(
                    input_variables=["first_prompt", "second_prompt"],
                    template="\n".join([
                        bot_preset, #persona
                        debate_role[0] + ": " + "{first_prompt}",
                        debate_role[1] + ": " + "{second_prompt}",
                        debate_role[2] + ": "
                        ])
                )
                third_bot_prompt = third_prompt_template.format(
                    first_prompt=first_response,
                    second_prompt=second_response
                )
                third_response = gpt_call(third_bot_prompt)

                bot_response = "\n".join([
                    bot_preset + "\n",
                    "First debater for the pro side: " + first_response + "\n",
                    "First debater for the con side: " + second_response + "\n",
                    "Second debater for the pro side: " + third_response + "\n",
                    "It's your turn! Write your opinion!"
                ])

            else:
                pass

        return bot_response

                # dialog_prompt_template = PromptTemplate(
                #     input_variables=["prompt"],
                #     template="\n".join([
                #         bot_persona, #persona
                #         few_shot_prompt,
                #         "Debate Subject: " + debate_subject,
                #         history,
                #         "User: {prompt}",
                #         "Bot: "
                #         ])
                # )

    #         bot_prompt = dialog_prompt_template.format(
    #             prompt=prompt
    #         )
    #         bot_response = gpt_call(bot_prompt)

    #         return bot_response
    #     # Assign user one of the following roles
    #     elif history_num == 1:
    #         pass

    #     bot_persona = "\n".join([
    #         'Debate Rules:',
    #         "1) This debate will be divided into two teams, pro and con, with two debates on each team.",
    #         "2) The order of speaking is: first debater for the pro side, first debater for the con side, second debater for the pro side, second debater for the con side.",

    #         "Assign user one of the following roles: first debater for the pro side, first debater for the con side, second debater fo the pro side, seconde debater for the con side.",
    #         "Debate the remaining roles you didn't give user. With given Debate Subject.",

    #     ])
    #     few_shot_prompt = "\n".join([
    #         ""
    #     ])
    # else:
    #     print("bot_role is needed")


    # dialog_prompt_template = PromptTemplate(
    #     input_variables=["prompt"],
    #     template="\n".join([
    #         bot_persona, #persona
    #         few_shot_prompt,
    #         "Debate Subject: " + debate_subject,
    #         history,
    #         "User: {prompt}",
    #         "Bot: "
    #         ])
    # )

    # bot_prompt = dialog_prompt_template.format(
    #     prompt=prompt
    # )
    # bot_response = gpt_call(bot_prompt)

    # return bot_response