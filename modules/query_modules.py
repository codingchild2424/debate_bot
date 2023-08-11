from time import time
from datetime import datetime

# modules
from modules.db_modules import put_item, get_lastest_item
from modules.history_modules import get_history

# bots
from bots.debate_bot import debate_bot


def query(
        db_table, 
        user_id, 
        prompt, 
        debate_subject, 
        bot_role,
        session_num
        ):
    
    print("query session", session_num)

    history, history_num = get_history(
        db_table, 
        name_of_partition_key="user_id", 
        value_of_partition_key=user_id,
        session_num=session_num
        )
    print("history", history)

    bot_result = debate_bot(
        prompt, 
        history, 
        debate_subject, 
        bot_role,
        history_num
        )
    
    time_stamp = str(datetime.fromtimestamp(time()))

    item = {
        'user_id': user_id,
        'time_stamp': time_stamp,
        'user_prompt': prompt,
        'bot_response': bot_result,
        'debate_subject': debate_subject,
        'session_num': session_num,
        'bot_role': bot_role
        }

    put_item(db_table, item)
    
    return bot_result