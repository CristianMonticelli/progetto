from flask import Flask, render_template, request, redirect, url_for
import json
import re
app = Flask(__name__)
FILE_PATH = "registered_users.json" 
registered_users = {'utenti':[],
                    'istruttori':[]}
try:
    with open(FILE_PATH, 'r') as file:
        registered_users = json.load(file)
except FileNotFoundError:
    pass

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/login', methods=['POST','GET'])
def login():
    username = request.form['username']
    email = request.form['email']
    password = request.form['password']
    
    for user in registered_users['utenti']:
        if user["username"]==username:
           return render_template('utente.html')
        
    for istruttori in registered_users['istruttori']:
        if istruttori["username"]==username:
            return render_template('istruttori.html')
        
    return render_template('errorereg.html')

@app.route('/pagina_di_registrazione', methods=['POST'])
def pagina_di_registrazione():
    return render_template('registrazione.html')

@app.route('/registrazione', methods=['POST'])
def registrazione():
    username = request.form['username']
    email = request.form['email']
    #password = request.form['password']
    password = 'Alto'
    peso = request.form['peso']
    eta = request.form['eta']
    altezza = request.form['altezza']

    
    
    messaggio = ''
    
    for user in registered_users['utenti']:
        if user["username"]==username:
            messaggio+='Username already exists.' 
    for istruttori in registered_users['istruttori']:
        if istruttori["username"]==username:
            messaggio+='Username already exists.' 

    if re.search(r'\d{3,}', password):
        messaggio+="Don't put number sequences like 123 in your password."
    if not re.search(r'[A-Z]', password):
        messaggio+="Put at least one uppercase capital letter in your password."
    
    if messaggio != '':
        return render_template('registrazione.html',messaggio=messaggio)
    
        
    registered_users['utenti'].append({'username':username,
                                'email':email,
                                'password':password,
                                'peso':peso,
                                'eta':eta,
                                'altezza':altezza,
                                'iscrizione':False})
    
    
    file_json = "registered_users.json"
    with open(file_json, "w") as f:
        json.dump(registered_users, f)
    f.close()
    return render_template('login.html')




@app.route('/pagina_di_registrazione_istruttori', methods=['POST'])
def pagina_di_registrazione_istruttore():
    return render_template('registrazione_istruttore.html')

@app.route('/termini-condizioni')
def termini_condizioni():
    return render_template('termini_condizioni.html')

@app.route('/registrazione_istruttore', methods=['POST'])
def registrazione_istruttori():
    username = request.form['username']
    email = request.form['email']
    #password = request.form['password']
    password = 'Alto'
    titolo = request.form['titolo']
    eta = request.form['eta']
    

    
    
    messaggio = ''
    
    for user in registered_users['utenti']:
        if user["username"]==username:
            messaggio+='Username already exists.' 
    for istruttori in registered_users['istruttori']:
        if istruttori["username"]==username:
            messaggio+='Username already exists.' 

    if re.search(r'\d{3,}', password):
        messaggio+="Don't put number sequences like 123 in your password."
    if not re.search(r'[A-Z]', password):
        messaggio+="Put at least one uppercase capital letter in your password."
    
    if messaggio != '':
        return render_template('registrazione.html',messaggio=messaggio)
    
        
    registered_users['istruttori'].append({'username':username,
                                'email':email,
                                'password':password,
                                'titolo':titolo,
                                'eta':eta,
                                'iscritti':[]})
    
    
    file_json = "registered_users.json"
    with open(file_json, "w") as f:
        json.dump(registered_users, f)
    f.close()
    return render_template('login.html')




if __name__ == '__main__':
    app.run(debug=True)