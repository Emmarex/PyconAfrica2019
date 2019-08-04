from datetime import date, datetime

from flask import Flask, request, abort, jsonify
from pydialogflow_fulfillment import *
import helper

flask_app = Flask(__name__)

CONFERENCE_START_DATE = datetime.strptime('2019-08-06','%Y-%m-%d').date()
CONFERENCE_END_DATE = datetime.strptime('2019-08-10','%Y-%m-%d').date()

CONFERENCE_DATE = datetime.strptime('2019-08-06','%Y-%m-%d').date()

CONFERENCE_SCHEDULE_INTENT = 'conference_Schedule'

@flask_app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        dialogflow_request = DialogflowRequest(request.data)
        dialogflow_intent = dialogflow_request.get_intent_displayName()
        if dialogflow_intent == "welcome_intent":
            dialogflow_response = DialogflowResponse("Welcome to my test dialogflow webhook")
            dialogflow_response.add(SimpleResponse("Welcome to my test dialogflow webhook","Welcome to my test dialogflow webhook"))
            response = flask_app.response_class(response=dialogflow_response.get_final_response(),mimetype='application/json')
        elif dialogflow_intent == CONFERENCE_SCHEDULE_INTENT:
            # todays_date = date.today()
            todays_date = CONFERENCE_DATE
            if todays_date >= CONFERENCE_START_DATE and todays_date <= CONFERENCE_END_DATE:
                is_successful, todays_schedule = helper.get_conference_schedule(todays_date)
                if is_successful:
                    simple_text = f"Here is the schedule for today {todays_date.strftime('%a %B %d')}"
                    dialogflow_response = DialogflowResponse(simple_text)
                    dialogflow_response.add(SimpleResponse(simple_text,simple_text))
                    table_rows = []
                    [table_rows.append(TableCell(cell_text=schedule)) for schedule in todays_schedule]
                    dialogflow_response.add(Table(rows=table_rows,columns=['Time','Talk 1','Talk 2'],add_dividers=True))
                else:
                    dialogflow_response = DialogflowResponse("Something happened, I cant find today's schedule")
                    dialogflow_response.add(SimpleResponse("Something happened, I cant find today's schedule","Something happened, I cant find today's schedule"))
            else:
                if todays_date >= CONFERENCE_END_DATE:
                    dialogflow_response = DialogflowResponse("Pycon Africa 2019 as ended.")
                    dialogflow_response.add(SimpleResponse("Pycon Africa 2019 as ended.","Pycon Africa 2019 as ended."))
                    dialogflow_response.add(LinkOutSuggestion("See Schedule Online","https://africa.pycon.org/schedule/"))
                else:
                    dialogflow_response = DialogflowResponse("Pycon Africa 2019 as not started.")
                    dialogflow_response.add(SimpleResponse("Pycon Africa 2019 as not started.","Pycon Africa 2019 as not started."))
                    dialogflow_response.add(LinkOutSuggestion("See Schedule Online","https://africa.pycon.org/schedule/"))
            response = flask_app.response_class(response=dialogflow_response.get_final_response(),mimetype='application/json')
        else:
            # table_rows = [
            #     TableCell(cell_text=['Text 1','Text 2','Text 3']),
            #     TableCell(cell_text=['Text 12','Text 22','Text 32'])
            # ]
            # dialogflow_response.add(Table(rows=table_rows,columns=['Header 1','Header 2','Header 3'],add_dividers=True))
            dialogflow_response = DialogflowResponse()
            dialogflow_response.add(SimpleResponse("Welcome to my test dialogflow webhook","Welcome to my test dialogflow webhook"))
            dialogflow_response.add(Suggestions(["About","Sync","More info"]))
            response = jsonify(dialogflow_response.get_final_response())
            print(dialogflow_response.get_final_response())
        return response
    else:
        return_data = {
            'error' : 0,
            'message' : 'Successful'
        }
        return flask_app.response_class(response=json.dumps(return_data),mimetype='application/json')


if __name__ == "__main__":
    flask_app.run(host='127.0.0.1', port=8080, debug=True)