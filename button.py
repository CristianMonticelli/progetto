from flask import Flask, render_template, request

app = Flask(__name__)
registered_users = {}
@app.route('/')
def index():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    name = request.form['name']
    surname = request.form['surname']
    gym = request.form['gym']
    password = request.form['password']
    
    # Qui puoi aggiungere la logica per verificare se username e password sono corretti
    # Ad esempio, puoi confrontarli con valori fissi o con valori memorizzati in un database
    
    # Esempio di verifica di un username e password fissi
    for i in registered_users[gym]:
        if name == 'name' and password == 'password' and surname=='surname':
            return 'Login successful!'
        else:
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
    registered_users[gym] = []
    # Aggiungere l'utente registrato al dizionario dei registri (da sostituire con un database reale)
    registered_users[gym].append({'name':name,
                              'surname':surname,
                              'password':password})
    return render_template('login.html')
if __name__ == '__main__':
    app.run(debug=True)
