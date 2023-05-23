


def perfect_case_selector(perfect_case_selected):

    if perfect_case_selected == "This house supports the creation of an international court with a mandate to prosecute leaders for health crimes":
        perfect_case_url = "https://www.youtube.com/live/s8g4BLdhQQw?feature=share&t=782"
        perfect_case_text_path = "./texts/model_speech1.txt"

    elif perfect_case_selected == "This house believes that governments would be justified in heavily pursuing long-termism":
        perfect_case_url = "https://www.youtube.com/live/D-JXK_yw1bI?feature=share&t=1154"
        perfect_case_text_path = "./texts/model_speech2.txt"

    elif perfect_case_selected == "THBT international discussion forums should not self-censor* in an attempt to increase inclusivity to people from countries with stringent freedom-of-speech rules.":

        perfect_case_url = "https://www.youtube.com/live/N2fXz3nfdfs?feature=share&t=1373"
        perfect_case_text_path = "./texts/model_speech3.txt"

        
    with open(perfect_case_text_path, "r") as f:
            perfect_case_text = f.read()

    perfect_case_result = {
            "perfect_case_url": perfect_case_url,
            "perfect_case_text": perfect_case_text
        }

    return perfect_case_result