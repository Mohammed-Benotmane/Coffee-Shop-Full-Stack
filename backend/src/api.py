import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
import sys
from flask_cors import CORS
from .database.models import db_drop_and_create_all, setup_db, Drink,db
from .auth.auth import AuthError, requires_auth

app = Flask(__name__)
setup_db(app)
CORS(app)

#db_drop_and_create_all()

## ROUTES
@app.route('/drinks',methods=['GET'])
def get_drinks():
    drinks = Drink.query.all()
    formatted_drink = [drk.short() for drk in drinks]
    return jsonify({
        'success':True,
        'drinks': formatted_drink
    })

@app.route('/drinks-detail',methods=['GET'])
@requires_auth('get:drinks-detail')
def get_drinks_details(token):
    drinks = Drink.query.all()
    formatted_drink = [drk.long() for drk in drinks]
    print(formatted_drink)
    return jsonify({
        'success':True,
        'drinks': formatted_drink
    })

@app.route('/drinks',methods=['POST'])
@requires_auth("post:drinks")
def post_drink(token):
    body = request.get_json()
    new_title = body.get("title",None)
    new_recipe = body.get("recipe",None)
    toz =  json.dumps(new_recipe)
    str_recipe = str(toz)
    try:
        drink = Drink(title = new_title,recipe= str_recipe)
        drink.insert()
    except:
        print(sys.exc_info())
        db.session.rollback()
        return unprocessable(422)
    return jsonify({
        'Success':True,
        'Drinks': drink.long()
    })

@app.route("/drinks/<drink_id>", methods=['PATCH'])
@requires_auth("patch:drinks")
def patch_drinks(token ,drink_id):
    body = request.get_json()
    drink = Drink.query.get(drink_id)
    if body.get("title"):
        drink.title = body.get("title")
    if body.get("recipe"):
        new_recipe = body.get("recipe")
        new_recipe =  json.dumps(new_recipe)
        str_recipe = str(new_recipe)
        drink.recipe = str_recipe
    drink.update()
    return jsonify({
        "success": True,
        "drinks": [drink.long()]
    })

@app.route("/drinks/<drink_id>", methods=['DELETE'])
@requires_auth("delete:drinks")
def delete_drinks(token, drink_id):
    drink = Drink.query.get(drink_id)
    if drink is None:
        abort(404)
    drink.delete()
    return jsonify({
        "success":True,
        "delete":drink_id
    })

## Error Handling
'''
Example error handling for unprocessable entity
'''
@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
                    "success": False, 
                    "error": 422,
                    "message": "unprocessable"
                    }), 422

@app.errorhandler(404)
def resource_not_found(error):
    return jsonify({
                    "success": False, 
                    "error": 404,
                    "message": "resource not found"
                    }), 404

@app.errorhandler(AuthError)
def auth_error(error):
    return jsonify({
                    "success": False, 
                    "error": 401,
                    "message": "Authorization header is expected."
                    }), 401