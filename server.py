from os import path
from turtle import position
from flask import redirect, render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String
from src import create_app


template_dir = path.abspath("/flask-demo/templates")
static_dir = path.abspath("/flask-demo/static")
app = create_app()
app.template_folder = template_dir
app.static_folder = static_dir

db = SQLAlchemy(app)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:@localhost/users"


class User(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    fullName = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False)
    job = Column(String(255), nullable=False)
    title = Column(String(255), nullable=False)
    position = Column(String(255), nullable=False)

    def __repi__(self):
        return f"<User {self.fullName}>"

    def __init__(self, fulName, email, job, title, position):
        self.fullName = fulName
        self.email = email
        self.job = job
        self.title = title
        self.position = position


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        users = User.query.order_by(User.id).all()
        print(len(users))
        return render_template("index.html", users=users)
    else:
        fullName = request.form["fullName"]
        job = request.form["job"]
        email = request.form["email"]
        title = request.form["title"]
        position = request.form["position"]
        print(fullName, job, email, title, position)
        user = User(fullName, email, job, title, position)
        db.session.add(user)
        db.session.commit()
        return redirect("/")


@app.route("/delete/<int:id>")
def delete_user(id):
    user = User.query.filter_by(id=id).first()
    print(user)
    try:
        db.session.delete(user)
        db.session.commit()
        return redirect("/")
    except Exception as e:
        print(e)
        return "There are problem deleting that user"


if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)
