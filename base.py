from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')
@app.route('/altro')
def altro():
    return render_template('altro.html')