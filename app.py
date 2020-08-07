from flask import Flask, jsonify, render_template, request
from flask_restful import Api, Resource
# from wtforms import Form, StringField, IntegerField, PasswordField, validators, SubmitField, SelectField


app = Flask(__name__)
api = Api(app)

@app.route('/get', methods=['GET'])
def get():
    #user_input = request.get_json()
    #print(user_input)
    state = 200
    respond = "hello"
    return jsonify({"state":state, "message":respond})

@app.route('/post', methods=['POST'])
def post():
    user_input = request.get_json()
    print(user_input)
    state = 200
    respond = "hello"
    return jsonify({"state":state, "message":respond})

if __name__=="__main__":
    app.run(host='0.0.0.0', port=12345)