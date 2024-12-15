from flask import Flask, request, render_template
import os

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    message = ""
    directory = "."  # Bieżący katalog
    files = os.listdir(directory)  # Pobranie listy plików w katalogu

    if request.method == 'POST':
        word = request.form.get('text_input', '')  # Pobierz dane z formularza
        message = f"You entered: {word}"  # Komunikat z wprowadzonym słowem

    return render_template('index.html', message=message, files=files)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
