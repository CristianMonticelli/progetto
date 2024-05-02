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
    username = request.form['username']
    gym = request.form['gym']
    email = request.form['email']
    global registered_users
    

    if gym in registered_users:
        for user in registered_users[gym]:
            if user['username'] == username and user['password'] == password:
                return 'Login successful!'
    return render_template('errorereg.html')

@app.route('/pagina_di_registrazione', methods=['POST'])
def pagina_di_registrazione():
    return render_template('registrazione.html')

@app.route('/registrazione', methods=['POST'])
def registrazione():
    username = request.form['username']
    email = request.form['email']
    gym = request.form['gym']
    password = request.form['password']

    global registered_users

    if gym not in registered_users:
        registered_users[gym] = []


    registered_users[tipe].append({'username':username,
                              'email':email,
                              'password':password})

    file_json = "registrazioni.json"
    with open(file_json, "w") as f:
        json.dump(registered_users, f)
    f.close()


#@app.route('/registrazione_palestra', methods=['POST'])
#def registrazione_palestra():
#    gym = request.form['palestra']
#    sorte = request.form['sorte']
#    capo = request.form['capo']
#    global registered_users
#    if sorte == 'aggiungeri':
#        registered_users[gym] = {'clienti':[],
#                                 'istruttori':[],
#                                 'capo':{'name':capo,
#                                         'password':capo + gym}}#e' inteso chiunque aggiunga i clienti
#        messaggio = f'la palestra {gym} e stata aggiunta con successo'
#    if sorte == 'rimuovi':
#        if gym not in registered_users:
#            messaggio = f'la palestra {gym} non esiste'
#        else:
#            registered_users.pop(gym)
#            messaggio = f'la palestra {gym} e stata eliminata'
#
#    with open(FILE_PATH, 'w') as file:
#        json.dump(registered_users, file)
#    return render_template('io.html',messaggio=messaggio)
#
#
#@app.route('/registrazione_utenti', methods=['POST'])
#def registrazione_utenti():
#    name = request.form['name']
#    surname = request.form['surname']
#    sorte = request.form['sorte']
#    gym = request.form['palestra']
#    global registered_users
#    if gym in registered_users:
#        for user in registered_users[gym]:
#            if sorte == 'istruttori':
#                user['istruttori'].append({'name':name,
#                             'surname':surname,
#                             'password':gym + 'istruttori'})
#            elif sorte == 'clienti':
#                registered_users[gym]['clienti'].append({'name':name,
#                             'surname':surname,
#                             'password':gym + 'clienti',
#                             'scheda':[]})
#            else:
#                for dizionario in user['istruttori']:
#                    if name in dizionario.values() and surname in dizionario.values():
#                        indice = user['istruttori'].index(dizionario)
#                        user['istruttori'].pop(indice)
#                    
#                #for dizionario in user['istruttori']:
#                #    if name in dizionario.values() and dato2 in dizionario.values():
#                #        return True
#
#
#
#    with open(FILE_PATH, 'w') as file:
#        json.dump(registered_users, file)
#
#    #return f'sorte = {sorte}'
#    return render_template('capo.html')
if __name__ == '__main__':
    app.run(debug=True)