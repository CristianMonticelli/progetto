from flask import Flask, render_template, request
import json
app = Flask(__name__)
@app.route('/', methods=['GET', 'POST'])
def form_example():
    if request.method == 'POST':
        # this is a POST request
        # we'll access the data from the form using request.form
        name = request.form.get('name')
        age = request.form.get('age')
        
        # salvare la nuova scheda nel file json

        # leggo dal file json la lista delle schede
        
        with open("schede.json", "r") as file_json:
            try:        
                mylist = json.load(file_json)    
            except:        
                mylist = []
        return render_template('form.html',name=mylist)

        # return 'You posted: Name - ' + str(name) + ', Age - ' + str(age)
    else:
        # this is a GET request, show the form
        # leggo dal file json la lista delle schede
        return render_template('form.html',name=None,schede=schede)


if __name__ == '__main__':
    app.run(debug=True)