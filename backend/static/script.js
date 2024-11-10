const baseUrl = 'http://127.0.0.1:5000/cards';
const modal = document.getElementById('create-card-modal');
const openModalBtn = document.getElementById('open-modal-btn');
const closeModalBtn = document.getElementById('close-modal-btn');
const createCardForm = document.getElementById('create-card-form');
const imageInput = document.getElementById('image');
const imagePreview = document.getElementById('image-preview');

// Modal öffnen
openModalBtn.addEventListener('click', () => {
    modal.style.display = 'flex';
    document.body.classList.add('modal-active');
});

// Modal schließen
closeModalBtn.addEventListener('click', () => {
    modal.style.display = 'none';
    document.body.classList.remove('modal-active');
    imagePreview.innerHTML = ''; // Vorschau löschen, wenn das Modal geschlossen wird
});

// Modal schließen, wenn außerhalb geklickt wird
window.addEventListener('click', (event) => {
    if (event.target === modal) {
        modal.style.display = 'none';
        document.body.classList.remove('modal-active');
        imagePreview.innerHTML = ''; // Vorschau löschen, wenn das Modal geschlossen wird
    }
});

// Event-Listener für die Bildvorschau
imageInput.addEventListener('change', (event) => {
    const file = event.target.files[0];
    if (file) {
        const reader = new FileReader();
        reader.onload = (e) => {
            imagePreview.innerHTML = `<img src="${e.target.result}" alt="Vorschau Bild">`;
        };
        reader.readAsDataURL(file);
    } else {
        imagePreview.innerHTML = ''; // Entfernt die Vorschau, wenn keine Datei ausgewählt ist
    }
});

// Karten abrufen und anzeigen
async function fetchCards() {
    const response = await fetch(baseUrl);
    const cards = await response.json();
    const cardsContainer = document.getElementById('cards-container');
    cardsContainer.innerHTML = '';  // Clear the container

    cards.forEach(card => {
        const cardDiv = document.createElement('div');
        cardDiv.className = 'card';
        cardDiv.innerHTML = `
            <div class="card-header">
                <span class="card-name">${card.name}</span>
                <span class="card-hp">HP: ${card.health_points}</span>
            </div>
            <div class="card-image">
                ${card.image_path ? `<img src="${card.image_path}" alt="${card.name} Bild">` : '<span>Kein Bild</span>'}
            </div>
            <div class="card-attributes">
                <span class="card-attack">Angriffsschaden: ${card.attack_damage}</span>
                <span class="card-energy">Energie-Typ: ${card.energy_type}</span>
            </div>
            <button onclick="deleteCard(${card.id})">Löschen</button>
        `;
        cardsContainer.appendChild(cardDiv);
    });
}

// Neue Karte erstellen
createCardForm.addEventListener('submit', async (event) => {
    event.preventDefault();

    const formData = new FormData();
    formData.append('name', document.getElementById('name').value);
    formData.append('health_points', document.getElementById('health_points').value);
    formData.append('attack_damage', document.getElementById('attack_damage').value);
    formData.append('energy_type', document.getElementById('energy_type').value);
    formData.append('image', document.getElementById('image').files[0]);

    await fetch(baseUrl, {
        method: 'POST',
        body: formData
    });

    fetchCards();
    createCardForm.reset();
    imagePreview.innerHTML = ''; // Vorschau löschen, wenn das Formular gesendet wird
    modal.style.display = 'none';
});

// Karte löschen
async function deleteCard(id) {
    await fetch(`${baseUrl}/${id}`, {
        method: 'DELETE'
    });
    fetchCards();
}

// Initiale Karten laden
fetchCards();