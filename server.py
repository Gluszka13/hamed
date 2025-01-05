from flask import Flask, request, render_template, flash, redirect, url_for
import subprocess

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Wymagane dla funkcji flash

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/tool1", methods=['GET', 'POST'])
def tool1():
    message = ""   # Komunikat po wpisaniu frazy
    results = ""   # Wyniki narzędzia OSINT
    
    if request.method == 'POST':
        # Pobranie frazy z formularza
        search_phrase = request.form.get('text_input', '')
        
        if search_phrase:
            message = f"You searched for: {search_phrase}"
            try:
                # Podaj prawidłową ścieżkę do Twojego narzędzia OSINT
                command = f"python3 Digital-Footprint-OSINT-Tool/digital_footprint.py '{search_phrase}'"
                process = subprocess.run(command, shell=True, capture_output=True, text=True)
                
                # Pobieranie wyników z procesu
                if process.returncode == 0:
                    results = process.stdout
                else:
                    results = f"Error: {process.stderr}"
            except Exception as e:
                results = f"An error occurred: {str(e)}"
        else:
            message = "Please enter a search phrase."

    return render_template("tool1.html", message=message, results=results)

# Podstrona Tool 2 z obsługą flash
@app.route("/tool2", methods=['GET', 'POST'])
def tool2():
    if request.method == 'POST':
        # Wyświetlenie komunikatu „Please, first pay”
        flash("Please, first pay", "info")
        return redirect(url_for('tool2'))  # Odświeżenie strony

    return render_template("tool2.html")

# Podstrona Tool 3
@app.route("/tool3")
def tool3():
    return render_template("tool3.html")


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
