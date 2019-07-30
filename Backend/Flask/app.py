from flask import Flask, request, abort, jsonify
from pydialogflow_fulfillment import *

flask_app = Flask(__name__)

@flask_app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        dialogflow_request = DialogflowRequest(request.data)
        if dialogflow_request.get_intent_displayName() == "welcome_intent":
            dialogflow_response = DialogflowResponse("Welcome to my test dialogflow webhook")
            dialogflow_response.add(SimpleResponse("Welcome to my test dialogflow webhook","Welcome to my test dialogflow webhook"))
            response = flask_app.response_class(response=dialogflow_response.get_final_response(),mimetype='application/json')
            print(type(response))
        else:
            dialogflow_response = DialogflowResponse()
            dialogflow_response.add(SimpleResponse("Welcome to my test dialogflow webhook","Welcome to my test dialogflow webhook"))
            dialogflow_response.add(Suggestions(["About","Sync","More info"]))
            response = jsonify(dialogflow_response.get_final_response())
            print(dialogflow_response.get_final_response())
        return response
    else:
        abort(404)


if __name__ == "__main__":
    flask_app.run(debug=True)