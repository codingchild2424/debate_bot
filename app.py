
import streamlit as st
from streamlit_chat import message
import requests
from time import time
import json
import boto3

from modules.db_modules import get_db, put_item, get_item, get_lastest_item
from modules.gpt_modules import gpt_call
from bots.debate_bot import debate_bot

import os



# DB
dynamodb = get_db()
debate_bot_log_table = dynamodb.Table('debate_bot_log')


###########
# streamlit
###########
st.header("DEBATE BOT")

if 'generated' not in st.session_state:
    st.session_state['generated'] = []

if 'past' not in st.session_state:
    st.session_state['past'] = []


def query(user_id, prompt, debate_subject, bot_role):

    history_list = get_lastest_item(
        table=debate_bot_log_table, 
        name_of_partition_key="user_id",
        value_of_partition_key=user_id,
        )
    
    # history가 없다면,
    if history_list==[]:
        history = ""
        # history가 있다면, [{}, {}]
    else:
        history = ""
        history_dummy_list = []
        for dic in history_list:
            history_dummy_list.append(dic['prompt'])
        
        history = "\n".join(history_dummy_list)


    bot_result = debate_bot(prompt, history, debate_subject, bot_role)

    # put_db
    save_prompt = "\n".join([
        "User: " + prompt, 
        "Cicero Bot: " + bot_result
        ])

    item = {
        'user_id': user_id,
        'prompt': save_prompt,
        'time_stamp': str(time()),
        'debate_subject': debate_subject,
        }

    put_item(debate_bot_log_table, item)
    
    return bot_result

#############################################
# Setting Form
#############################################
if 'debate_topic' not in st.session_state:
    st.session_state.debate_topic = ""

with st.form("first_form"):
    #############################################
    # Debate Theme
    #############################################
    debate_theme =st.selectbox(label='Debate Theme', options=[
        'Education',
        'Sports',
        'Religion',
        'Justice',
        'Pandemic',
        'Politics',
        'Minority',
        'etc'
    ])
    change = st.form_submit_button("Change")

    #############################################
    # Debate Topic
    #############################################
    if debate_theme == "Education":
        topic_list = (
            "THBT college entrance examinations should accept students only on the basis of their academic performance in secondary education.", 
            "THS a world where the government gives cash that individuals can use to freely select their academic preference (including but not limited to school of choice, private academies, and tutoring) instead of funding for public education.",
            "THW abolish all requirements and evaluation criteria in higher education (i.e., attendance, exams, assignments)."
            )
    elif debate_theme == "Sports":
        topic_list = (
            "THBT having star players for team sports do more harm than good to the team.",
            "THR the emphasis on winning a medal in the Olympics as a core symbol of success.",
            "THP a world where sports serves purely entertainment purposes even at the expense of fair play."
        )
    elif debate_theme == "Religion":
        topic_list = (
            "THW, as a religious group/leader, cease attempts at increasing the number of believers and instead prioritize boosting loyalty amongst adherents to the religion.",
            "Assuming feasibility, TH prefers a world where a panel of church leaders would create a universally accepted interpretation of the Bible that the believers would abide by.",
            "THW aggressively crackdown on megachurches."
        )
    elif debate_theme == "Justice":
        topic_list = (
            "In 2050, AI robots are able to replicate the appearance, conversation, and reaction to emotions of human beings. However, their intelligence still does not allow them to sense emotions and feelings such as pain, happiness, joy, and etc.",
            "In the case a human destroys the robot beyond repair, THW charge murder instead of property damage.",
            "THP a world where the criminal justice system’s role is mainly for victim’s vengeance. THW allow prosecutors and victims to veto assigned judges."
        )
    elif debate_theme == "Pandemic":
        topic_list = (
            "During a pandemic, THBT businesses that benefit from the pandemic should be additionally taxed.",
            "THW nullify the effect of medical patents in cases of medical emergencies.",
            "THW ban media content that denies the efficacy of the COVID-19 without substantial evidence."
        )
    elif debate_theme == "Politics":
        topic_list = (
            "Info: The Candle Light Will (촛불민심) is a term derived from the symbolic candle-light protests for the impeachment of the late president Park Geun Hye, commonly used to mean the people’s will to fight against corrupt governments. The Moon administration has frequently referred to the Candle Light Will as the driving force behind its election that grants legitimacy to its policies. THR the ‘candle light will’ narrative in the political discourse of South Korea.",
            "THW impose a cap on the property and income of politicians.",
            "THW give the youth extra votes."
        )
    elif debate_theme == "Minority":
        topic_list = (
            "Context: A prominent member of the LGBT movement has discovered that a very influential politician helping the LGBT movement has been lying about their sexual orientation as being gay when they are straight. THW disclose this information.",
            "THBT the LGBTQIA+ movement should denounce the existence of marriage as opposed to fighting for equal marriage rights.",
            "THBT the LGBTQIA+ movement should condemn the consumption of movies and TV shows that cast straight actors/actresses in non-heterosexual identified roles."
        )
    else:
        topic_list = (
            "THW remove all laws that relate to filial responsibilities.",
            "THW require parents to receive approval from experts in relevant fields before making crucial decisions for their children.",
            "Assuming it is possible to measure the ‘societal danger’ of the fetus in the future, THBT the state should raise infants that pose high levels of threat.",
            "THBT any upper limits on prison sentences for particularly heinous crimes should be abolished.",
            "THW require dating apps to anonymize profile pictures.",
            "THW adopt a Pass/Fail grading system for students who suffer from mental health problems (e.g. depression, bipolar disorder, etc.).",
            "THBT South Korean feminist movements should reject feminist icons that are adversarial and embody violence.",
            "THBT freedom of speech should be considered obsolete.",
            "THR the narrative that eccentric personalities are essential to create art.",
            "THW allow parents of severely mentally disabled children to medically impede their children's physical growth.",
            "THR the emphasis on longevity in relationships.",
            "Assuming feasibility, THW choose to continuously relive the happiest moment of one’s life."
        )

    debate_topic = st.selectbox(
        '2. Choose your Topic',
        topic_list
        )
    
    #############################################
    # Role of Bot
    #############################################
    bot_role_list = (
        "주제 정의",
        "POI 연습",
        "역할 추천",
        "주장 비판",
        "토론"
    )

    bot_role = st.selectbox(
        '3. Choose Role of Bot',
        bot_role_list
    )
    
    submitted = st.form_submit_button('Send')



#############################################
# Chatbot
#############################################

if 'user_id' not in st.session_state:
    st.session_state.user_id = ""

if 'debate_subject' not in st.session_state:
    st.session_state.debate_subject = ""

with st.form('form', clear_on_submit=True):
    user_id = st.text_input(
        "Enter Your User ID", 
        st.session_state.user_id, # For remain the id
        key='user_id'
        )
    user_input = st.text_input(
        'Message', 
        '', 
        key='input'
        )
    submitted = st.form_submit_button('Send')


if submitted and user_input:

    output = query(user_id, user_input, debate_topic, bot_role)

    st.session_state.past.append(user_input)
    st.session_state.generated.append(output)

if st.session_state['generated']:
    for i in range(len(st.session_state['generated'])-1, -1, -1):
        message(
            st.session_state['past'][i], 
            is_user=True, 
            key=str(i) + '_user'
            )
        message(
            st.session_state["generated"][i], 
            key=str(i),
            #avatar_style="Fun Emoji"
            )