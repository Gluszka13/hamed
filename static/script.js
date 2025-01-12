document.addEventListener('DOMContentLoaded', () => {
    const darkModeToggle = document.getElementById('dark-mode-toggle');

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
});
