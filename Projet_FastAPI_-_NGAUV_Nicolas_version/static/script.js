async function loadLanguages() {
    // Charger la liste des langues depuis le fichier JSON
    const response = await fetch("/static/lang_tags.json");
    const languages = await response.json();

    let sourceSelect = document.getElementById("source-lang");
    let targetSelect = document.getElementById("target-lang");

    // Ajouter les langues aux menus déroulants
    for (let lang in languages) {
        let option1 = new Option(lang, languages[lang]);
        let option2 = new Option(lang, languages[lang]);
        sourceSelect.add(option1);
        targetSelect.add(option2);
    }

    // Valeurs par défaut (ex : Français → Anglais)
    sourceSelect.value = "fr";
    targetSelect.value = "en";
}

async function translateText() {
    let inputText = document.getElementById("input-text").value;
    let sourceLang = document.getElementById("source-lang").value;
    let targetLang = document.getElementById("target-lang").value;

    if (!inputText.trim()) {
        alert("Veuillez entrer un texte !");
        return;
    }

    let response = await fetch("/translate", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            source: sourceLang,
            target: targetLang,
            text: inputText
        })
    });

    let data = await response.json();

    document.getElementById("translated-text").textContent = data.translation;
    document.getElementById("translation-score").textContent = `Score: ${data.score.toFixed(2)}`;
}

// Charger les langues au démarrage
document.addEventListener("DOMContentLoaded", loadLanguages);
