from flask import Flask, request, jsonify, render_template
from transformers import pipeline, AutoModelForCausalLM, AutoTokenizer
from werkzeug.utils import secure_filename  # Importa secure_filename da Werkzeug
from PIL import Image
import os

app = Flask(__name__)

model = AutoModelForCausalLM.from_pretrained("distilgpt2")
tokenizer = AutoTokenizer.from_pretrained("distilgpt2")
text_generator = pipeline('text-generation', model=model, tokenizer=tokenizer)

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/', methods=['GET', 'POST'])
def chatbot():
    if request.method == 'POST':
        user_input = request.form['user_input']
        prompt = user_input
        output = text_generator(prompt, max_length=50, do_sample=True, top_k=50, top_p=0.95, num_return_sequences=1)
        return jsonify({"response": output[0]['generated_text']})
    return render_template('index.html')

@app.route('/create_meme', methods=['GET', 'POST'])
def create_meme():
    if request.method == 'POST':
        text = request.form['text']
        image = request.files['image']
        filename = secure_filename(image.filename)
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        image.save(image_path)

        # Qui aggiungi la tua logica per la creazione del meme, combinando l'immagine caricata e il testo

        return render_template('meme.html', image_path=image_path, text=text)

    return render_template('create_meme.html')

if __name__ == '__main__':
    app.run(debug=True, port=4674)
