from flask import Flask, render_template, request, redirect, url_for


app = Flask(__name__)
messaggio = None
# Pagina iniziale con un bottone per reindirizzare
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        p11 = request.form['11']
        p12 = request.form['12']
        
        p21 = request.form['21']
        p22 = request.form['22']
        
        p31 = request.form['31']
        p32 = request.form['32']
        
        attrezzo = request.form['attrezzo']
        nota = request.form['nota']
        
        
        return render_template('primaria.html', p11=p11,p12=p12,p21=p21,p22=p22,
                               p31=p31,p32=p32,nota=nota,attrezzo=attrezzo)
    return render_template('primaria.html')

# Pagina di destinazione
@app.route('/secondaria')
def pagina_destinazione():
    return render_template('seconda.html')



if __name__ == '__main__':
    app.run(debug=True)