from flask import Flask, request, render_template, send_file
from flask_cors import CORS
import requests
import subprocess, os
from dotenv import load_dotenv

# Załaduj zmienne środowiskowe z pliku .env
load_dotenv()

# Pobierz dane z pliku .env
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
GOOGLE_SEARCH_ENGINE_ID = os.getenv("GOOGLE_SEARCH_ENGINE_ID")
# print("GOOGLE_API_KEY:", GOOGLE_API_KEY)
# print("GOOGLE_SEARCH_ENGINE_ID:", GOOGLE_SEARCH_ENGINE_ID)


app = Flask(__name__)
CORS(app)
app.secret_key = 'fdfdsfs'  # Wymagane dla funkcji flash

@app.route("/")
def home():
    return render_template("index.html")

# Podstrona Tool 2 z obsługą flash
@app.route("/tool1", methods=['GET', 'POST'])
def tool1():
    message = ""   # Komunikat po wpisaniu frazy
    results = ""   # Wyniki narzędzia OSINT
    report_file = ""  # Ścieżka do pliku HTML z raportem

    # Ustaw bazowy folder projektu względem lokalizacji server.py
    base_dir = os.path.dirname(os.path.abspath(__file__))

    if request.method == 'POST':
        # Pobranie frazy z formularza
        search_phrase = request.form.get('text_input', '')

        if search_phrase:
            message = f"You searched for: {search_phrase}"
            try:
                # Ścieżka do pliku raportu w folderze `hamed`
                report_file = os.path.join(base_dir, f"whatsmyname_report_{search_phrase}.html")
                
                # Komenda uruchamiająca skrypt WhatsMyName
                command = f"python3 WhatsMyName-Python/whatsmyname.py -u '{search_phrase}'"
                process = subprocess.run(command, shell=True, capture_output=True, text=True)
                
                # Pobieranie wyników z procesu
                if process.returncode == 0:
                    if os.path.exists(report_file):
                        return send_file(report_file)  # Zwraca wygenerowany raport jako stronę HTML
                    else:
                        results = "Report file not found, but command executed successfully."
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
    message = ""
    results = []

    if request.method == 'POST':
        # Pobierz słowo kluczowe z formularza
        query_word = request.form.get('text_input', '')
        if not query_word:
            message = "Please enter a search phrase."
        else:
            # Tworzenie zapytania z "intext:<slowo>"
            search_query = f"intext:{query_word}"

            # URL Google Search API
            url = "https://www.googleapis.com/customsearch/v1"

            # Parametry zapytania
            params = {
                "key": GOOGLE_API_KEY,
                "cx": GOOGLE_SEARCH_ENGINE_ID,
                "q": search_query,
                "num": 10  # Liczba wyników do zwrócenia
            }

            try:
                # Wykonaj żądanie HTTP
                response = requests.get(url, params=params)
                if response.status_code != 200:
                    message = "Failed to fetch data from Google API."
                else:
                    data = response.json()
                    for item in data.get("items", []):
                        results.append({
                            "title": item.get("title"),
                            "link": item.get("link"),
                            "snippet": item.get("snippet")
                        })
                    message = f"Results for: {query_word}"
            except Exception as e:
                message = f"An error occurred: {str(e)}"

    return render_template("tool2.html", message=message, results=results)

# Podstrona Tool 3
@app.route("/tool3")
def tool3():
    return render_template("tool3.html")


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)