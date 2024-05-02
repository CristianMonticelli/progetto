from flask import Flask, render_template, request, redirect, url_for
import json

app = Flask(__name__)
lista_esercizii_istruttore = []
FILE_PATH = "lista_esercizii_istruttore.json"  # Percorso del file JSON per salvare i dati
try:
    with open(FILE_PATH, 'r') as file:
        lista_esercizii_istruttore = json.load(file)
except FileNotFoundError:
    pass

FILE_PATH = "registered_users.json"  # Percorso del file JSON per salvare i dati
try:
    with open(FILE_PATH, 'r') as file:
        registered_users = json.load(file)
except FileNotFoundError:
    pass

lista_esercizii = {}
FILE_PATH = "lista_esercizii.json"  # Percorso del file JSON per salvare i dati
try:
    with open(FILE_PATH, 'r') as file:
        lista_esercizii = json.load(file)
except FileNotFoundError:
    pass
# Pagina iniziale con un bottone per reindirizzare

@app.route('/')
def index():
    return render_template('login2.html')

@app.route('/login', methods=['POST'])
def login():
    name = request.form['name']
   
    global registered_users
    if name=='istruttore':
        return render_template('primaria.html')
    if name=='capo':
        return render_template('segreteria.html')

@app.route('/registrazione_utenti', methods=['POST'])
def registrazione_utenti():
    name = request.form['name']
    global lista_esercizii
    lista_esercizii[name] = []
    file_json = "lista_esercizii.json"
    with open(file_json, "w") as f:
        json.dump(lista_esercizii, f)
    f.close()
    return render_template('segreteria.html')


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

@app.route('/aggiungi_titoletto', methods=['POST'])
def aggiungi_titoletto():
    numero = 0
    lista_esercizii.append(numero+1)
    return render_template('primaria.html', lista_esercizii=lista_esercizii)

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


if __name__ == '__main__':
    app.run(debug=True)