import pandas as pd

import jwt

def decode_google_token(token_string):
    decoded_result = jwt.decode(token_string, verify=False, algorithms='RS256')
    return decoded_result

def get_conference_schedule(current_date):
    try:
        conference_file_columns = [
            'date',
            'time',
            'talk_1',
            'talk_2'
        ]
        conference_schedule = pd.read_csv('./conference_schedule.csv',names=conference_file_columns,index_col=None)
        todays_schedule = conference_schedule.loc[conference_schedule['date'] == str(current_date)]
        if todays_schedule.empty:
            return False, None
        else:
            return True, todays_schedule[['time','talk_1','talk_2']].values.tolist()
    except Exception as e:
        print(e)