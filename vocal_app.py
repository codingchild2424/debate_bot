import streamlit as st
import openai

from gtts import gTTS
from collections import Counter
from streamlit_chat import message

from dotenv import dotenv_values
from bots.judgement_bot import debate_judgement
from collections import Counter
from audiorecorder import audiorecorder
from st_custom_components import st_audiorec

# modules
from modules.gpt_modules import gpt_call
#from modules.whisper_modules import transcribe

config = dotenv_values(".env")

openai.organization = config.get('OPENAI_ORGANIZATION')
openai.api_key = config.get('OPENAI_API_KEY')


# Page Configuration
st.set_page_config(page_title="Streamlit App")

# Initialize session state variables
if "page" not in st.session_state:
    st.session_state.page = "Page 1"

if "topic" not in st.session_state:
    st.session_state.topic = "None"

if "user_id" not in st.session_state:
    st.session_state.user_id = ""

if "openAI_token" not in st.session_state:
    st.session_state.openAI_token = ""

if "case1" not in st.session_state:
    st.session_state.case1 = ""

if "case2" not in st.session_state:
    st.session_state.case2 = ""

if "case3" not in st.session_state:
    st.session_state.case3 = ""

if "page2_tab" not in st.session_state:
    st.session_state.page2_tab = "tab1"

if "total_debate_history" not in st.session_state:
    st.session_state.total_debate_history = []

if "user_debate_history" not in st.session_state:
    st.session_state.user_debate_history = []

if "bot_debate_history" not in st.session_state:
    st.session_state.bot_debate_history = []

if "user_debate_time" not in st.session_state:
    st.session_state.user_debate_time = ""

if "pros_and_cons" not in st.session_state:
    st.session_state.pros_and_cons = ""

if 'generated' not in st.session_state:
    st.session_state['generated'] = []

if 'past' not in st.session_state:
    st.session_state['past'] = []

if 'messages' not in st.session_state:
    st.session_state['messages'] = [
        {"role": "system", "content": "You are a helpful assistant."}
    ]


# Save function (placeholder)
def save_info(user_id, openAI_token, debate_theme):
    # You can add the code to save the submitted info (e.g., to a database)
    st.session_state.user_id = user_id
    st.session_state.openAI_token = openAI_token
    st.session_state.debate_theme = debate_theme

    print("User ID:", user_id)
    print("OpenAI token:", openAI_token)
    print("Debate theme:", debate_theme)

# Session state
#session_state = SessionState.get(user_id="", openAI_token="", debate_theme="")

def write_info():
    st.write('You choose', st.session_state.topic_list)

# for callback when button is clicked
def page_1_2_controller():
    if st.session_state.user_id.strip() == "" or st.session_state.openAI_token.strip() == "":
        st.session_state.page = "Page 1"
        st.warning('Please fill in all the required fields.')
    else:
        st.session_state.page = "Page 2"

def page_2_3_controller():
    st.session_state.page = "Page 3"

def page2_tab_controller():
    st.session_state.page2_tab = "tab2"

def page4_controller():
    st.session_state.page = "Page 4"

def page_5_6_controller():
    st.session_state.page = "Page 6"

#########################################################
# Page 1
#########################################################
def page1():

    # for local variables
    topic_list = []

    st.header('User Info & Debate Setting')
    st.session_state.user_id = st.text_input(
        label="Enter user ID",
        max_chars=100,
        placeholder="Enter user ID"
        )
    st.session_state.openAI_token = st.text_input(
        label="Enter OpenAI token",
        max_chars=200,
        placeholder="Enter OpenAI token"
        )

    if st.button(
        label='Submit all information',
        on_click=page_1_2_controller
        ):
        # You can add a function here to save the submitted info
        if st.session_state.user_id != '' and st.session_state.openAI_token != '':
            save_info(
                st.session_state.user_id, 
                st.session_state.openAI_token, 
                st.session_state.debate_theme
                )
            st.write('Information submitted successfully.')

#########################################################
# Page 2
#########################################################
def page2():
    st.header("Choose Option")
    option_result = st.selectbox("Choose your option", ["Total Debate", "Evaluation Only", "Analyzing Utterances"])

    # add controller
    if option_result == "Total Debate":
        page_control_func = page_2_3_controller
    #TODO page_2_7_controller, page_2_8_controller 만들기!
    # elif option_result == "Evaluation Only":
    #     page_control_func = page_2_7_controller
    # elif option_result == "Analyzing Utterances":
    #     page_control_func = page_2_8_controller

    if st.button(
        label='Submit all information',
        on_click=page_control_func
        ):
        st.write('Information submitted successfully.')
        

def page3():
    #########################################################
    # Tab 1 - Total Debate (토론 준비 -> 연습 -> 평가)
    #########################################################
    st.header("Total Debate")
    debate_themes = ['Education','Sports','Religion','Justice','Pandemic','Politics','Minority','etc']

    st.write("1. Select a debate theme")
    st.session_state.debate_theme = st.selectbox("Choose your debate theme", debate_themes)

    if st.session_state.debate_theme == 'Education':
        topic_list = [
            "THBT college entrance examinations should accept students only on the basis of their academic performance in secondary education.", 
            "THS a world where the government gives cash that individuals can use to freely select their academic preference (including but not limited to school of choice, private academies, and tutoring) instead of funding for public education.",
            "THW abolish all requirements and evaluation criteria in higher education (i.e., attendance, exams, assignments)."
            ]
        #topic = st.selectbox("Select a topic_list", topic_list)
    elif st.session_state.debate_theme == 'Sports':
        topic_list = [
            "THBT having star players for team sports do more harm than good to the team.",
            "THR the emphasis on winning a medal in the Olympics as a core symbol of success.",
            "THP a world where sports serves purely entertainment purposes even at the expense of fair play."
            ]
        #topic = st.selectbox("Select a topic_list", topic_list)
    elif st.session_state.debate_theme == 'Religion':
        topic_list = [
            "THW, as a religious group/leader, cease attempts at increasing the number of believers and instead prioritize boosting loyalty amongst adherents to the religion.",
            "Assuming feasibility, TH prefers a world where a panel of church leaders would create a universally accepted interpretation of the Bible that the believers would abide by.",
            "THW aggressively crackdown on megachurches."
            ]
        #topic = st.selectbox("Select a topic_list", topic_list)
    elif st.session_state.debate_theme == 'Justice':
        topic_list = [
            "In 2050, AI robots are able to replicate the appearance, conversation, and reaction to emotions of human beings. However, their intelligence still does not allow them to sense emotions and feelings such as pain, happiness, joy, and etc.",
            "In the case a human destroys the robot beyond repair, THW charge murder instead of property damage.",
            "THP a world where the criminal justice system’s role is mainly for victim’s vengeance. THW allow prosecutors and victims to veto assigned judges."
            ]
        #topic = st.selectbox("Select a topic_list", topic_list)
    elif st.session_state.debate_theme == 'Pandemic':
        topic_list = [
            "During a pandemic, THBT businesses that benefit from the pandemic should be additionally taxed.",
            "THW nullify the effect of medical patents in cases of medical emergencies.",
            "THW ban media content that denies the efficacy of the COVID-19 without substantial evidence."
            ]
        #topic = st.selectbox("Select a topic_list", topic_list)
    elif st.session_state.debate_theme == 'Politics':
        topic_list = [
            "Info: The Candle Light Will (촛불민심) is a term derived from the symbolic candle-light protests for the impeachment of the late president Park Geun Hye, commonly used to mean the people’s will to fight against corrupt governments. The Moon administration has frequently referred to the Candle Light Will as the driving force behind its election that grants legitimacy to its policies. THR the ‘candle light will’ narrative in the political discourse of South Korea.",
            "THW impose a cap on the property and income of politicians.",
            "THW give the youth extra votes."
            ]
        #topic = st.selectbox("Select a topic_list", topic_list)
    elif st.session_state.debate_theme == 'Minority':
        topic_list = [
            "Context: A prominent member of the LGBT movement has discovered that a very influential politician helping the LGBT movement has been lying about their sexual orientation as being gay when they are straight. THW disclose this information.",
            "THBT the LGBTQIA+ movement should denounce the existence of marriage as opposed to fighting for equal marriage rights.",
            "THBT the LGBTQIA+ movement should condemn the consumption of movies and TV shows that cast straight actors/actresses in non-heterosexual identified roles."
            ]
        #topic = st.selectbox("Select a topic_list", topic_list)
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

    st.write("2. Select a topic")
    st.session_state.topic = st.selectbox("Choose your topic", topic_list)

    st.write("3. Write 3 cases here (Each case should be consisted of opinion, reasoning, and example).")
    st.session_state.case1 = st.text_area(
        label="Case 1",
        placeholder="Each case should be consisted of opinion, reasoning, and example.",
        height=100
        )
    st.session_state.case2 = st.text_area(
        label="Case 2",
        placeholder="Each case should be consisted of opinion, reasoning, and example.",
        height=100
        )
    st.session_state.case3 = st.text_area(
        label="Case 3",
        placeholder="Each case should be consisted of opinion, reasoning, and example.",
        height=100
        )
    
    st.session_state.pros_and_cons = st.selectbox("Choose your Side (Pros and Cons)", ["Pros", "Cons"])
    
    st.button(
        "Start Debate",
        on_click=page4_controller
        )
    

    with st.sidebar:
        st.sidebar.title('Ask to GPT')
        st.sidebar.text_area(
            label="Input text here", 
            placeholder="Input text here",
            height=100)
        st.sidebar.button("Ask")

#########################################################
# Page4
#########################################################

# generate response
def generate_response(prompt):
    st.session_state['messages'].append({"role": "user", "content": prompt})
    response = gpt_call(prompt)
    st.session_state['messages'].append({"role": "assistant", "content": response})
    return response

def page4():

    with st.sidebar:
        st.sidebar.title('Ask to GPT')
        user_input = st.sidebar.text_area(
            label="Input text here", 
            placeholder="Input text here",
            height=100)
        output = st.sidebar.button("Ask")
        if output:
            result = gpt_call(user_input)
        else:
            result = ""

        st.sidebar.text_area(
            label="Answer in here", 
            placeholder="(Answer)",
            value=result,
            height=150)

    debate_preset = "\n".join([
        "Debate Rules: ",
        "1) This debate will be divided into two teams, pro and con, with two debates on each team.",
        "2) The order of speaking is: first debater for the pro side, first debater for the con side, second debater for the pro side, second debater for the con side.",
        "3) Answer logically with an introduction, body, and conclusion.", #add this one.
        "4) Your role : " + st.session_state["pros_and_cons"] + "side debator"
        "5) Debate subject: " + st.session_state['topic']
    ])
    first_prompt = "Now we're going to start. Summarize the subject and your role. And ask user ready to begin."
    st.session_state['messages'] = [
        {"role": "system", "content": debate_preset}
    ]

    response = gpt_call(debate_preset + "\n" + first_prompt, role="system")
    st.session_state['messages'].append({"role": "assistant", "content": response})
    st.session_state['generated'].append(response)


    # container for chat history
    response_container = st.container()
    # container for text box
    container = st.container()

    with container:
        #TODO (웅기형) : STT 붙이는 부분
        # audio_data = st_audiorec()
        audio_data = audiorecorder("Click to record", "Recording...")

        if audio_data is not None:            
            wav_file = open("audio.wav", "wb")
            wav_file.write(audio_data.tobytes())
            wav_file.close()

            with open("audio.wav", "rb") as audio_file:
                whisper_result = openai.Audio.transcribe(
                    model = "whisper-1",
                    file = audio_file,
                    response_format = "text",
                    language = "en"
                )
                print(whisper_result)
        
        with st.form(key='my_form', clear_on_submit=True):
            if whisper_result:
                user_input = whisper_result
            else:
                user_input = st.text_area("You:", key='input', height=100)
            submit_buttom = st.form_submit_button(label='Send')

        if submit_buttom and user_input:
            output = generate_response(user_input)
            st.session_state['user_debate_history'].append(user_input)
            st.session_state['bot_debate_history'].append(output)
            st.session_state['total_debate_history'].append(
                {
                    "user" + str(len(st.session_state['user_debate_history'])): user_input,
                    "bot" + str(len(st.session_state['bot_debate_history'])): output,
                }
            )
            st.session_state['past'].append(user_input)
            st.session_state['generated'].append(output)

    if st.session_state['generated']:
        with response_container:
            message(st.session_state["generated"][0], key=str(0))
            for i in range(len(st.session_state['past'])):
                message(st.session_state["past"][i], is_user=True, key=str(i) + '_user')
                
                text_to_speech = gTTS(text=st.session_state["generated"][i + 1], lang='en', slow=False)
                text_to_speech.save(f'audio/test_gtts_{str(i)}.mp3')
                audio_file = open(f'audio/test_gtts_{str(i)}.mp3', 'rb')
                audio_bytes = audio_file.read()
                st.audio(audio_bytes, format='audio/ogg')

                message(st.session_state["generated"][i + 1], key=str(i + 1))

    #TODO 전체 유저가 발화한 시간 기록하기 -> 세션에 저장

print("#"*50)
print(st.session_state)
print("#"*50)

#########################################################
# Page5 - Total Debate Evaluation
#########################################################
def page5():

    # st.tab
    st.header('Total Debate Evaluation')

    tab1, tab2 = st.tabs(['Debate Judgement', 'Debate Analysis'])

    with tab1:
        st.header("Debate Evaluation")
        
        debate_themes = ['User-Bot', "User", "Bot"]

        # 전체, 유저, 봇 세 가지 옵션 중에 선택
        judgement_who = st.selectbox("Choose your debate theme", debate_themes)

        if judgement_who == 'User-Bot':
            debate_history = st.session_state.total_debate_history
        elif judgement_who == 'User':
            debate_history = st.session_state.user_debate_history
        elif judgement_who == 'Bot':
            debate_history = st.session_state.bot_debate_history

        judgement_result = debate_judgement(debate_history)

        st.write("Debate Judgement Result")
        st.write(judgement_result)

    with tab2:
        st.header('Debate Analysis')

        # 유저의 history를 기반으로 발화량, 빈출 단어, 발화 습관 세 가지를 분석
        user_history = st.session_state.user_debate_history

        # 1. 발화량: 총 단어, 평균 속도(단어/시간)를 평균 발화량 혹은 참고 지표와 비교해 제시

        # 총 단어
        # 텍스트를 단어로 분할합니다.
        words = user_history.split()
        # 각 단어의 빈도를 계산합니다.
        total_word_count = Counter(words)
        #total_word_count = len(user_history.split())
        st.write("Total Word Count: ", total_word_count)

        # 평균 속도(단어/시간)
        user_debate_time = st.session_state.user_debate_time
        average_word_per_time = total_word_count / user_debate_time # 시간 단위보고 나중에 수정하기
        st.write("Average Word Per Time: ", average_word_per_time)

        # 2. 빈출 단어: 반복해서 사용하는 단어 리스트
        # 빈도가 높은 순서대로 단어를 정렬합니다.
        most_common_words = total_word_count.most_common()
        # 가장 빈도가 높은 10개의 단어를 출력합니다.
        st.write("Most Common Words: ", most_common_words[:10])

        # 3. 발화 습관: 불필요한 언어습관(아, 음)
        # whisper preprocesser에서 주면
        disfluency_word_list = ['eh', 'umm', 'ah', 'uh', 'er', 'erm', 'err']
        # Count the disfluency words
        disfluency_counts = {word: total_word_count[word] for word in disfluency_word_list}
        st.write("Disfluency Counts: ", disfluency_counts)

        # 유저와 봇의 대화 데이터가 세션에 남아있음
        # st.session_state.debate_history

    

#########################################################
# Page6
#########################################################

def page6():

    # 여기서 User의 과거 기록을 검색할 수 있게 해야 함
    
    # st.tab
    st.header('Total Debate Evaluation')

    tab1, tab2 = st.tabs(['Debate Judgement', 'Debate Analysis'])

    with tab1:
        st.header("Debate Evaluation")
        
        debate_themes = ['User-Bot', "User", "Bot"]

        # 전체, 유저, 봇 세 가지 옵션 중에 선택
        judgement_who = st.selectbox("Choose your debate theme", debate_themes)

        if judgement_who == 'User-Bot':
            debate_history = st.session_state.total_debate_history
        elif judgement_who == 'User':
            debate_history = st.session_state.user_debate_history
        elif judgement_who == 'Bot':
            debate_history = st.session_state.bot_debate_history

        judgement_result = debate_judgement(debate_history)

        st.write("Debate Judgement Result")
        st.write(judgement_result)

    with tab2:
        st.header('Debate Analysis')

        # 유저의 history를 기반으로 발화량, 빈출 단어, 발화 습관 세 가지를 분석
        user_history = st.session_state.user_debate_history

        # 1. 발화량: 총 단어, 평균 속도(단어/시간)를 평균 발화량 혹은 참고 지표와 비교해 제시

        # 총 단어
        # 텍스트를 단어로 분할합니다.
        words = user_history.split()
        # 각 단어의 빈도를 계산합니다.
        total_word_count = Counter(words)
        #total_word_count = len(user_history.split())
        st.write("Total Word Count: ", total_word_count)

        # 평균 속도(단어/시간)
        user_debate_time = st.session_state.user_debate_time
        average_word_per_time = total_word_count / user_debate_time # 시간 단위보고 나중에 수정하기
        st.write("Average Word Per Time: ", average_word_per_time)

        # 2. 빈출 단어: 반복해서 사용하는 단어 리스트
        # 빈도가 높은 순서대로 단어를 정렬합니다.
        most_common_words = total_word_count.most_common()
        # 가장 빈도가 높은 10개의 단어를 출력합니다.
        st.write("Most Common Words: ", most_common_words[:10])

        # 3. 발화 습관: 불필요한 언어습관(아, 음)
        # whisper preprocesser에서 주면
        disfluency_word_list = ['eh', 'umm', 'ah', 'uh', 'er', 'erm', 'err']
        # Count the disfluency words
        disfluency_counts = {word: total_word_count[word] for word in disfluency_word_list}
        st.write("Disfluency Counts: ", disfluency_counts)

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
    "Page 1": page1, # user_id와 openai_key를 입력받는 페이지
    "Page 2": page2, # 원하는 기능을 선택하는 페이지
    "Page 3": page3, # Total Debate
    "Page 4": page4, # Evaluation Only
    "Page 5": page5, # Analyzing Utterances
    "Page 6": page6,
}

selection = st.session_state.page
print("selection:", selection)

page = pages[selection]
# Execute selected page function
page()


