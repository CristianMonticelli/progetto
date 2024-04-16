from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    # Esempio di una lista di elementi
    elementi = []
    return render_template('prove1.html', elementi=elementi)

if __name__ == '__main__':
    app.run(debug=True)