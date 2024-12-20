document.querySelector('form').addEventListener('submit', (e) => {
    const searchInput = document.querySelector('input[name="search"]');
    if (!searchInput.value.trim()) {
        alert('Veuillez saisir un mot-clé ou une date valide.');
        e.preventDefault(); // Empêche l'envoi du formulaire
    }
});
