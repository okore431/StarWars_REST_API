from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(40), unique=True, nullable=False)
    password = db.Column(db.String(40), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    favorites = db.relationship("Favorites", back_populates="user")


    def __repr__(self):
        return '<User %r>' % self.username

    def serialize(self):
        favorites = [favorite.serialize() for favorite in self.favorites]
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "favorites":favorites

            # do not serialize the password, it's a security breach
        }

class Favorites(db.Model):
    __tablename__ = 'favorites'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete="CASCADE"), nullable=False)
    planet_id = db.Column(db.Integer, db.ForeignKey('planet.id', ondelete="CASCADE"), nullable=True)
    character_id = db.Column(db.Integer, db.ForeignKey('characters.id', ondelete="CASCADE"), nullable=True)
    user = db.relationship('User', back_populates='favorites')
    planet = db.relationship('Planets', backref='planet', foreign_keys=[planet_id])
    characters = db.relationship('Characters', backref='characters', foreign_keys=[character_id])

    def __repr__(self):
        return '<Favorites %r>' % self.user_id

    def serialize(self):
        return {
            "id": self.id,
            "username": self.user.username,
            "planet_id": self.planet_id,
            'planet_name': self.planet.planet_name if self.planet else None,
            "character_id": self.character_id,
            'character_name': self.characters.character_name if self.characters else None
        }

class Planets(db.Model):
    __tablename__ = 'planet'
    id = db.Column(db.Integer, primary_key=True)
    planet_name = db.Column(db.String(250), unique = True, nullable=False)
    population = db.Column(db.Integer)
    gravity = db.Column(db.String(40))
    climate = db.Column(db.String(50))
    terrain = db.Column(db.String(50))
    orbital_period = db.Column(db.Integer)
    rotation_period =db.Column(db.Integer)
    favorites = db.relationship('Favorites', back_populates='planet')

    def __repr__(self):
        return '<Planets %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "planet_name": self.planet_name,
            "population": self.population,
            "gravity": self.gravity,
            "climate": self.climate,
            "terrain": self.terrain,
            "orbital_period": self.orbital_period,
            "rotation_period": self.rotation_period,
        }

class Characters(db.Model):
    __tablename__ = 'characters'
    id = db.Column(db.Integer, primary_key=True)
    character_name = db.Column(db.String(250), unique = True, nullable=False)
    height = db.Column(db.Integer)
    weight = db.Column(db.Integer)
    eye_color = db.Column(db.String(10))
    favorites = db.relationship("Favorites", back_populates="characters")

    def __repr__(self):
        return '<Characters %r>' % self.character_name

    def serialize(self):
        return {
            "id": self.id,
            "character_name": self.character_name,
            "height": self.height,
            "weight": self.weight,
            "eye_color": self.eye_color,
        }
