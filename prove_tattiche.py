from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    elementi = [1, 2, 3]  # Esempio di una lista non vuota
    altra_condizione = False  # Esempio di un'altra condizione

    return render_template('prove1.html', elementi=elementi, altra_condizione=altra_condizione)

if __name__ == '__main__':
    app.run(debug=True)