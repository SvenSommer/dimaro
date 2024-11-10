import os
import random
from flask import Flask, request, jsonify, send_from_directory
from flask_restful import Api, Resource
from werkzeug.utils import secure_filename
from db_setup import db, create_app
from models import Card

# Erstelle das Flask-App-Objekt und API mit statischem Pfad
app = Flask(__name__, static_folder='static', static_url_path='/static')
app = create_app()
api = Api(app)

# Bild-Upload-Konfiguration
UPLOAD_FOLDER = 'images'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Liste von deutschen Namen und Energie-Typen
names = ["Feuerdrache", "Wasserbestie", "Donnerwolf", "Erdgolem", "Windfalke", "Schattenkatze", "Flammentiger", "Frostgigant", "Elektrofuchs", "Mystikschlange"]
energy_types = ["Feuer", "Wasser", "Blitz", "Erde", "Luft", "Schatten", "Licht", "Eis", "Gift", "Magie"]

# Mock-Funktion zum Erstellen von 10 zufälligen Karten
def create_mock_cards():
    for _ in range(10):
        card = Card(
            name=random.choice(names),
            health_points=random.randint(50, 150),
            attack_damage=random.randint(10, 50),
            energy_type=random.choice(energy_types),
            image_path=None  # Optional: Du kannst hier ein Bild hinzufügen oder es leer lassen
        )
        db.session.add(card)
    db.session.commit()
    print("10 zufällige Karten wurden erstellt.")

# Stelle sicher, dass die Funktion nur im App-Kontext ausgeführt wird
with app.app_context():
    db.create_all()  # Erstelle die Tabellen, falls sie noch nicht existieren
    #create_mock_cards()

# Route für das Abrufen hochgeladener Bilder
@app.route('/images/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

class CardListResource(Resource):
    def get(self):
        cards = Card.query.all()
        return jsonify([card.to_dict() for card in cards])

    def post(self):
        data = request.form
        image = request.files.get('image')

        if image:
            filename = secure_filename(image.filename)
            image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            image_path = f'/images/{filename}'
        else:
            image_path = None

        new_card = Card(
            name=data.get('name'),
            health_points=int(data.get('health_points')),
            attack_damage=int(data.get('attack_damage')),
            energy_type=data.get('energy_type'),
            image_path=image_path
        )
        db.session.add(new_card)
        db.session.commit()

        return new_card.to_dict(), 201

class CardResource(Resource):
    def get(self, card_id):
        card = Card.query.get_or_404(card_id)
        return jsonify(card.to_dict())

    def put(self, card_id):
        data = request.form
        card = Card.query.get_or_404(card_id)

        card.name = data.get('name', card.name)
        card.health_points = int(data.get('health_points', card.health_points))
        card.attack_damage = int(data.get('attack_damage', card.attack_damage))
        card.energy_type = data.get('energy_type', card.energy_type)

        image = request.files.get('image')
        if image:
            if card.image_path:
                os.remove(card.image_path)
            filename = secure_filename(image.filename)
            image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            card.image_path = f'/images/{filename}'  # Korrigierter Pfad für das Bild

        db.session.commit()
        return jsonify(card.to_dict())

    def delete(self, card_id):
        card = Card.query.get_or_404(card_id)
        if card.image_path:
            os.remove(os.path.join(app.config['UPLOAD_FOLDER'], os.path.basename(card.image_path)))
        db.session.delete(card)
        db.session.commit()
        return '', 204

api.add_resource(CardListResource, '/cards')
api.add_resource(CardResource, '/cards/<int:card_id>')

if __name__ == '__main__':
    app.run(debug=True)