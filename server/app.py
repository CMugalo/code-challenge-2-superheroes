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

@app.route('/')
def index():
    return '<h1>Code challenge</h1>'

@app.route('/heroes', methods=['GET'])
def get_heroes():
    heroes = Hero.query.all()
    return jsonify([hero.to_dict(rules={'-hero_powers': True}) for hero in heroes])

@app.route('/heroes/<int:id>', methods=['GET'])
def get_hero(id):
    hero = db.session.get(Hero, id)
    if hero is None:
            return {"error": "Hero not found"}, 404
    return jsonify(hero.to_dict())

@app.route('/powers', methods=['GET'])
def retrieve_powers():
     powers = Power.query.all()
     return jsonify([power.to_dict(rules={'-hero_powers': True}) for power in powers])



if __name__ == '__main__':
    app.run(port=5555, debug=True)
