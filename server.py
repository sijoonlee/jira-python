from flask import Flask, jsonify, render_template, request
from flask_restful import Api, Resource
from flask_cors import CORS, cross_origin
from businessLogic.metrics import sprint
from businessLogic.db import queries
from db.sqlite3.connector import SqliteConnector

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
api = Api(app)

# Below is the example return value from endpoints
# {
#   columns: ['id','key']
#   index: ['0','1']
#   data: [['1','key-A'],['2','key-B']]
# }

# sprint information
# ex) http://0.0.0.0:12345/sprintBetween?start=2020-01-01&end=2020-03-01&boardId=93
@app.route('/sprintBetween', methods=['GET'])
@cross_origin()
def getSprintBetween():
    startStr = request.args.get("start") # "2020-01-01"
    endStr = request.args.get("end") # "2020-03-01"
    boardId = request.args.get("boardId") # 93 for omp
    df = sprint.calculateWorkDonePercentage(SqliteConnector(), boardId, startStr, endStr)
    return df.to_json(orient="split")

@app.route('/sprintInBoard', methods=['GET'])
@cross_origin()
def getSprintInBoard():
    boardId = request.args.get("boardId", "*")
    df = queries.getSprintByBoardId(SqliteConnector(), boardId)
    return df.to_json(orient="split")

@app.route('/sprint', methods=['GET'])
@cross_origin()
def getSprint():
    sprintId = request.args.get("sprintId", "*")
    df = queries.getSprintById(SqliteConnector(),sprintId)
    return df.to_json(orient="split")

@app.route('/board', methods=['GET'])
@cross_origin()
def getBoard():
    boardId = request.args.get("boardId", "*")
    df = queries.getBoardById(SqliteConnector(),boardId)
    return df.to_json(orient="split")

@app.route('/project', methods=['GET'])
@cross_origin()
def getProject():
    projectId = request.args.get("projectId", "*")
    df = queries.getProjectById(SqliteConnector(),projectId)
    return df.to_json(orient="split")

@app.route('/issue', methods=['GET'])
@cross_origin()
def getIssue():
    issueId = request.args.get("issueId", "*")
    df = queries.getIssueById(SqliteConnector(),issueId)
    return df.to_json(orient="split")

@app.route('/issueBySprint', methods=['GET'])
@cross_origin()
def getIssueBySprint():
    sprintId = request.args.get("sprintId", "*")
    df = queries.getIssueBySprintId(SqliteConnector(),sprintId)
    return df.to_json(orient="split")


# @app.route('/post', methods=['POST'])
# def post():
#     user_input = request.get_json()
#     print(user_input)
#     state = 200
#     respond = "hello"
#     return jsonify({"state":state, "message":respond})

if __name__=="__main__":
    app.run(host='0.0.0.0', port=12345)