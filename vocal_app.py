import streamlit as st
#import SessionState

# Page Configuration
st.set_page_config(page_title="Streamlit App")

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
    st.selectbox("Choose your option", ["Total Debate", "Evaluation Only", "Analyzing Utterances"])

    if st.button(
        label='Submit all information',
        on_click=page_2_3_controller
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
    
    st.button(
        "Start Debate",
        on_click=page2_tab_controller
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
def page4():

    with st.sidebar:
        st.sidebar.title('Ask to GPT')
        st.sidebar.text_area(
            label="Input text here", 
            placeholder="Input text here",
            height=100)
        st.sidebar.button("Ask")


#########################################################
# Page5
#########################################################
def page5():

    with st.sidebar:
        st.sidebar.title('Ask to GPT')
        st.sidebar.text_area(
            label="Input text here", 
            placeholder="Input text here",
            height=100)
        st.sidebar.button("Ask")


#########################################################
# Page Routing
#########################################################
pages = {
    "Page 1": page1, # user_id와 openai_key를 입력받는 페이지
    "Page 2": page2, # 원하는 기능을 선택하는 페이지
    "Page 3": page3, # Total Debate
    "Page 4": page4, # Evaluation Only
    "Page 5": page5, # Analyzing Utterances
}

selection = st.session_state.page
print("selection:", selection)

page = pages[selection]
# Execute selected page function
page()


