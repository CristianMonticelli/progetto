from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Dati di esempio per la registrazione (da sostituire con un database reale)
registered_users = {}

@app.route('/')
def index():
    return render_template('indice.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    
    # Qui puoi aggiungere la logica per verificare se username e password sono corretti
    # Ad esempio, puoi confrontarli con valori fissi o con valori memorizzati in un database
    
    # Esempio di verifica di un username e password fissi
    if username == 'admin' and password == 'password':
        return 'Login successful!'
    else:
        return 'Invalid username or password. Please try again.'

@app.route('/registrazione', methods=['POST'])
def registrazione():
    username = request.form['username']
    password = request.form['password']
    
    # Aggiungere l'utente registrato al dizionario dei registri (da sostituire con un database reale)
    registered_users[username] = password
    
    return 'Registration successful!'

if __name__ == '__main__':
    app.run(debug=True)