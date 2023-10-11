#!/usr/bin/env python3
from flask import Flask
from flask import Flask, make_response, jsonify, request
from flask_migrate import Migrate
from flask_restful import Api, Resource

from models import db, Hero, Power, HeroPower

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)

db.init_app(app)
api = Api(app)

class Heroes(Resource):
    def get(self):
        heroes = Hero.query.all()

        heroes_data = []
        for hero in heroes:
            hero_data = {
                'id': hero.id,
                'name': hero.name,
                'super_name': hero.super_name
            }
            heroes_data.append(hero_data)

        return heroes_data, 200


api.add_resource(Heroes, '/heroes')


class HeroesByID(Resource):
    

    def get(self, num):
       
        hero = Hero.query.filter(Hero.id == num).first()

        if hero:
            hero_body = {
                "id": hero.id,
                "name": hero.name,
                "super_name": hero.super_name,
                "powers": [
                    {
                        "id": hero_power.power.id,
                        "name": hero_power.power.name,
                        "description": hero_power.power.description
                    }
                    for hero_power in hero.hero_powers
                ]
            }

            return hero_body

        return {
            "error": "Hero not found"
        }, 404


api.add_resource(HeroesByID, '/heroes/<int:num>')


class Powers(Resource):
  
    def get(self):
        
        powers = Power.query.all()

        powers_data = []
        for power in powers:
            power_data = {
                "id": power.id,
                "name": power.name,
                "description": power.description
            }
            powers_data.append(power_data)

        return powers_data, 200


api.add_resource(Powers, '/powers')


class PowersByID(Resource):
   
    def get(self, num):
       
        power = Power.query.filter(Power.id == num).first()

        if power:
            power_body = {
                "id": power.id,
                "name": power.name,
                "description": power.description
            }

            return power_body, 200

        return {
            "error": "Power not found"
        }, 404

    def patch(self, num):
        
        power = Power.query.filter(Power.id == num).first()

        data = request.get_json()

        if power:
            for attr in data:
                setattr(power, attr, data[attr])

            db.session.add(power)
            db.session.commit()

            response_body = {
                "id": power.id,
                "name": power.name,
                "description": power.description
            }

            return response_body, 201

        return {
            "error": "Power not found"
        }, 400


api.add_resource(PowersByID, '/powers/<int:num>')


class HeroPowers(Resource):
   

    def post(self):
        
        data = request.get_json()

        hero = Hero.query.filter(Hero.id == data['hero_id']).first()
        power = Power.query.filter(Power.id == data['power_id']).first()

        if not hero or not power:
            return {
                "errors": ["Hero or Power doesn't exist"]
            }, 404

        new_hero_power = HeroPower(
            strength=data['strength'],
            power_id=data['power_id'],
            hero_id=data['hero_id']
        )

        db.session.add(new_hero_power)
        db.session.commit()

        hero_data = HeroesByID().get(hero.id)

        return hero_data, 201


api.add_resource(HeroPowers, '/hero_powers')


if __name__ == "__main__":
    app.run(port=8000, debug=True)