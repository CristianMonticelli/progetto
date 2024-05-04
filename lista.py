from flask import Flask, render_template, request, redirect, url_for
import json

app = Flask(__name__)


FILE_PATH = "registered_users.json" 
try:
    with open(FILE_PATH, 'r') as file:
        registered_users = json.load(file)
except FileNotFoundError:
    registered_users = {"utente": {}, "istruttore": {}}


@app.route('/')
def index():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    email = request.form['email']
    password = request.form['password']
    type_account = request.form['type_account']
    global registered_users
    

    
    for user in registered_users[type_account]:
        if user['username'] == username and user['password'] == password and user['email'] == email:
            return 'Login successful!'
    
    return render_template('errorereg.html')

@app.route('/pagina_di_registrazione', methods=['POST'])
def pagina_di_registrazione():
    return render_template('registrazione.html')

@app.route('/registrazione', methods=['POST'])
def registrazione():
    username = request.form['username']
    email = request.form['email']
    password = request.form['password']
    peso = request.form['peso']
    eta = request.form['email']
    altezza = request.form['password']

    tipo_account = request.form['tipo_account']
    global registered_users
    
    
    #aggiungi controllo password
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
                                            'password':password
                                        }
    
    file_json = "registered_users.json"
    with open(file_json, "w") as f:
        json.dump(registered_users, f)
    f.close()
    return render_template('login.html')
#
#@app.route('/primaria', methods=['GET', 'POST'])
#def primaria():
#    name = request.form
#    global lista_esercizii
#
#    if request.method == 'POST':
#        lista_esercizii[name].append({
#        'titolo':request.form['titolo'],   
#        'p11' : request.form['11'],
#        'p12' : request.form['12'],
#        'p21' : request.form['21'],
#        'p22' : request.form['22'],
#        'p31' : request.form['31'],
#        'p32' : request.form['32'],
#        'attrezzo' : request.form['attrezzo'],
#        'nota' : request.form['nota']})
#        lista_esercizii_istruttore.append({
#        'titolo':request.form['titolo'],   
#        'p11' : request.form['11'],
#        'p12' : request.form['12'],
#        'p21' : request.form['21'],
#        'p22' : request.form['22'],
#        'p31' : request.form['31'],
#        'p32' : request.form['32'],
#        'attrezzo' : request.form['attrezzo'],
#        'nota' : request.form['nota']})
#        file_json = "lista_esercizii_istruttore.json"
#        with open(file_json, "w") as f:
#            json.dump(lista_esercizii_istruttore, f)
#        f.close()
#
#
#
#        file_json = "lista_esercizii.json"
#        with open(file_json, "w") as f:
#            json.dump(lista_esercizii, f)
#        f.close()
#        
#        return render_template('primaria.html', lista_esercizii=lista_esercizii)
#    return render_template('primaria.html',lista_esercizii=lista_esercizii)
#
## Pagina di destinazione
#@app.route('/secondaria')
#def pagina_destinazione():
#
#    global lista_esercizii_istruttore
#    return render_template('seconda.html', lista_prefabbricati=lista_esercizii_istruttore)
#
#@app.route('/aggiungi_titoletto', methods=['POST'])
#def aggiungi_titoletto():
#    numero = 0
#    lista_esercizii.append(numero+1)
#    return render_template('primaria.html', lista_esercizii=lista_esercizii)
#
#@app.route('/predefiniti',methods=['POST'])
#def prefabbricato():
#    lista_prefabbricati = {}
#    lista_prefabbricati = {
#        'p11' : request.form['11panca'],
#        'p12' : request.form['12panca'],
#        'p21' : request.form['21panca'],
#        'p22' : request.form['22panca'],
#        'p31' : request.form['31panca'],
#        'p32' : request.form['32panca'],
#        'attrezzo' : request.form['attrezzopanca'],
#        'nota' : request.form['notapanca']}
#
#    return render_template('secondaria.html',lista_prefabbricati=lista_prefabbricati)


if __name__ == '__main__':
    app.run(debug=True)