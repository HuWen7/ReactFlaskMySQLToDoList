# coding:utf-8
import os
from flask import Flask, request, jsonify, redirect, send_file
from flask_cors import CORS

from schema import db, User, ToDoList
from login import login_required, TOKEN_MACHINE
from state import RegisterState, LoginState, DecodeTokenState

from constant import PORT, MYSQL_URL


app = Flask("Try Login")
app.debug = True
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = MYSQL_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db.init_app(app)


@app.route("/")
def hello_world():
    return "Hello World"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=PORT)