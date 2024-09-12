#!/usr/bin/env python3

from flask import Flask, request, make_response, jsonify
from flask_migrate import Migrate
from flask_restful import Api, Resource
from models import db, Hero, Power, HeroPower
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get(
    "DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)
api = Api(app)

class Home(Resource):
     def get(self):
          return '<h1>Code challenge</h1>'

class HeroesData(Resource):
     def get(self):
        heroes = Hero.query.all()
        return [hero.to_dict(rules={'-hero_powers': True}) for hero in heroes], 200

class IndividualHero(Resource):
     def get(self, id):
        hero = db.session.get(Hero, id)
        if hero is None:
            return {"error": "Hero not found"}, 404
        return hero.to_dict(), 200
          

class PowersData(Resource):
    def get(self):
        powers = Power.query.all()
        return [power.to_dict(rules={'-hero_powers': True}) for power in powers], 200

class PowerById(Resource):
    def get(self, id):
        power = db.session.get(Power, id)
        if power is None:
            return {"error": "Power not found"}, 404
        return power.to_dict(rules={'-hero_powers': True}), 200
    


api.add_resource(Home, '/')
api.add_resource(HeroesData, '/heroes')
api.add_resource(IndividualHero, '/heroes/<int:id>')
api.add_resource(PowersData, '/powers')
api.add_resource(PowerById, '/powers/<int:id>')



if __name__ == '__main__':
    app.run(port=5555, debug=True)
