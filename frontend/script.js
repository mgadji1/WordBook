const API_URL = "http://localhost:8080/api/words";

const wordsList = document.getElementById("words-list");
const addWordForm = document.getElementById("add-word-form");
const searchInput = document.getElementById("search-input");
const searchButton = document.getElementById("search-button");
const showAllButton = document.getElementById("show-all-button");
const message = document.getElementById("message");


async function loadWords() {
    const response = await fetch(API_URL);

    if (!response.ok) {
        throw new Error("Failed to load words");
    }

    const words = await response.json();

    renderWords(words);
}


function renderWords(words) {
    wordsList.innerHTML = "";

    if (words.length === 0) {
        wordsList.innerHTML = "<p>No words found.</p>";
        return;
    }

    words.forEach(word => {
        const card = document.createElement("div");
        card.className = "word-card";

        card.innerHTML = `
            <div class="word-info">
                <span class="word">${word.word}</span>
                <span>—</span>
                <span class="translation">${word.translation}</span>
            </div>

            <div class="actions">
                <button class="edit-button"
                        onclick="editWord('${word.word}', '${word.translation}')">
                    Edit
                </button>

                <button class="delete-button"
                        onclick="deleteWord('${word.word}')">
                    Delete
                </button>
            </div>
        `;

        wordsList.appendChild(card);
    });
}


addWordForm.addEventListener("submit", async (event) => {
    event.preventDefault();

    const word = document.getElementById("word-input").value;
    const translation = document.getElementById("translation-input").value;

    const response = await fetch(API_URL, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            word: word,
            translation: translation
        })
    });

    if (response.ok) {
        addWordForm.reset();
        message.textContent = "Word added successfully.";
        await loadWords();
    } else {
        const data = await response.json();
        message.textContent = data.detail || "Failed to add word.";
    }
});


async function deleteWord(word) {
    const response = await fetch(
        `${API_URL}/${encodeURIComponent(word)}`,
        {
            method: "DELETE"
        }
    );

    if (response.ok) {
        message.textContent = "Word deleted.";
        await loadWords();
    } else {
        message.textContent = "Failed to delete word.";
    }
}


async function editWord(word, currentTranslation) {
    const newTranslation = prompt(
        `New translation for "${word}":`,
        currentTranslation
    );

    if (newTranslation === null || newTranslation.trim() === "") {
        return;
    }

    const response = await fetch(
        `${API_URL}/${encodeURIComponent(word)}`,
        {
            method: "PUT",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                translation: newTranslation
            })
        }
    );

    if (response.ok) {
        message.textContent = "Translation updated.";
        await loadWords();
    } else {
        message.textContent = "Failed to update translation.";
    }
}


searchButton.addEventListener("click", async () => {
    const word = searchInput.value.trim();

    if (!word) {
        return;
    }

    const response = await fetch(
        `${API_URL}/${encodeURIComponent(word)}`
    );

    if (response.ok) {
        const result = await response.json();
        renderWords([result]);
        message.textContent = "";
    } else {
        renderWords([]);
        message.textContent = "Word not found.";
    }
});


showAllButton.addEventListener("click", async () => {
    searchInput.value = "";
    message.textContent = "";
    await loadWords();
});


loadWords();
