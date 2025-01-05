document.addEventListener("DOMContentLoaded", () => {
    const toggleButton = document.getElementById("dark-mode-toggle");
    const body = document.body;

    // Sprawdź, czy w localStorage zapisany jest tryb ciemny
    const darkMode = localStorage.getItem("darkMode");
    if (darkMode === "enabled") {
        body.classList.add("dark-mode");
    }

    // Dodaj obsługę przycisku tylko, jeśli istnieje
    if (toggleButton) {
        toggleButton.addEventListener("click", () => {
            body.classList.toggle("dark-mode");

            // Zapisz preferencje użytkownika w localStorage
            if (body.classList.contains("dark-mode")) {
                localStorage.setItem("darkMode", "enabled");
            } else {
                localStorage.setItem("darkMode", "disabled");
            }
        });
    }
});
