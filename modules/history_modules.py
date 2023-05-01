
from modules.db_modules import get_db, put_item, get_item, get_lastest_item

def get_history(
        table, 
        name_of_partition_key, 
        value_of_partition_key,
        session_num
        ):
    
    history_list = get_lastest_item(
        table=table,
        name_of_partition_key=name_of_partition_key,
        value_of_partition_key=value_of_partition_key,
    )

    if history_list==[]:
        history = ""
    else:
        history = ""
        history_dummy_list = []
        for dic in history_list:
            if dic['session_num'] == session_num:
                history_dummy_list.append("User: " + dic['user_prompt'])
                history_dummy_list.append("Bot: " + dic['bot_response'])
        
        history = "\n".join(history_dummy_list)

    return history