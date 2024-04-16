from flask import Flask, render_template, request

app = Flask(__name__)
testi_aggiunti = []
@app.route('/')
def index():
    return render_template('index.html', testi_aggiunti=testi_aggiunti)

@app.route('/aggiungi_testo', methods=['POST'])
def aggiungi_testo():
    # testo = request.form['nuovo_testo']
    testo = "ciao"
    testi_aggiunti.append(testo)
    return render_template('index.html', testi_aggiunti=testi_aggiunti)


@app.route('/processa_scelta', methods=['POST'])
def processa_scelta():
    scelta = request.form['scelta']
    if scelta == 'Serie':
        messaggio = "Serie."
    elif scelta == 'Durata':
        messaggio = "Durata"
    elif scelta == 'opzione3':
        opzione_personalizzata = request.form['personalizzata']
        messaggio = opzione_personalizzata

    else:
        messaggio = "Scelta non valida."
    return messaggio

if __name__ == '__main__':
    app.run(debug=True)