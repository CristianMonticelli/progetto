from flask import Flask, render_template, request, redirect, url_for
import json
import re
import random
import matplotlib.pyplot as plt
from datetime import datetime

app = Flask(__name__)

USER_FILE_PATH = "users.json"
ISTRUTTORI_FILE_PATH = "istruttori.json"
ESERCIZI_FILE_PATH = "esercizii.json"
PUBBLICITA_FILE_PATH = "publicita.json"

pubblicita= []
try:
    with open(PUBBLICITA_FILE_PATH, 'r') as file:
        pubblicita = json.load(file)
except FileNotFoundError:
    pass

users = []
try:
    with open(USER_FILE_PATH, 'r') as file:
        users = json.load(file)
except FileNotFoundError:
    pass

istruttori = []
try:
    with open(ISTRUTTORI_FILE_PATH, 'r') as file:
        istruttori = json.load(file)
except FileNotFoundError:
    pass

esercizii = {}
try:
    with open(ESERCIZI_FILE_PATH, 'r') as file:
        esercizii = json.load(file)
except FileNotFoundError:
    pass

user_peso = {user["username"]: user.get("peso", []) for user in users}

def save_data(file_path, data):
    """Save data to the specified JSON file."""
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)

@app.route('/')
def indexS():
    """Render the login page with randomly selected images."""
    
    immagine1 = random.choice(pubblicita)
    immagine2 = random.choice(pubblicita)
    
    while immagine1 == immagine2:
        immagine2 = random.choice(pubblicita)
    
    return render_template('login.html', left_image=immagine1, right_image=immagine2)

@app.route('/image-test')
def image_test():
    """Test route to display an image."""
    image_path = url_for('static', filename='squat.jpg')
    return f'<img src="{image_path}" alt="Girl in a jacket" width="500" height="600">'

@app.route('/login', methods=['POST'])
def login():
    """Handle user login."""
    username = request.form['username']
    password = request.form['password']

    for istruttore in istruttori:
        if istruttore['username'] == username and istruttore['password'] == password:
            iscritti = istruttore.get('utenti', [])
            return render_template('home.html', users=iscritti, username=username)

    for user in users:
        if user['username'] == username and user['password'] == password:
            return redirect(url_for('ute', username=username))

    return "Credenziali non valide"

@app.route('/term')
def term():
    """Render the terms and conditions page."""
    return render_template('termini_condizioni.html')

@app.route('/istr/<username>')
def istr(username):
    """Render the instructor's homepage with their users."""
    for istruttore in istruttori:
        if istruttore['username'] == username:
            iscritti = istruttore['utenti']
        return render_template('home.html', users=iscritti)

@app.route('/ute/<username>')
def ute(username):
    user = next((user for user in users if user["username"] == username), None)
    if user:
        selected_exercises = user.get("schede", [])
        return render_template('ute.html', selected_user=user, selected_exercises=selected_exercises)
    return "User not found", 404

@app.route('/add_peso', methods=['POST'])
def add_peso():
    """Add a weight entry for the user."""
    username = request.form['username']
    peso = request.form['peso']
    
    if username in user_peso:
        user_peso[username].append({
            "date": datetime.now().strftime("%Y-%m-%d"),
            "peso": float(peso)
        })
    else:
        user_peso[username] = [{
            "date": datetime.now().strftime("%Y-%m-%d"),
            "peso": float(peso)
        }]

    for user in users:
        if user["username"] == username:
            user["peso"] = user_peso[username]
            break
    save_data(USER_FILE_PATH, users)

    return redirect(url_for('statistiche', username=username))

@app.route('/statistiche/<username>')
def statistiche(username):
    """Render the user's weight statistics."""
    user = next((user for user in users if user["username"] == username), None)
    peso = user_peso.get(username, [])

    if peso:
        dates = [entry["date"] for entry in peso]
        peso_values = [entry["peso"] for entry in peso]

        plt.figure(figsize=(10, 5))
        plt.plot(dates, peso_values, marker='o', linestyle='-', color='blue')
        plt.xlabel('Giorno')
        plt.ylabel('Peso (kg)')
        plt.title('Andamento del Peso nel Tempo')
        plt.xticks(rotation=45)
        plot_filename = f'static/{username}_weight_plot.png'
        plt.savefig(plot_filename)
        plot_url = url_for('static', filename=f'{username}_weight_plot.png')
    else:
        plot_url = None

    return render_template('statistiche.html', username=username, plot_url=plot_url)

@app.route('/select_user', methods=['GET'])
def select_user():
    """Redirect to the selected user's profile page."""
    username = request.args.get('username')
    if username:
        return redirect(url_for('user_profile', username=username))
    return redirect(url_for('istr'))

@app.route('/user_profile/<username>')
def user_profile(username):
    """Render the selected user's profile page."""
    user = next((user for user in users if user["username"] == username), None)
    if user:
        category = request.args.get('category')
        selected_exercises = user["schede"]
        current_category = esercizii.get(category, [])
        print(category)
        print(current_category)
        print(esercizii)
        return render_template('user_profile.html', selected_user=user, selected_exercises=selected_exercises, esercizii=esercizii, current_category=current_category)
    return "User not found", 404

@app.route('/view_workout/<username>')
def view_workout(username):
    """Render the selected user's workout page."""
    user = next((user for user in users if user["username"] == username), None)
    if user:
        selected_exercises = user["schede"]
        return render_template('ute.html', selected_user=user, selected_exercises=selected_exercises)
    return "User not found", 404

@app.route('/add_exercise/<username>', methods=['POST'])
def add_exercise(username):
    selected_exercise_name = request.form['selected_exercise']
    ripetizioni = request.form['ripetizioni']
    serie = request.form['serie']
    pausa = request.form['pausa']
    kg = request.form['kg']
    
    selected_exercise = next((exercise for category_exercises in esercizii.values() for exercise in category_exercises if exercise["esercizio"] == selected_exercise_name), None)
    
    if selected_exercise:
        user = next((user for user in users if user["username"] == username), None)
        
        if user:
            if "schede" not in user:
                user["schede"] = []
            new_exercise = {
                "esercizio": selected_exercise_name,
                "ripetizioni": ripetizioni,
                "serie": serie,
                "pausa": pausa,
                "kg":kg,
                "immagine": selected_exercise["immagine"]
            }
            user["schede"].append(new_exercise)
            save_data(USER_FILE_PATH, users)
    
    return redirect(url_for('user_profile', username=username))
@app.route('/remove_exercise/<username>', methods=['POST'])
def remove_exercise(username):
    """Remove an exercise from the user's workout plan."""
    exercise_name = request.form['exercise']
    
    user = next((user for user in users if user["username"] == username), None)
    
    if user and "schede" in user:
        user["schede"] = [exercise for exercise in user["schede"] if exercise['esercizio'] != exercise_name]
        save_data(USER_FILE_PATH, users)
    
    return redirect(url_for('user_profile', username=username))

@app.route('/pagina_di_registrazione/<tipo_registrazione>', methods=['POST'])
def pagina_di_registrazione(tipo_registrazione):
    """Render the registration page based on the type of registration."""
    if tipo_registrazione == "utente":
        return render_template('registrazione.html')

    return render_template('registrazione_istruttore.html')

def controllo_errori(username:str, password) -> str:
    """Check for errors in the username and password."""
    messaggio = ''
    for user in users:
        if user["username"] == username:
            messaggio += 'Username already exists.' 
    for istruttore in istruttori:
        if istruttore["username"] == username:
            messaggio += 'Username already exists.' 
    

    if re.search(r'\d{3,}', password):
        messaggio += "Don't put number sequences like 123 in your password."
    if not re.search(r'[A-Z]', password):
        messaggio += "Put at least one uppercase capital letter in your password."
    
    return messaggio

@app.route('/registrazione', methods=['POST'])
def registrazione():
    """Handle user registration."""
    username = request.form['username']
    password = request.form['password']
    email = request.form['email']
    peso = request.form['peso']
    eta = request.form['eta']
    altezza = request.form['altezza']
   
    messaggio = controllo_errori(username, password)
    
    if messaggio != '':
        return render_template('registrazione.html', messaggio=messaggio)
    
    nuovo_utente = {
        "username": username,
        "password": password,
        "email": email,
        "peso": [{
            "date": datetime.now().strftime("%Y-%m-%d"),
            "peso": float(peso)
        }],
        "eta": eta,
        "altezza": altezza
    }

    users.append(nuovo_utente)
    save_data(USER_FILE_PATH, users)

    return redirect(url_for('indexS'))

@app.route('/add_user/<username>', methods=['POST'])
def add_user(username):
    new_user = {
        "username": request.form['utent_name'],
        "email": request.form['email'],
    }
    
    
    istruttore = next((istruttore for istruttore in istruttori if istruttore["username"] == username), None)
    print(1)
    if istruttore:
       
        istruttore['utenti'].append(new_user)
        
        
        save_data(ISTRUTTORI_FILE_PATH, istruttori)
        print(2)
        return redirect(url_for('istr',username=username))
    else:
        return "utente non trovato"
    
@app.route('/registrazione_istruttore', methods=['GET', 'POST'])
def registrazione_istruttore():
    """Handle instructor registration."""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        titolo = request.form['titolo']
        eta = request.form['eta']

        messaggio = controllo_errori(username, password)

        if messaggio != '':
            return render_template('registrazione_istruttore.html', messaggio=messaggio)

        nuovo_istruttore = {
            "username": username,
            "password": password,
            "email": email,
            "titolo": titolo,
            "eta": eta,
            "utenti": []
        }

        istruttori.append(nuovo_istruttore)
        save_data(ISTRUTTORI_FILE_PATH, istruttori)

        return redirect(url_for('indexS'))
    return render_template('registrazione_istruttore.html', messaggio='')


@app.route('/add_workout_divider/<username>', methods=['POST'])
def add_workout_divider(username):
    """Add a workout divider to the user's workout plan."""
    user = next((user for user in users if user["username"] == username), None)
    if user:
        workout_name = request.form['workout_name']
        divider = {
            "esercizio": "Workout Divider",
            "ripetizioni": "",
            "serie": "",
            "pausa": "",
            "immagine": "",
            "workout_name": workout_name
        }
        user["schede"].append(divider)
        save_data(USER_FILE_PATH, users)
    return redirect(url_for('user_profile', username=username))

@app.route('/remove_workout_divider/<username>', methods=['POST'])
def remove_workout_divider(username):
    """Remove a workout divider from the user's workout plan."""
    divider_name = request.form['divider_name']
    user = next((user for user in users if user["username"] == username), None)
    
    if user and "schede" in user:
        user["schede"] = [exercise for exercise in user["schede"] if not (exercise['esercizio'] == "Workout Divider" and exercise['workout_name'] == divider_name)]
        save_data(USER_FILE_PATH, users)
    
    return redirect(url_for('user_profile', username=username))

@app.route('/edit_workout_divider/<username>', methods=['POST'])
def edit_workout_divider(username):
    """Edit the name of a workout divider in the user's workout plan."""
    old_divider_name = request.form['old_divider_name']
    new_divider_name = request.form['new_divider_name']
    
    user = next((user for user in users if user["username"] == username), None)
    
    if user and "schede" in user:
        for exercise in user["schede"]:
            if exercise['esercizio'] == "Workout Divider" and exercise['workout_name'] == old_divider_name:
                exercise['workout_name'] = new_divider_name
                break
        save_data(USER_FILE_PATH, users)
    
    return redirect(url_for('user_profile', username=username))

if __name__ == '__main__':
    random_port = random.randint(1024, 49151)
    app.run(debug=True, port=random_port)
