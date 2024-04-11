from flask import Flask, send_from_directory, url_for, render_template
from markupsafe import escape

# import matplotlib.pyplot as plt

app = Flask(__name__)


@app.route("/")
def hello_world():
    return render_template("hello.html")


@app.route("/hello/")
@app.route("/hello/<name>")
def hello(name=None):
    return render_template("hello.html")


@app.route("/listastudenti")
def print_students():
    students = ["Ana", "Ion", "Maria", "George"]
    return render_template("students.html", students=students)


@app.route("/square_number/<int:number>")
def square_number(number):
    return f"The square of {number} is {number**2}!"