from flask import Flask, render_template, request, redirect, url_for
utenti = []
FILE_PATH = "registered_users.json"  # Percorso del file JSON per salvare i dati
try:
    with open(FILE_PATH, 'r') as file:
        registered_users = json.load(file)
except FileNotFoundError:
    pass

app = Flask(__name__)
@app.route('/')
def index():
    return render_template('segreteria.html')


@app.route('/registrazione_utenti', methods=['POST'])
def registrazione_utenti():
    name = request.form['name']