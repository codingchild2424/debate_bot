import streamlit as st
import numpy as np
import pprint
import time

from decimal import Decimal
from gtts import gTTS
from collections import Counter
from streamlit_chat import message
from audiorecorder import audiorecorder

# internal modules
from bots.judgement_bot import debate_judgement
from modules.db_modules import get_db, put_item, get_all_items, get_lastest_item
from modules.gpt_modules import gpt_call, gpt_call_context
from modules.whisper_modules import whisper_transcribe
from modules.setting_modules import blockPrint

#########################################################
# Disabled Console print
#########################################################
blockPrint()

#########################################################
# Page Configurations
#########################################################
st.set_page_config(page_title="Debate With GPT : DEBO")

#########################################################
# GET DB
#########################################################
dynamodb = get_db()

#########################################################
# Time Stamp
#########################################################
tm = time.localtime()
time_stamp = time.strftime('%Y-%m-%d %I:%M:%S %p', tm)

#########################################################
# Initialize session state variables
#########################################################
if "page" not in st.session_state:
    st.session_state.page = "Page 1"

if "topic" not in st.session_state:
    st.session_state.topic = "None"

if "user_id" not in st.session_state:
    st.session_state.user_id = ""

if "case1" not in st.session_state:
    st.session_state.case1 = ""

if "case2" not in st.session_state:
    st.session_state.case2 = ""

if "case3" not in st.session_state:
    st.session_state.case3 = ""

if "page2_tab" not in st.session_state:
    st.session_state.page2_tab = "tab1"

if "ask_gpt_prev_response" not in st.session_state:
    st.session_state.ask_gpt_prev_response = ""

if "total_debate_history" not in st.session_state:
    st.session_state.total_debate_history = []

if "user_debate_history" not in st.session_state:
    st.session_state.user_debate_history = []

if "bot_debate_history" not in st.session_state:
    st.session_state.bot_debate_history = []

if "pros_and_cons" not in st.session_state:
    st.session_state.pros_and_cons = ""

if "start_time" not in st.session_state:
    st.session_state.start_time = time.time()

if "end_time" not in st.session_state:
    st.session_state.end_time = time.time()

if "debate_time" not in st.session_state:
    st.session_state.debate_time = 0

if "judgement_result" not in st.session_state:
    st.session_state.judgement_result = ""

if "pre_audio" not in st.session_state:
    st.session_state.pre_audio = np.array([])

if "disabled" not in st.session_state:
    st.session_state.disabled = True

# for db session number
if "session_num" not in st.session_state:
    st.session_state.session_num = 0

#########################################################
# Page Controller
#########################################################
def page_1_2_controller():
    st.session_state.page = "Page 2"
    
def page_2_4_controller():
    st.session_state.page = "Page 4"

# def page_3_4_controller():
#     st.session_state.page = "Page 4"

def page_4_5_controller():
    st.session_state.page = "Page 5"

def page_5_6_controller():
    st.session_state.page = "Page 6"

# def page_2_7_controller():
#     st.session_state.page = "Page 7"

def page_n_1_controller():
    st.session_state.page = "Page 1"

def page2_tab_controller():
    st.session_state.page2_tab = "tab2"

#########################################################
# Page 1
#########################################################
def validate_user_id(id_input):
    table = dynamodb.Table('DEBO_user')
    users_set = get_all_items(table, 'user_id')
    if id_input in users_set:
        return True
    else:
        return False

def save_info(user_id):
    # You can add the code to save the submitted info (e.g., to a database)
    st.session_state.user_id = user_id
    
    #########################################################
    # Session Update
    #########################################################
    debate_setting = get_lastest_item(
        table=dynamodb.Table('DEBO_debate_setting'),
        name_of_partition_key="user_id",
        value_of_partition_key=st.session_state.user_id,
        limit_num=1
    )
    # Session이 없다면, 0으로 초기화
    if not debate_setting:
        st.session_state.session_num = 0
    # User의 이전 기록에서 Session이 있다면, Session Number를 가져오고 갱신함
    else:
        st.session_state.session_num = debate_setting[0]['session_num']

def page1():
    st.header('User Info')
    user_input = st.text_input(
        label='User ID',
        max_chars=100,
        placeholder="Enter user ID",
    )
    message = st.empty()
    
    if user_input:
        if validate_user_id(user_input):
            save_info(user_input)
            message.success('User ID successfully verified!', icon="✅")
            st.session_state.disabled = False
        else:
            message.error('Please fill in correct User ID', icon="🚨")
            st.session_state.disabled = True
    else:
        st.session_state.disabled = True

    st.button(
        label='Next',
        type='primary',
        disabled=st.session_state.disabled,
        on_click=page_1_2_controller
    )
#########################################################
# Page 2
#########################################################
def page2():
    _, _, pre, home  = st.columns([5, 5, 1, 1])
    with pre:
        st.button("🔙", on_click=page_n_1_controller, use_container_width=True)
    with home:
        st.button("🔝", on_click=page_n_1_controller, use_container_width=True)

    st.header("Choose Option")
    option_result = st.selectbox("Choose your option", ["Total Debate", "Evaluation Only & Analyzing Utterances"])

    # add controller
    if option_result == "Total Debate":
        page_control_func = page_2_4_controller
        st.session_state.disabled = False
    elif option_result == "Evaluation Only & Analyzing Utterances":
        st.info('Sorry:( This function will be developed soon.', icon="ℹ️")
        page_control_func = page_1_2_controller
        st.session_state.disabled = True

    st.button(
        label='Next',
        type='primary',
        disabled=st.session_state.disabled,
        on_click=page_control_func,
    )

#########################################################
# Page 3
#########################################################
# def page3():
#     debate_history = get_lastest_item(
#             table=dynamodb.Table('DEBO_debate_setting'),
#             name_of_partition_key="user_id",
#             value_of_partition_key=st.session_state.user_id,
#             #TODO 전체 보여줄 개수 설정
#             limit_num=10
#         )

#     if not debate_history:
#         st.info('There is no previous debate history', icon="ℹ️")

#     _, _, pre, home  = st.columns([5, 5, 1, 1])
#     with pre:
#         st.button("🔙", on_click=page_1_2_controller, use_container_width=True)
#     with home:
#         st.button("🔝", on_click=page_n_1_controller, use_container_width=True)
#     st.header("Debate History")

#     st.button(
#         label=f'🚀 Start new debate',
#         type='primary',
#         on_click=page_3_4_controller
#     )
#     st.write("_"*50)

#     num_history = len(debate_history)
#     for i in range(num_history):
#         with st.container():
#             st.write(f"#### {i + 1}")
#             st.write(f"Debate Thema : {debate_history[i]['debate_theme']}")
#             st.write(f"Debate Topic : {debate_history[i]['debate_topic']}")
#             st.write(f"Case 1 : {debate_history[i]['case1']}")
#             st.write(f"Case 2 : {debate_history[i]['case2']}")
#             st.write(f"Case 3 : {debate_history[i]['case3']}")
#             st.write(f"Created at : {debate_history[i]['time_stamp']}")
#             st.button(
#                 label='Continue this dabate',
#                 key=str(i),
#                 on_click=page_4_5_controller
#             )
#             st.write("_"*50)

#########################################################
# Page 4
#########################################################
def store_debate_data(checked, case1, case2, case3):
    if checked:
        st.session_state.case1, st.session_state.case2, st.session_state.case3 = "", "", ""
    if not checked:
        st.session_state.case1, st.session_state.case2, st.session_state.case3 = case1, case2, case3

    put_item(
        table=dynamodb.Table('DEBO_debate_setting'),
        item={
            'user_id': st.session_state.user_id,
            'time_stamp': time_stamp,
            'debate_theme': st.session_state.debate_theme,
            'debate_topic': st.session_state.topic,
            'case1': st.session_state.case1,
            'case2': st.session_state.case2,
            'case3': st.session_state.case3,
            'session_num': st.session_state.session_num,
            }
    )

def page4():
    #########################################################
    # Tab 1 - Total Debate (토론 준비 -> 연습 -> 평가)
    #########################################################

    _, _, pre, home  = st.columns([5, 5, 1, 1])
    with pre:
        st.button("🔙", on_click=page_1_2_controller, use_container_width=True)
    with home:
        st.button("🔝", on_click=page_n_1_controller, use_container_width=True)

    st.header("Total Debate")
    debate_themes = ['Education','Sports','Religion','Justice','Pandemic','Politics','Minority','etc']

    st.subheader("1. Theme")
    st.session_state.debate_theme = st.selectbox("Choose your debate theme", debate_themes)

    if st.session_state.debate_theme == 'Education':
        topic_list = [
            "THBT college entrance examinations should accept students only on the basis of their academic performance in secondary education.", 
            "THS a world where the government gives cash that individuals can use to freely select their academic preference (including but not limited to school of choice, private academies, and tutoring) instead of funding for public education.",
            "THW abolish all requirements and evaluation criteria in higher education (i.e., attendance, exams, assignments)."
            ]
    elif st.session_state.debate_theme == 'Sports':
        topic_list = [
            "THBT having star players for team sports do more harm than good to the team.",
            "THR the emphasis on winning a medal in the Olympics as a core symbol of success.",
            "THP a world where sports serves purely entertainment purposes even at the expense of fair play."
            ]
    elif st.session_state.debate_theme == 'Religion':
        topic_list = [
            "THW, as a religious group/leader, cease attempts at increasing the number of believers and instead prioritize boosting loyalty amongst adherents to the religion.",
            "Assuming feasibility, TH prefers a world where a panel of church leaders would create a universally accepted interpretation of the Bible that the believers would abide by.",
            "THW aggressively crackdown on megachurches."
            ]
    elif st.session_state.debate_theme == 'Justice':
        topic_list = [
            "In 2050, AI robots are able to replicate the appearance, conversation, and reaction to emotions of human beings. However, their intelligence still does not allow them to sense emotions and feelings such as pain, happiness, joy, and etc.",
            "In the case a human destroys the robot beyond repair, THW charge murder instead of property damage.",
            "THP a world where the criminal justice system’s role is mainly for victim’s vengeance. THW allow prosecutors and victims to veto assigned judges."
            ]
    elif st.session_state.debate_theme == 'Pandemic':
        topic_list = [
            "During a pandemic, THBT businesses that benefit from the pandemic should be additionally taxed.",
            "THW nullify the effect of medical patents in cases of medical emergencies.",
            "THW ban media content that denies the efficacy of the COVID-19 without substantial evidence."
            ]
    elif st.session_state.debate_theme == 'Politics':
        topic_list = [
            "Info: The Candle Light Will (촛불민심) is a term derived from the symbolic candle-light protests for the impeachment of the late president Park Geun Hye, commonly used to mean the people’s will to fight against corrupt governments. The Moon administration has frequently referred to the Candle Light Will as the driving force behind its election that grants legitimacy to its policies. THR the ‘candle light will’ narrative in the political discourse of South Korea.",
            "THW impose a cap on the property and income of politicians.",
            "THW give the youth extra votes."
            ]
    elif st.session_state.debate_theme == 'Minority':
        topic_list = [
            "Context: A prominent member of the LGBT movement has discovered that a very influential politician helping the LGBT movement has been lying about their sexual orientation as being gay when they are straight. THW disclose this information.",
            "THBT the LGBTQIA+ movement should denounce the existence of marriage as opposed to fighting for equal marriage rights.",
            "THBT the LGBTQIA+ movement should condemn the consumption of movies and TV shows that cast straight actors/actresses in non-heterosexual identified roles."
            ]
    else:
        topic_list = [
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
            ]

    st.subheader("2. Topic")
    topic = st.session_state.topic = st.selectbox(
        label="Choose your topic",
        options=topic_list,
        format_func=lambda x: x[:35] + "...",
        # help="This is help message",
    )
    st.write("> Topic : ", topic)

    st.subheader("3. Side")
    st.session_state.pros_and_cons = st.selectbox("Choose your Side (Pros and Cons)", ["Pros", "Cons"])

    st.subheader("4. Cases")
    st.caption('📢 These are just a tool to help you structure your thoughts on the content and does not reflect the actual discussion.')
    checked = st.checkbox(
        label="If you Don't need to write this 3 cases, Please check",
        key="disabled",
    )
    #########################################################
    # Case도 세션에 저장
    #########################################################
    case1 = st.text_area(
        label="Write a Case 1",
        placeholder="Each case should be consisted of opinion, reasoning, and example.",
        height=150,
        disabled=st.session_state.disabled
        )
    case2 = st.text_area(
        label="Write a Case 2",
        placeholder="Each case should be consisted of opinion, reasoning, and example.",
        height=150,
        disabled=st.session_state.disabled
    )
    case3 = st.text_area(
        label="Write a Case 3",
        placeholder="Each case should be consisted of opinion, reasoning, and example.",
        height=150,
        disabled=st.session_state.disabled
    )
    case_error_message = st.empty()
    
    st.write("*" * 50)

    # Save the data to database
    start = st.button(
        label="Start Debate",
        type='primary',
        on_click=store_debate_data,
        args=(checked, case1, case2, case3)
        )

    def validate_case(error_message):
        if not st.session_state.case1 or not st.session_state.case2 or not st.session_state.case3:
            error_message.error("Please fill out above all", icon="🚨")
            return False
        else:
            return True

    if start:
        if checked:
            page_4_5_controller()
            st.experimental_rerun()
        else:
            if validate_case(case_error_message):
                page_4_5_controller()
                st.experimental_rerun()

    #########################################################
    # Ask to GPT
    #########################################################
    with st.sidebar:
        st.sidebar.title('Ask to GPT')
        user_input = st.sidebar.text_area(
            label="Question", 
            placeholder="Input text here",
            height=100)
        output = st.sidebar.button("Ask")
        error_message = st.empty()
        if output:
            if not user_input:
                error_message.error("Please enter your question")
                result = st.session_state.ask_gpt_prev_response
            else:
                try:
                    result = gpt_call(user_input)
                    st.session_state.ask_gpt_prev_response = result
                except:
                    st.warning('Chat-GPT Error : The engine is currently overloaded. Please click "Rerun" button below.', icon="⚠️")
                    time.sleep(1)
                    rerun = st.button(label="Rerun", type="primary")
                    if rerun:
                        st.experimental_rerun()
                    st.stop()

                # save user_prompt and bot_response to database
                put_item(
                    table=dynamodb.Table('DEBO_gpt_ask'),
                    item={
                        'user_id': st.session_state.user_id,
                        'time_stamp': time_stamp,
                        'user_prompt': user_input,
                        'bot_response': result,
                        'session_num': st.session_state.session_num,
                    }
                )

        else:
            result = st.session_state.ask_gpt_prev_response

        st.sidebar.text_area(
            label="Answer", 
            placeholder="(Answer will be shown here)",
            value=result,
            height=400)

#########################################################
# Page5
#########################################################

def generate_response(prompt):
    if len(prompt.split()) < 5:
        response = "Please speak longer!"
    else:
        try:
            response = gpt_call_context(st.session_state['total_debate_history'])
            st.session_state['user_debate_history'].append(prompt)
            st.session_state['total_debate_history'].append({"role": "user", "content": prompt})
            st.session_state['bot_debate_history'].append(response)
            st.session_state['total_debate_history'].append({"role": "assistant", "content": response})
            return response
        except:
            raise RuntimeError("ChatGPT API Error")

def execute_stt(audio):
    # audio 기록 누적
    #user_audio_path = "audio/" + str(st.session_state.user_id) + "_" + str(st.session_state.session_num) + "_" + str(time.time()) + ".wav"
    # audio 기록을 누적하고 싶지 않다면
    user_audio_path = "audio/audio.wav"

    wav_file = open(user_audio_path, "wb")
    wav_file.write(audio.tobytes())

    try:
        user_input = whisper_transcribe(wav_file)
        wav_file.close()
        return user_input
    except:
        raise RuntimeError("Whisper API Error")

def page5():

    # time
    st.session_state.start_time = time.time()

    #########################################################
    # Ask to GPT
    #########################################################
    with st.sidebar:
        st.sidebar.title('Ask to GPT')
        user_input = st.sidebar.text_area(
            label="Question", 
            placeholder="Input text here",
            height=100)
        output = st.sidebar.button("Ask")
        error_message = st.empty()
        if output:
            if not user_input:
                error_message.error("Please enter your question")
                result = st.session_state.ask_gpt_prev_response
            else:
                try:
                    result = gpt_call(user_input)
                    st.session_state.ask_gpt_prev_response = result
                except:
                    st.warning('Chat-GPT Error : The engine is currently overloaded. Please click "Rerun" button below.', icon="⚠️")
                    time.sleep(1)
                    rerun = st.button(label="Rerun", type="primary")
                    if rerun:
                        st.experimental_rerun()
                    st.stop()
                
                put_item(
                    table=dynamodb.Table('DEBO_gpt_ask'),
                    item={
                        'user_id': st.session_state.user_id,
                        'time_stamp': time_stamp,
                        'user_prompt': user_input,
                        'bot_response': result,
                        'session_num': st.session_state.session_num,
                    }
                )
        else:
            result = st.session_state.ask_gpt_prev_response

        st.sidebar.text_area(
            label="Answer", 
            placeholder="(Answer will be shown here)",
            value=result,
            height=400)

    # default system prompt settings
    if not st.session_state['total_debate_history']:

        # bot role, pros and cons
        if st.session_state.pros_and_cons == "Pros":
            bot_role = "Cons"
        elif st.session_state.pros_and_cons == "Cons":
            bot_role = "Pros"
        else:
            bot_role = "(Not yet Determined)"

        debate_preset = "\n".join([
            "Debate Rules: ",
            "1) This debate will be divided into two teams, pro and con, with two debates on each team.",
            "2) The order of speaking is: first debater for the pro side, first debater for the con side, second debater for the pro side, second debater for the con side.",
            "3) Answer logically with an introduction, body, and conclusion.",
            "4) Your role : " + bot_role + " side debator",
            "5) Debate subject: " + st.session_state['topic'],
        ])
        first_prompt = "Now we're going to start. Summarize the subject and your role. And ask user ready to begin."

        try:
            response = gpt_call(debate_preset + "\n" + first_prompt, role="system")
        except:
            st.warning('Chat-GPT Error : The engine is currently overloaded. Please click "Rerun" button below.', icon="⚠️")
            time.sleep(1)
            rerun = st.button(label="Rerun", type="primary")
            if rerun:
                st.experimental_rerun()
            st.stop()
        
        st.session_state['total_debate_history'].append({"role": "system", "content": debate_preset})
        st.session_state['total_debate_history'].append({"role": "assistant", "content": response})
        st.session_state['bot_debate_history'].append(response)

    _, _, pre, home  = st.columns([5, 5, 1, 1])
    with pre:
        st.button("🔙", on_click=page_2_4_controller, use_container_width=True)
    with home:
        st.button("🔝", on_click=page_n_1_controller, use_container_width=True)

    # container for chat history
    response_container = st.container()
    # Chat-GPT & Whisper api error handling
    openai_error_bottom = st.empty()
    # container for text box
    container = st.container()
    reload = False

    with container:
        with st.form(key='my_form', clear_on_submit=True):
            user_input = None
            # record voice
            audio = audiorecorder("⏺️ Click to record", "⏹️ Recording...")
            if np.array_equal(st.session_state['pre_audio'], audio):
                audio = np.array([])

            submit_button = st.form_submit_button(label='💬 Send')
            send_error_message = st.empty()
        
        #if submit_button and user_input:
        if submit_button:
            if audio.any():
                try:
                    user_input = execute_stt(audio)
                except:
                    openai_error_bottom.warning('Whisper Error : The engine is currently overloaded. Please click "Rerun" button below.', icon="⚠️")
                    time.sleep(1)
                    rerun = st.button(label="Rerun", type="primary")
                    reload = True
                    if rerun:
                        st.experimental_rerun()
                    st.stop()
                try :
                    response = generate_response(user_input)
                except:
                    openai_error_bottom.warning('Chat-GPT Error : The engine is currently overloaded. Please click "Rerun" button below.', icon="⚠️")
                    time.sleep(1)
                    rerun = st.button(label="Rerun", type="primary")
                    reload = True
                    if rerun:
                        st.experimental_rerun()
                    st.stop()
                st.session_state['pre_audio'] = audio

                debate_main_latest_data = get_lastest_item(
                    table=dynamodb.Table('DEBO_debate_main'),
                    name_of_partition_key="user_id",
                    value_of_partition_key=st.session_state.user_id,
                    limit_num=1
                )
                if not debate_main_latest_data:
                    turn_num = 0
                else:
                    turn_num = debate_main_latest_data[0]['turn_num']

                put_item(
                    table=dynamodb.Table('DEBO_debate_main'),
                    item={
                        'user_id': st.session_state.user_id,
                        'time_stamp': time_stamp,
                        'session_num': st.session_state.session_num,
                        'bot_response': response,
                        'user_prompt': user_input,
                        'turn_num': turn_num,
                    }
                )
            else:
                send_error_message.error("Please record your voice first", icon="🚨")
                reload = True

    with response_container:
        try:
            message(st.session_state['bot_debate_history'][0], key='0_bot')
        except:
            st.warning('Server Error : Unexpected Server error occur. Please click "Rerun" button below.', icon="⚠️")
            time.sleep(1)
            reload = True
            st.session_state['total_debate_history'] = []
            rerun = st.button(label="Rerun", type="primary")
            if rerun:
                st.experimental_rerun()
            st.stop()
        if len(st.session_state['bot_debate_history']) == 1:
            text_to_speech = gTTS(text=st.session_state['bot_debate_history'][0], lang='en', slow=False)
            text_to_speech.save(f"audio/ses_{st.session_state['session_num']}_bot_res_0.mp3")
        
        audio_file = open(f"audio/ses_{st.session_state['session_num']}_bot_res_0.mp3", 'rb')
        audio_bytes = audio_file.read()
        st.audio(audio_bytes, format='audio/ogg')

        #TODO zip_longest() 고려하기!
        message_pairs = zip(
            st.session_state['bot_debate_history'][1:],
            st.session_state['user_debate_history'],
        )
        for i, (bot_hist, user_hist) in enumerate(message_pairs):
            message(user_hist, is_user=True, key=str(i)+'_user')
            message(bot_hist, key=str(i + 1)+'_bot')
            # if bot_hist:
            #TODO 생성된 message와 음성 파일 path를 하나의 객체로 관리하는 방법 고민
            if i == len(st.session_state['bot_debate_history']) - 2 and not reload:
                text_to_speech = gTTS(text=bot_hist, lang='en', slow=False)
                text_to_speech.save(f"audio/ses_{st.session_state['session_num']}_bot_res_{str(i + 1)}.mp3")
            audio_file = open(f"audio/ses_{st.session_state['session_num']}_bot_res_{str(i + 1)}.mp3", 'rb')
            audio_bytes = audio_file.read()
            st.audio(audio_bytes, format='audio/ogg')
        reload = False

    st.button(
        label="Next",
        type="primary",
        on_click=page_5_6_controller
    )

print("#"*80)
pprint.pprint(st.session_state.to_dict())
print("#"*80)

#########################################################
# Page6 - Total Debate Evaluation
#########################################################
@st.cache_data
def preprocess_words(user_history):
    res = " ".join(user_history)
    res = res.lower()
    res = res.translate(dict.fromkeys(map(ord, '!"#&\(),./:;<=>@[\\]^_`{|}~')))
    return res.split()

@st.cache_data
def get_stop_words():
    file = open("text/stop_words.txt", "r")
    try:
        content = file.read()
        stopwords = content.split(",")
    finally:
        file.close()
    return set(stopwords)

def page6():

    # end time
    st.session_state.end_time = time.time()
    st.session_state.debate_time = st.session_state.end_time - st.session_state.start_time

    _, _, pre, home  = st.columns([5, 5, 1, 1])
    with pre:
        st.button("🔙", on_click=page_4_5_controller, use_container_width=True)
    with home:
        st.button("🔝", on_click=page_n_1_controller, use_container_width=True)

    # st.tab
    st.header('Total Debate Evaluation')
    st.caption('📢 Note that evaluation using GPT is an experimental feature. Please check it out and give us your feedback.')

    tab1, tab2 = st.tabs(['Debate Evaluation', 'Debate Analysis']) ## Delete 'Perfect Case'

    with tab1:
        st.header("Debate Evaluation")

        # 전체, 유저, 봇 세 가지 옵션 중에 선택
        #judgement_who = st.selectbox("Choose what you want! (Evaluation result / Perfect case on this theme)", debate_themes)

        if st.session_state.judgement_result == "":
            with st.spinner('Wait for result...'):
                judgement_result = ""

                user_debate_history = "".join(
                    st.session_state.user_debate_history
                )
                bot_debate_history = "".join(
                    st.session_state.bot_debate_history
                )

                judgement_result = debate_judgement(
                    user_debate_history, 
                    bot_debate_history
                    )

                st.write("Debate Judgement Result")
                st.write(judgement_result)

                if judgement_result != "":
                    put_item(
                        table=dynamodb.Table('DEBO_evaluation'),
                        item={
                            'user_id': st.session_state.user_id,
                            'time_stamp': time_stamp,
                            'judgement_text': judgement_result,
                            'session_num': st.session_state.session_num,
                        }
                    )
            st.success('Done!')
        else:
            st.write(st.session_state.judgement_result)

    # with tab2:
    #     st.header("Perfect Case")

    #     perfect_case_list = [
    #         "This house supports the creation of an international court with a mandate to prosecute leaders for health crimes",
    #         "This house believes that governments would be justified in heavily pursuing long-termism",
    #         "THBT international discussion forums should not self-censor* in an attempt to increase inclusivity to people from countries with stringent freedom-of-speech rules.",
    #         ]

    #     perfect_case_selected = st.selectbox("Choose the Perfect Case", perfect_case_list)

    #     perfect_case = perfect_case_selector(
    #         perfect_case_selected
    #         )
        
    #     perfect_case_url = perfect_case['perfect_case_url']
    #     perfect_case_text = perfect_case['perfect_case_text']

    #     st.video(perfect_case_url)
    #     st.write(perfect_case_text)

    with tab2:
        st.header('Debate Analysis')

        # 유저의 history를 기반으로 발화량, 빈출 단어, 발화 습관 세 가지를 분석
        user_history = st.session_state.user_debate_history

        # 1. 발화량: 총 단어, 평균 속도(단어/시간)를 평균 발화량 혹은 참고 지표와 비교해 제시

        # 총 단어
        # 텍스트를 단어로 분할합니다.
        # 각 단어의 빈도를 계산합니다.

        # 리스트를 문자열로 변환하고, 전처리를 합니다. 공백을 기준으로 단어를 분할합니다.
        total_word_list = preprocess_words(user_history)
        total_word_count = len(total_word_list)
        #total_word_count = len(user_history.split())
        st.write("Total Word Count: ", total_word_count)

        # 평균 속도(단어/시간)
        #user_debate_time = st.session_state.user_debate_time
        average_word_per_time = total_word_count / st.session_state.debate_time # 시간 단위보고 나중에 수정하기
        st.write("Average Word Per Time: ", average_word_per_time)

        # 2. 빈출 단어: 반복해서 사용하는 단어 리스트
        # 불용어 제거
        total_word_list = [word for word in total_word_list if word not in get_stop_words()]
        # 빈도 계산
        frequency = Counter(total_word_list)
        # 가장 빈도가 높은 데이터 출력
        most_common_data = frequency.most_common(5)

        st.write("Most Common Words: ")
        for word, count in most_common_data:
            st.write(" - ", word, ":", count)

        # print(most_common_data)
        # st.write("Most Common Words: ", most_common_data)

        # 3. 발화 습관: 불필요한 언어습관(아, 음)
        # whisper preprocesser에서 주면
        disfluency_word_list = ['eh', 'umm', 'ah', 'uh', 'er', 'erm', 'err']
        # Count the disfluency words
        disfluency_counts = sum(user_word in disfluency_word_list for user_word in user_history)
        st.write("Disfluency Counts: ", disfluency_counts)

        if total_word_count != "" and average_word_per_time != "" and disfluency_counts != "":

                put_item(
                    table=dynamodb.Table('DEBO_debate_analysis'),
                    item={
                        'user_id': st.session_state.user_id,
                        'time_stamp': time_stamp,
                        'total_word_count': total_word_count,
                        'average_word_per_time': Decimal(str(average_word_per_time)),
                        'disfluency_counts': disfluency_counts,
                        'session_num': int(st.session_state.session_num),
                    }
                )

        # 유저와 봇의 대화 데이터가 세션에 남아있음
        # st.session_state.debate_history
    
    ############################################
    # Visualization
    ############################################

    # 이전에 기록된 값이 있다면, 그래프를 그립니다.
    # 이전에 기록된 값이 없다면, 그래프를 그리지 않습니다.


#########################################################
# Page7
#########################################################

# def page7():

#     # end time
#     st.session_state.end_time = time.time()
#     st.session_state.debate_time = st.session_state.end_time - st.session_state.start_time

#     _, _, pre, home  = st.columns([5, 5, 1, 1])
#     with pre:   
#         st.button("🔙", on_click=page_1_2_controller, use_container_width=True)
#     with home:
#         st.button("🔝", on_click=page_n_1_controller, use_container_width=True)

#     st.header('Total Debate Evaluation')

#     tab1, tab2 = st.tabs(['Debate Judgement', 'Debate Analysis'])

#     with tab1:
#         st.header("Debate Evaluation")
        
#         debate_themes = ['User-Bot', "User", "Bot"]

#         # 전체, 유저, 봇 세 가지 옵션 중에 선택
#         judgement_who = st.selectbox("Choose your debate theme", debate_themes)

#         if st.session_state.judgement_result == "":
#             with st.spinner('Wait for judgement result...'):
#                 judgement_result = ""

#                 user_debate_history = "".join(
#                     st.session_state.user_debate_history
#                 )
#                 bot_debate_history = "".join(
#                     st.session_state.bot_debate_history
#                 )

#                 judgement_result = debate_judgement(
#                     judgement_who, 
#                     user_debate_history, 
#                     bot_debate_history
#                     )
                
#                 st.session_state.judgement_result = judgement_result
                
#                 st.write("Debate Judgement Result")
#                 st.write(judgement_result)

#                 if judgement_result:
#                         put_item(
#                             table=dynamodb.Table('DEBO_evaluation'),
#                             item={
#                                 'user_id': st.session_state.user_id,
#                                 'time_stamp': time_stamp,
#                                 'judgement_text': judgement_result,
#                                 'session_num': int(st.session_state.session_num),
#                             }
#                         )
#                 st.success('Done!')
#         else:
#             st.write(st.session_state.judgement_result)

#     with tab2:
#         st.header('Debate Analysis')

#         # 유저의 history를 기반으로 발화량, 빈출 단어, 발화 습관 세 가지를 분석
#         user_history = st.session_state.user_debate_history

#         # 1. 발화량: 총 단어, 평균 속도(단어/시간)를 평균 발화량 혹은 참고 지표와 비교해 제시

#         # 총 단어
#         # 텍스트를 단어로 분할합니다.
#         # 각 단어의 빈도를 계산합니다.
#         total_word_count = len(user_history)
#         #total_word_count = len(user_history.split())
#         st.write("Total Word Count: ", total_word_count)

#         # 평균 속도(단어/시간)
#         #user_debate_time = st.session_state.user_debate_time
#         average_word_per_time = total_word_count / st.session_state.debate_time # 시간 단위보고 나중에 수정하기
#         st.write("Average Word Per Time: ", average_word_per_time)

#         # 2. 빈출 단어: 반복해서 사용하는 단어 리스트
#         # 빈도 계산
#         frequency = Counter(user_history)
#         # 가장 빈도가 높은 데이터 출력
#         most_common_data = frequency.most_common(10)
#
#         print(most_common_data)
#         st.write("Most Common Words: ", most_common_data)

#         # 3. 발화 습관: 불필요한 언어습관(아, 음)
#         # whisper preprocesser에서 주면
#         disfluency_word_list = ['eh', 'umm', 'ah', 'uh', 'er', 'erm', 'err']
#         # Count the disfluency words
#         disfluency_counts = sum(user_word in disfluency_word_list for user_word in user_history)
#         st.write("Disfluency Counts: ", disfluency_counts)

#         if total_word_count != "" and average_word_per_time != "" and disfluency_counts != "":
#                 put_item(
#                     table=dynamodb.Table('DEBO_evaluation'),
#                     item={
#                         'user_id': st.session_state.user_id,
#                         'time_stamp': time_stamp,
#                         'total_word_count': total_word_count,
#                         'average_word_per_time': Decimal(str(average_word_per_time)),
#                         'disfluency_counts': disfluency_counts,
#                         'session_num': int(st.session_state.session_num),
#                     }
#                 )

        # 유저와 봇의 대화 데이터가 세션에 남아있음
        # st.session_state.debate_history

    ############################################
    # Visualization
    ############################################

    # 이전에 기록된 값이 있다면, 그래프를 그립니다.
    # 이전에 기록된 값이 없다면, 그래프를 그리지 않습니다.


#########################################################
# Page Routing
#########################################################
pages = {
    "Page 1": page1, # user_id를 입력받는 페이지
    "Page 2": page2, # 원하는 기능을 선택하는 페이지
    # "Page 3": page3, # 과거 토론 내역을 선택하는 페이지
    "Page 4": page4, # 토론 세부사항 설정
    "Page 5": page5, # Total Debate
    "Page 6": page6, # Evaluation Only
    # "Page 7": page7, # Analyzing Utterances
}

selection = st.session_state.page
print("selection:", selection)

page = pages[selection]
# Execute selected page function
page()
