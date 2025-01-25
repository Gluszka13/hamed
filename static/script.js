document.addEventListener('DOMContentLoaded', () => {
    const darkModeToggle = document.getElementById('dark-mode-toggle');
    const form = document.getElementById('searchForm');
    const resultsList = document.getElementById('results');
    const resultsContainer = document.getElementById('results-container');

    // Ustawienie domyślnej ikony na podstawie stanu dark mode
    if (document.body.classList.contains('dark-mode')) {
        darkModeToggle.textContent = '☀️'; // Ikona słońca dla trybu ciemnego
    } else {
        darkModeToggle.textContent = '🌙'; // Ikona księżyca dla trybu jasnego
    }

    darkModeToggle.addEventListener('click', () => {
        // Przełączanie klasy dla dark mode
        const isDarkMode = document.body.classList.toggle('dark-mode');

        // Zmiana ikony na podstawie aktualnego stanu dark mode
        darkModeToggle.textContent = isDarkMode ? '☀️' : '🌙';
    });

    // Obsługa formularza wyszukiwania
    resultsContainer.style.display = 'none'; // Ukryj sekcję wyników na start

    form.addEventListener('submit', async (event) => {
        event.preventDefault(); // Zapobiega przeładowaniu strony
        resultsList.innerHTML = ''; // Czyści poprzednie wyniki

        const query = document.getElementById('query').value.trim();

        if (!query) {
            alert('Wpisz coś w pole wyszukiwania!');
            return;
        }

        try {
            // Wysyłanie zapytania do backendu na porcie 8000
            const response = await fetch(`http://127.0.0.1:8000/search?query=${encodeURIComponent(query)}`);
            if (!response.ok) {
                throw new Error('Błąd podczas pobierania danych');
            }

            const results = await response.json();

            // Wyświetlanie wyników
            if (results.length === 0) {
                resultsList.innerHTML = '<li>Brak wyników.</li>';
            } else {
                results.forEach(result => {
                    const li = document.createElement('li');
                    li.innerHTML = `<a href="${result.link}" target="_blank">${result.title}</a><br>${result.snippet}`;
                    resultsList.appendChild(li);
                });
            }

            resultsContainer.style.display = 'block'; // Pokaż sekcję wyników
        } catch (error) {
            console.error(error);
            resultsList.innerHTML = '<li>Wystąpił błąd. Spróbuj ponownie później.</li>';
            resultsContainer.style.display = 'block';
        }
    });
});
