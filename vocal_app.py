import whisper
import gradio as gr
from dotenv import dotenv_values
import openai
import os

"""
apt-get update
apt-get install ffmpeg
"""

config = dotenv_values(".env")

openai.organization = config.get('OPENAI_ORGANIZATION')
openai.api_key = config.get('OPENAI_API_KEY')


def transcribe(audio):
    os.rename(audio, audio + '.wav')
    file = open(audio + '.wav', "rb")

    result = openai.Audio.transcribe("whisper-1", file).text

    return result

with gr.Blocks() as app:
    # 주제선택
    with gr.Tab("Selecting Subject"):
        debate_theme = gr.Dropdown(
            ['Education','Sports','Religion','Justice','Pandemic','Politics','Minority','etc'],
            label="Debate Theme",
            info="Select a theme for the debate."
        )
        submit_button = gr.Button("Submit")
        

        if debate_theme.value == "Education":
            topic_list = [
                "THBT college entrance examinations should accept students only on the basis of their academic performance in secondary education.", 
                "THS a world where the government gives cash that individuals can use to freely select their academic preference (including but not limited to school of choice, private academies, and tutoring) instead of funding for public education.",
                "THW abolish all requirements and evaluation criteria in higher education (i.e., attendance, exams, assignments)."
            ]
        elif debate_theme.value == "Sports":
            topic_list = [
                "THBT having star players for team sports do more harm than good to the team.",
                "THR the emphasis on winning a medal in the Olympics as a core symbol of success.",
                "THP a world where sports serves purely entertainment purposes even at the expense of fair play."
            ]
        elif debate_theme.value == "Religion":
            topic_list = [
                "THW, as a religious group/leader, cease attempts at increasing the number of believers and instead prioritize boosting loyalty amongst adherents to the religion.",
                "Assuming feasibility, TH prefers a world where a panel of church leaders would create a universally accepted interpretation of the Bible that the believers would abide by.",
                "THW aggressively crackdown on megachurches."
            ]
        elif debate_theme.value == "Justice":
            topic_list = [
                "In 2050, AI robots are able to replicate the appearance, conversation, and reaction to emotions of human beings. However, their intelligence still does not allow them to sense emotions and feelings such as pain, happiness, joy, and etc.",
                "In the case a human destroys the robot beyond repair, THW charge murder instead of property damage.",
                "THP a world where the criminal justice system’s role is mainly for victim’s vengeance. THW allow prosecutors and victims to veto assigned judges."
            ]
        elif debate_theme.value == "Pandemic":
            topic_list = [
                "During a pandemic, THBT businesses that benefit from the pandemic should be additionally taxed.",
                "THW nullify the effect of medical patents in cases of medical emergencies.",
                "THW ban media content that denies the efficacy of the COVID-19 without substantial evidence."
            ]
        elif debate_theme.value == "Politics":
            topic_list = [
                "Info: The Candle Light Will (촛불민심) is a term derived from the symbolic candle-light protests for the impeachment of the late president Park Geun Hye, commonly used to mean the people’s will to fight against corrupt governments. The Moon administration has frequently referred to the Candle Light Will as the driving force behind its election that grants legitimacy to its policies. THR the ‘candle light will’ narrative in the political discourse of South Korea.",
                "THW impose a cap on the property and income of politicians.",
                "THW give the youth extra votes."
            ]
        elif debate_theme.value == "Minority":
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

        debate_topic = gr.Dropdown(
            topic_list,
            label="Debate Topic",
            info="Select a topic for the debate."
        )
        text_input = gr.Textbox()
        text_output = gr.Textbox()
        text_button = gr.Button("Flip")

    # 토론준비
    with gr.Tab("Ready to Debate"):
        text_input = gr.Textbox()
        text_output = gr.Textbox()
        text_button = gr.Button("Flip")

    # 토론연습
    with gr.Tab("Practice Debate"):
        text_input = gr.Textbox()
        text_output = gr.Textbox()
        text_button = gr.Button("Flip")

    # 토론평가
    with gr.Tab("Evaluate Debate"):
        text_input = gr.Textbox()
        text_output = gr.Textbox()
        text_button = gr.Button("Flip")

    # 발화분석
    with gr.Tab("Analysis Voice"):
        text_input = gr.Textbox()
        text_output = gr.Textbox()
        text_button = gr.Button("Flip")    


app.launch()
        #submit = gr.inputs.Button(label="Submit")
# gr.Interface(
#     title = 'Whisper Audio to Text with Speaker Recognition', 
#     fn=transcribe,
#     inputs=[
#         gr.inputs.Audio(source="microphone", type="filepath"),
#         #gr.inputs.Number(default=2, label="Number of Speakers")
#     ],
#     outputs="text"
# ).launch()