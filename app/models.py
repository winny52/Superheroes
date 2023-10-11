"""
This module defines SQLAlchemy models for the Heroes, Powers, and HeroPower relationships.
"""

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates

db = SQLAlchemy()


class Hero(db.Model):
    """
    Represents a Hero in the database.

    Attributes:
        id (int): The unique identifier for the hero.
        name (str): The name of the hero.
        super_name (str): The superhero name of the hero.
        created_at (datetime): The timestamp when the hero was created.
        updated_at (datetime): The timestamp when the hero was last updated.
        hero_powers (relationship): A relationship to the HeroPower model.
    """

    __tablename__ = 'heroes'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    super_name = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    hero_powers = db.relationship('HeroPower', back_populates='hero')


class Power(db.Model):
    """
    Represents a Power in the database.

    Attributes:
        id (int): The unique identifier for the power.
        name (str): The name of the power.
        description (str): The description of the power.
        created_at (datetime): The timestamp when the power was created.
        updated_at (datetime): The timestamp when the power was last updated.
        hero_powers (relationship): A relationship to the HeroPower model.
    """

    __tablename__ = 'powers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    description = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    hero_powers = db.relationship('HeroPower', back_populates='power')

    @validates('description')
    def description_validation(self, key, description):
        """
        Validates the description field of a Power.

        Args:
            key (str): The name of the field.
            description (str): The description to be validated.

        Returns:
            str: The validated description.

        Raises:
            ValueError: If the description is empty or less than 20 characters.
        """
        if not description:
            raise ValueError('Power must have a description')
        if len(description) < 20:
            raise ValueError('Description must be more than 20 characters')

        return description


class HeroPower(db.Model):
    """
    Represents the relationship between a Hero and a Power in the database.

    Attributes:
        id (int): The unique identifier for the HeroPower relationship.
        strength (str): The strength of the hero when using the power.
        hero_id (int): The foreign key referencing the Hero model.
        power_id (int): The foreign key referencing the Power model.
        created_at (datetime): The timestamp when the relationship was created.
        updated_at (datetime): The timestamp when the relationship was last updated.
        hero (relationship): A relationship to the Hero model.
        power (relationship): A relationship to the Power model.
    """

    __tablename__ = 'hero_powers'

    id = db.Column(db.Integer, primary_key=True)
    strength = db.Column(db.String)
    hero_id = db.Column(db.Integer, db.ForeignKey('heroes.id'))
    power_id = db.Column(db.Integer, db.ForeignKey('powers.id'))
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    hero = db.relationship('Hero', back_populates='hero_powers')
    power = db.relationship('Power', back_populates='hero_powers')

    @validates('strength')
    def strength_validation(self, key, strength):
        """
        Validates the strength field of a HeroPower.

        Args:
            key (str): The name of the field.
            strength (str): The strength to be validated.

        Returns:
            str: The validated strength.

        Raises:
            ValueError: If the strength is not one of 'Strong', 'Weak', or 'Average'.
        """
        if strength not in ['Strong', 'Weak', 'Average']:
            raise ValueError(
                "Strength must be either Strong, Weak, or Average")
        return strength