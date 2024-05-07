from flask import Flask, render_template, request, redirect, url_for
import json
import re
import random
app = Flask(__name__)


FILE_PATH = "registered_users.json" 
registered_users = {}
try:
    with open(FILE_PATH, 'r') as file:
        registered_users = json.load(file)
except FileNotFoundError:
    pass



@app.route('/')
def indexS():
    return render_template('login.html')
    #return render_template('lo.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    email = request.form['email']
    password = request.form['password']
    tipo_account = request.form['tipo_account']
    global registered_users
    

    
    
    if username in registered_users.get(tipo_account, {}):
        if password==registered_users[tipo_account][username]['password'] and email==registered_users[tipo_account][username]['email']:
            if tipo_account=='istruttore':
                
                return render_template('istruttore.html',nome=username,istruttore=registered_users[tipo_account][username],valutazione =3)
            else:
                
                return render_template('utente.html',immagine=random.randint(1, 3))
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
    eta = request.form['email']
    altezza = request.form['password']

    tipo_account = request.form['tipo_account']
    global registered_users
    messaggio = ''
    
    if username in registered_users.get(tipo_account, {}):
        
        messaggio+='Username already exists.' 
    if re.search(r'\d{3,}', password):
        messaggio+="Don't put number sequences like 123 in your password."
    if not re.search(r'[A-Z]', password):
        messaggio+="Put at least one uppercase capital letter in your password."
    
    if messaggio != '':
        return render_template('registrazione.html',messaggio=messaggio)
    if tipo_account=="utente":
        
        registered_users[tipo_account][username]={
                                            'email':email,
                                            'password':password,
                                            'peso':peso,
                                            'eta':eta,
                                            'altezza':altezza
                                        }
    else:
        registered_users[tipo_account][username]={
                                            'email':email,
                                            'password':password,
                                            'stelle':0,
                                            'commenti':[],
                                            'iscritti':[]
                                        }
    
    file_json = "registered_users.json"
    with open(file_json, "w") as f:
        json.dump(registered_users, f)
    f.close()
    return render_template('login.html')
@app.route('/iscrizione', methods=[ 'POST'])
def iscrizione():
    username = request.form['username']
    iscrizione=request.form('iscrizione')
    registered_users['istruttore'][iscrizione]['iscritti'].append({'username':username,
                                                                   'email':registered_users['utente'][username]['email'],
                                                                   'peso':registered_users['utente'][username]['peso'],
                                                                    'eta':registered_users['utente'][username]["eta"],
                                                                    'altezza':registered_users['utente'][username]})

@app.route('/primaria', methods=['GET', 'POST'])
def primaria():
    name = request.form
    global lista_esercizii

    if request.method == 'POST':
        lista_esercizii[name].append({
        'titolo':request.form['titolo'],   
        'p11' : request.form['11'],
        'p12' : request.form['12'],
        'p21' : request.form['21'],
        'p22' : request.form['22'],
        'p31' : request.form['31'],
        'p32' : request.form['32'],
        'attrezzo' : request.form['attrezzo'],
        'nota' : request.form['nota']})
        lista_esercizii_istruttore.append({
        'titolo':request.form['titolo'],   
        'p11' : request.form['11'],
        'p12' : request.form['12'],
        'p21' : request.form['21'],
        'p22' : request.form['22'],
        'p31' : request.form['31'],
        'p32' : request.form['32'],
        'attrezzo' : request.form['attrezzo'],
        'nota' : request.form['nota']})
        file_json = "lista_esercizii_istruttore.json"
        with open(file_json, "w") as f:
            json.dump(lista_esercizii_istruttore, f)
        f.close()



        file_json = "lista_esercizii.json"
        with open(file_json, "w") as f:
            json.dump(lista_esercizii, f)
        f.close()
        
        return render_template('primaria.html', lista_esercizii=lista_esercizii)
    return render_template('primaria.html',lista_esercizii=lista_esercizii)

# Pagina di destinazione
@app.route('/secondaria')
def pagina_destinazione():

    global lista_esercizii_istruttore
    return render_template('seconda.html', lista_prefabbricati=lista_esercizii_istruttore)



@app.route('/predefiniti',methods=['POST'])
def prefabbricato():
    lista_prefabbricati = {}
    lista_prefabbricati = {
        'p11' : request.form['11panca'],
        'p12' : request.form['12panca'],
        'p21' : request.form['21panca'],
        'p22' : request.form['22panca'],
        'p31' : request.form['31panca'],
        'p32' : request.form['32panca'],
        'attrezzo' : request.form['attrezzopanca'],
        'nota' : request.form['notapanca']}

    return render_template('secondaria.html',lista_prefabbricati=lista_prefabbricati)

@app.route('/scegli_istruttore')
def scegli_istruttore():
    return render_template('istruttori.html',istruttori=registered_users['istruttore'])

@app.route('/utente', methods=['POST'])
def utente():
    return render_template('utente.html')

@app.route('/istruttore', methods=['POST'])
def istruttore():
    return render_template('istruttore.html')

if __name__ == '__main__':
    app.run(debug=True)