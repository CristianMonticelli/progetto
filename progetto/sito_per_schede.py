from flask import Flask, render_template, request, redirect, url_for
import random
app = Flask(__name__)

users = [
    {
        "username": "Bob",
        "eta": 30,
        "peso": 75,
        "altezza": 175,
        "password": "password2",
        "schede": []  
    },
    {
        "username": "Charlie",
        "eta": 35,
        "peso": 85,
        "altezza": 180,
        "password": "password3",
        "schede": []  
    },
    {
        "username": "Emma",
        "eta": 28,
        "peso": 65,
        "altezza": 160,
        "password": "password5",
        "schede": []  
    },
    {
        "username": "Frank",
        "eta": 32,
        "peso": 80,
        "altezza": 185,
        "password": "password6",
        "schede": []  
    },
    {
        "username": "Hannah",
        "eta": 29,
        "peso": 68,
        "altezza": 175,
        "password": "password8",
        "schede": []  
    },
    {
        "username": "Isaac",
        "eta": 33,
        "peso": 90,
        "altezza": 180,
        "password": "password9",
        "schede": []  
    }
]

istruttori = [
    {"username": "A", "password": "p", "eta": 25, "titolo studio": "Laurea in Economia", "utenti": [
        {"username": "Bob"},
        {"username": "Charlie"}
    ]},
    {"username": "David", "password": "password4", "eta": 30, "titolo studio": "Diploma di scuola superiore", "utenti": [
        {"username": "Emma"},
        {"username": "Frank"}
    ]},
    {"username": "Grace","password": "password7" ,"eta": 28, "titolo studio": "Master in Informatica", "utenti": [
        {"username": "Hannah"},
        {"username": "Isaac"}
    ]}
]



# Lista di esercizi come dizionari
esercizii = [
    {"esercizio": "Push-up", "ripetizioni": 20, "serie": 3, "immagine": "pushup.jpg"},
    {"esercizio": "Sit-up", "ripetizioni": 30, "serie": 3, "immagine": "situp.jpg"},
    {"esercizio": "Squat", "ripetizioni": 15, "serie": 3, "immagine": "squat.jpg"},
    {"esercizio": "Pull-up", "ripetizioni": 10, "serie": 3, "immagine": "pullup.jpg"},
    {"esercizio": "Plank", "ripetizioni": 1, "serie": 3, "immagine": "plank.jpg"},
    {"esercizio": "Lunge", "ripetizioni": 20, "serie": 3, "immagine": "lunge.jpg"}
]

# Dizionario per memorizzare gli esercizi selezionati per ogni utente
user_exercises = {user["username"]: [] for user in users}

@app.route('/')
def indexS():
    return render_template('login.html')

@app.route('/image-test')
def image_test():
    image_path = url_for('static', filename='squat.jpg')
    return f'<img src="{image_path}" alt="Girl in a jacket" width="500" height="600">'

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    # Controlla se l'utente è un istruttore
    for istruttore in istruttori:
        if istruttore['username'] == username and istruttore['password'] == password:
            
            iscritti = istruttore['utenti']
            return render_template('home.html', users=iscritti, username=username)

    # Controlla l'utente 
    for user in users:
        if user['username'] == username and user['password'] == password:
            return redirect(url_for('ute'))

    return "Credenziali non valide"

@app.route('/istr')
def istr():
    username = request.form['username']
    for istruttore in istruttori:
        iscritti = istruttore['utenti']
        return render_template('home.html', users=iscritti)

@app.route('/ute')
def ute():
    return render_template('ute.html')

@app.route('/select_user', methods=['GET'])
def select_user():
    username = request.args.get('username')
    if username:
        return redirect(url_for('user_profile', username=username))
    return redirect(url_for('istr'))

@app.route('/user/<username>', methods=['GET', 'POST'])
def user_profile(username):
    user = next((user for user in users if user["username"] == username), None)
    
    if user:
        user_selected_exercises = user_exercises[username]
        
        return render_template('user_profile.html', selected_user=user, esercizii=esercizii, selected_exercises=user_selected_exercises)
    else:
        return "Utente non trovato", 404

@app.route('/add_exercise/<username>', methods=['POST'])
def add_exercise(username):
    selected_exercise_name = request.form['selected_exercise']
    selected_exercise = next((exercise for exercise in esercizii if exercise["esercizio"] == selected_exercise_name), None)
    
    if selected_exercise:
        user = next((user for user in users if user["username"] == username), None)
        
        if user:
            user['schede'].append(selected_exercise)
            
    return redirect(url_for('user_profile', username=username))

@app.route('/remove_exercise/<username>', methods=['POST'])
def remove_exercise(username):
    exercise_name = request.form['exercise']
    user = next((user for user in users if user["username"] == username), None)
    if user:
        user['schede'] = [exercise for exercise in user['schede'] if exercise['esercizio'] != exercise_name]
    return redirect(url_for('user_profile', username=username))


@app.route('/add_user', methods=['POST'])
def add_user():
    new_user = {
        "username": request.form['username'],
        "eta": int(request.form['eta']),
        "peso": int(request.form['peso']),
        "altezza": int(request.form['altezza'])
    }
    
    # Trova l'istruttore che sta aggiungendo l'utente
    istruttore_username = request.form['istruttore']
    istruttore = next((istruttore for istruttore in istruttori if istruttore["username"] == istruttore_username), None)
    
    if istruttore:
        # Aggiungi l'utente alla lista degli utenti dell'istruttore
        istruttore['utenti'].append({"username": new_user["username"]})
        users.append(new_user)
        user_exercises[new_user["username"]] = []
        return redirect(url_for('index'))
    else:
        return "Istruttore non trovato"


if __name__ == "__main__":
    random_port = random.randint(1024, 49151)
    app.run(debug=True, port=random_port)
