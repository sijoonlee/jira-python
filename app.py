from flask import Flask, jsonify, render_template, request
from flask_restful import Api, Resource
from flask_cors import CORS, cross_origin
#from wtforms import Form, StringField, IntegerField, PasswordField, validators, SubmitField, SelectField 
#https://wtforms.readthedocs.io/en/2.3.x/crash_course/
from businessLogic.metrics import sprint
from businessLogic.db import queries

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
api = Api(app)


# sprint information
# ex) http://0.0.0.0:12345/sprintBetween?start=2020-01-01&end=2020-03-01&boardId=93
@app.route('/sprintBetween', methods=['GET'])
@cross_origin()
def getSprintBetween():
    startStr = request.args.get("start") # "2020-01-01"
    endStr = request.args.get("end") # "2020-03-01"
    boardId = request.args.get("boardId") # 93 for omp
    df = sprint.calculateWorkDonePercentage(boardId, startStr, endStr)
    html = df.to_html()
    print(html)
    response = jsonify({"state":200, "message":html})
    print(response)
    return response

@app.route('/sprintInBoard', methods=['GET'])
@cross_origin()
def getSprintInBoard():
    boardId = request.args.get("boardId", "*")
    df = queries.getSprintByBoardId(boardId)
    json = df.to_json()
    response = jsonify({"state":200, "message":json})
    return response


@app.route('/sprint', methods=['GET'])
@cross_origin()
def getSprint():
    sprintId = request.args.get("sprintId", "*")
    df = queries.getSprintById(sprintId)
    json = df.to_json()
    response = jsonify({"state":200, "message":json})
    return response

@app.route('/board', methods=['GET'])
@cross_origin()
def getBoard():
    boardId = request.args.get("boardId", "*")
    df = queries.getBoardById(boardId)
    json = df.to_json()
    response = jsonify({"state":200, "message":json})
    return response
# message looks like
# {
#     "id": {
#         "0": "40",
#         "1": "50",
#         "2": "62"
#     },
#     "name": {
#         "0": "Dev",
#         "1": "Dev Board - Core",
#         "2": "PM Board - OMP"
#     },
#     "type": {
#         "0": "scrum",
#         "1": "scrum",
#         "2": "kanban"
#     }
# }

@app.route('/issue', methods=['GET'])
@cross_origin()
def getIssue():
    issueId = request.args.get("issueId", "*")
    df = queries.getIssueById(issueId)
    json = df.to_json()
    response = jsonify({"state":200, "message":json})
    return response

@app.route('/issueBySprint', methods=['GET'])
@cross_origin()
def getIssueBySprint():
    sprintId = request.args.get("sprintId", "*")
    df = queries.getIssueBySprintId(sprintId)
    json = df.to_json()
    response = jsonify({"state":200, "message":json})
    return response


@app.route('/post', methods=['POST'])
def post():
    user_input = request.get_json()
    print(user_input)
    state = 200
    respond = "hello"
    return jsonify({"state":state, "message":respond})

if __name__=="__main__":
    app.run(host='0.0.0.0', port=12345)