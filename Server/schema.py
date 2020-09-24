from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class User(db.Model):
    __tablename__ = "user_login"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(24), nullable=False)
    password = db.Column(db.String(24), nullable=False)

    def __init__(self, username, password):
        self.username = username
        self.password = password

class ToDoList(db.Model):
    __tablename__ = "todolist"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(24), nullable=False)
    content = db.Column(db.String(24), nullable=False)
    isDone = db.Column(db.Integer, nullable=False)

    def __init__(self, username, content, is_done):
        self.username = username
        self.content = content
        self.isDone = is_done

    def get_config(self):
        return {
            "id": self.id,
            "username": self.username,
            "content": self.content,
            "isDone": self.isDone
        }

if __name__ == "__main__":
    db.create_all()