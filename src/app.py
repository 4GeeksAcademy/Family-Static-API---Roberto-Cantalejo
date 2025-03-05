"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# create the jackson family object
jackson_family = FamilyStructure("Jackson")

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/members', methods=['GET'])
def get_everyone():

    # this is how you can use the Family datastructure by calling its methods
    members = jackson_family.get_all_members()
    response_body = {
        "family": members
    }
    return jsonify(response_body), 200

@app.route('/member/<int:member_id>', methods=['GET'])
def get_memb(member_id):
    member = jackson_family.get_member(member_id)
    if member:
        response_body= {
            "id": member["id"],
            "first_name": member["first_name"],
            "age": member["age"],
            "lucky_numbers": member["lucky_numbers"]
        }
        return jsonify(response_body), 200
    else:
        return jsonify({"error": "Member not found"}), 404
    
@app.route('/member', methods=['POST'])
def add_memb():
    new_member = request.get_json() # Meto en una variable el json enviado, que si no tiene información devuelve un error 400 y si tiene lo añade a la familia
    if new_member is None:
        return jsonify({"error": "Invalid member"}), 400
    jackson_family.add_member(new_member)
    return jsonify({"message": "Member added successfully"}), 200

@app.route('/member/<int:member_id>', methods=['DELETE'])
def delete_memb(member_id):
        member = jackson_family.get_member(member_id)
        if member:
            jackson_family.delete_member(member_id)
            return jsonify({"message": "Member added successfully"}), 200
        return jsonify({"error": "Member not found"}), 404

    
# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
