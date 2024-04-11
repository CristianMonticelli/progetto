from flask import Flask, render_template, request

app = Flask(__name__)

# Lista per memorizzare le stringhe aggiunte
testi_aggiunti = []

@app.route('/')
def index():
    return render_template('index.html', testi_aggiunti=testi_aggiunti)

@app.route('/aggiungi_esercizio', methods=['POST'])
def aggiungi_testo():
    testo = request.form['nuovo_testo']
    testi_aggiunti.append(testo)
    return render_template('index.html', testi_aggiunti=testi_aggiunti)

if __name__ == '__main__':
    app.run(debug=True)