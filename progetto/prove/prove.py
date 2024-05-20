from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Lista di utenti e istruttori
users = [
    {"nome": "Alice", "cognome": "Rossi", "password": "password1"},
    {"nome": "Bob", "cognome": "Bianchi", "password": "password2"},
    {"nome": "Charlie", "cognome": "Verdi", "password": "password3"}
]

istruttori = [
    {"nome": "David", "cognome": "Smith", "password": "password4"},
    {"nome": "Emma", "cognome": "Johnson", "password": "password5"}
]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    # Controlla se l'utente è un istruttore
    for istruttore in istruttori:
        if istruttore['nome'] == username and istruttore['password'] == password:
            return redirect(url_for('istr'))

    # Controlla se l'utente è un utente normale
    for user in users:
        if user['nome'] == username and user['password'] == password:
            return redirect(url_for('ute'))

    return "Credenziali non valide"

@app.route('/istr')
def istr():
    return render_template('istr.html')

@app.route('/ute')
def ute():
    return render_template('ute.html')

if __name__ == '__main__':
    app.run(debug=True)
