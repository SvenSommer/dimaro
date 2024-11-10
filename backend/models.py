from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Card(db.Model):
    __tablename__ = 'cards'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    health_points = db.Column(db.Integer, nullable=False)
    attack_damage = db.Column(db.Integer, nullable=False)
    energy_type = db.Column(db.String(20), nullable=False)
    image_path = db.Column(db.String(100), nullable=True)  # Pfad zum Bild

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'health_points': self.health_points,
            'attack_damage': self.attack_damage,
            'energy_type': self.energy_type,
            'image_path': self.image_path
        }