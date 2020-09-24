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

@app.route("/login", methods=["POST"])
def login():
    proto = request.get_json()
    print "Recieve Login Request"
    user = User.query.filter_by(username=proto["username"], password=proto["password"]).first()
    if user:
        token = TOKEN_MACHINE.token_encode(**{"username": user.username})
        print "User ", user.username ,"Login Success"
        return jsonify({
            "STATE": LoginState.SUCCESS.name,
            "token": token
        })
    
    print "User Login Fail"
    return jsonify({"STATE": LoginState.FAIL.name})

@app.route("/auth_token", methods=["POST"])
def auth_token():
    proto = request.get_json()
    token = proto["token"]
    return jsonify({"STATE": TOKEN_MACHINE.token_decode(token).name})

@app.route("/register", methods=["POST"])
def register():
    proto = request.get_json()
    user = User.query.filter_by(username=proto["username"]).first()
    if user:
        return jsonify({"STATE": RegisterState.ALREADY.name})
    elif not(proto["username"] and proto["password"]):
        return jsonify({"STATE": RegisterState.EMPTY.name})
    else:
        user = User(username=proto["username"], password=proto["password"])
        db.session.add(user)
        db.session.commit()
        return jsonify({"STATE": RegisterState.SUCCESS.name})

@app.route("/user_info", methods=["POST"])
@login_required
def user_info():
    proto = request.get_json()
    return jsonify({
        "STATE": DecodeTokenState.SUCCESS.name,
        "USER_INFO": {"username": TOKEN_MACHINE.current_auth_user.username}
    })

@app.route("/user_todolist", methods=["POST"])
@login_required
def user_todolist():
    proto = request.get_json()
    todolist_query = ToDoList.query.filter_by(username=TOKEN_MACHINE.current_auth_user.username)
    todolist = list(map(lambda x: x.get_config(), todolist_query))
    return jsonify({
        "STATE": DecodeTokenState.SUCCESS.name,
        "TODOLIST": todolist
    })

@app.route("/todolist_add_item", methods=["POST"])
@login_required
def todolist_add_item():
    proto = request.get_json()
    item = ToDoList(**proto["item"])
    db.session.add(item)
    db.session.commit()
    return jsonify({
        "STATE": DecodeTokenState.SUCCESS.name,
        "ITEM": item.get_config()
    })

@app.route("/todolist_delete_item", methods=["POST"])
@login_required
def todolist_delete_item():
    proto = request.get_json()
    item = ToDoList.query.filter_by(id=proto["item"]["id"]).first()
    db.session.delete(item)
    db.session.commit()
    return jsonify({
        "STATE": DecodeTokenState.SUCCESS.name,
    })

@app.route("/todolist_change_item", methods=["POST"])
@login_required
def todolist_change_item():
    proto = request.get_json()
    item = ToDoList.query.filter_by(id=proto["item"]["id"]).first()
    for key, value in proto["item"].items():
        if key in ToDoList.__dict__:
            setattr(item, key, value)
    db.session.commit()
    return jsonify({
        "STATE": DecodeTokenState.SUCCESS.name,
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=PORT)