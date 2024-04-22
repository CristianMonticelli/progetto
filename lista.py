from flask import Flask, render_template, request, redirect, url_for


app = Flask(__name__)
messaggio = None
lista_esercizii = []

# Pagina iniziale con un bottone per reindirizzare
@app.route('/', methods=['GET', 'POST'])
def index():
    
    

    if request.method == 'POST':
        lista_esercizii.append({
        'p11' : request.form['11'],
        'p12' : request.form['12'],
        'p21' : request.form['21'],
        'p22' : request.form['22'],
        'p31' : request.form['31'],
        'p32' : request.form['32'],
        'attrezzo' : request.form['attrezzo'],
        'nota' : request.form['nota']})
        
        
        return render_template('primaria.html', lista_esercizii=lista_esercizii)
    return render_template('primaria.html',lista_esercizii=lista_esercizii)

# Pagina di destinazione
@app.route('/secondaria')
def pagina_destinazione():
    lista_prefabbricati = None
    return render_template('seconda.html', lista_prefabbricati=lista_prefabbricati)

@app.route('/aggiungi_titoletto', methods=['POST'])
def aggiungi_titoletto():
    numero = 0
    lista_esercizii.append(numero+1)
    return render_template('primaria.html', lista_esercizii=lista_esercizii)

@app.route('/prefabbricato',methods=['POST'])
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