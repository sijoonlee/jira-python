from flask import Flask, jsonify, render_template, request
from flask_restful import Api, Resource
# from wtforms import Form, StringField, IntegerField, PasswordField, validators, SubmitField, SelectField
from businessLogic.metrics import sprint

app = Flask(__name__)
api = Api(app)


# sprint information
# 
@app.route('/sprint', methods=['GET'])
def get():
    startStr = request.args.get("start") # "2020-01-01"
    endStr = request.args.get("end") # "2020-03-01"
    boardId = request.args.get("boardId") # 93 for omp
    #df = sprint.sprintsStartedBetween(startStr, endStr) 
    #html = df.to_html()
    df = sprint.calculateWorkDonePercentage(boardId, startStr, endStr)
    html = df.to_html()
    return html # jsonify({"state":state, "message":respond})

@app.route('/post', methods=['POST'])
def post():
    user_input = request.get_json()
    print(user_input)
    state = 200
    respond = "hello"
    return jsonify({"state":state, "message":respond})

if __name__=="__main__":
    app.run(host='0.0.0.0', port=12345)