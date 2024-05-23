from flask import Flask, render_template
import random
import json

app = Flask(__name__)
FILE_PATH = "publicita.json" 
pubblicita = []

try:
    with open(FILE_PATH, 'r') as file:
        pubblicita = json.load(file)
except FileNotFoundError:
    pass

@app.route('/')
def image_test():
    immagine1 = random.choice(pubblicita)
    immagine2 = random.choice(pubblicita)
    while immagine1 == immagine2:
        immagine2 = random.choice(pubblicita)
    return render_template('prove.html', left=immagine1, right=immagine2)

if __name__ == '__main__':
    app.run(debug=True)