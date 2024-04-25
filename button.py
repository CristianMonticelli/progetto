from flask import Flask, render_template, request
import json
app = Flask(__name__)
registered_users = {}
FILE_PATH = "registered_users.json"  # Percorso del file JSON per salvare i dati
try:
    with open(FILE_PATH, 'r') as file:
        registered_users = json.load(file)
except FileNotFoundError:
    pass


@app.route('/')
def index():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    name = request.form['name']
    surname = request.form['surname']
    gym = request.form['gym']
    password = request.form['password']
    global registered_users
    if name=='io' and surname=='io' and password=='password':
        return render_template('io.html')
    
    if gym in registered_users:
        for user in registered_users[gym]:
            if user['name'] == name and user['surname'] == surname and user['password'] == password:
                return 'Login successful!'
    return render_template('errorereg.html')
        
@app.route('/pagina_di_registrazione', methods=['POST'])
def pagina_di_registrazione():
    return render_template('registrazione.html')

@app.route('/registrazione', methods=['POST'])
def registrazione():
    name = request.form['name']
    surname = request.form['surname']
    gym = request.form['gym']
    password = request.form['password']
    
    global registered_users

    if gym not in registered_users:
        registered_users[gym] = []

    
    registered_users[gym].append({'name':name,
                              'surname':surname,
                              'password':password})
    
    file_json = "registrazioni.json"
    with open(file_json, "w") as f:
        json.dump(registered_users, f)
    f.close()
    
@app.route('/registrazione_palestra', methods=['POST'])
def registrazione_palestra():
    gym = request.form['palestra']
    sorte = request.form['sorte']

    if gym not in registered_users:
        registered_users[gym] = {'clienti':[],
                                 'istruttori':[]}

    with open(FILE_PATH, 'w') as file:
        json.dump(registered_users, file)


@app.route('//registrazione_utenti', methods=['POST'])
def registrazione_palestra():
    utente = request.form['utente']
    sorte = request.form['sorte']
    gym = request.form['palestra']

    if gym in registered_users:
        for user in registered_users[gym][sorte]:
            if sorte == 'istruttori':
                user.append()
            user['filled'] = True

    with open(FILE_PATH, 'w') as file:
        json.dump(registered_users, file)

    return f'sorte = {sorte}'
if __name__ == '__main__':
    app.run(debug=True)
