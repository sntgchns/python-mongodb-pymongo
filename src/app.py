from flask import Flask, request,jsonify, Response
from flask_pymongo import PyMongo, ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
from bson import json_util

app = Flask(__name__)

app.config['MONGO_URI'] = 'mongodb://localhost:27017/woonkly'
mongo = PyMongo(app)

@app.route('/users', methods=['POST'])
def create_user():
    username = request.json['username']
    password = request.json['password']
    email = request.json['email']

    if username and password and email:
        hashed_password = generate_password_hash(password)
        user = mongo.db.users
        id = user.insert_one({'username': username, 'password': hashed_password, 'email': email}).inserted_id
        response = {'_id': str(id), 'username': username, 'password': hashed_password, 'email': email}
        return response
    else:
        return not_found()
    # print(request.json)

@app.route('/users', methods=['GET'])
def get_users():
    users = mongo.db.users.find()
    response = json_util.dumps(users)
    return Response(response, mimetype='application/json')

@app.route('/users/<id>', methods=['GET'])
def get_user(id):
    user = mongo.db.users.find_one({'_id': ObjectId(id)})
    if user:
        response = json_util.dumps(user)
        return Response(response, mimetype='application/json')
    else:
        return not_found()

@app.route('/users/<id>', methods=['PUT'])
def update_user(id):
    user = mongo.db.users.find_one({'_id': ObjectId(id)})
    if user:
        username = request.json['username']
        password = request.json['password']
        email = request.json['email']
        hashed_password = generate_password_hash(password)
        mongo.db.users.update_one({'_id': ObjectId(id)}, {'$set': {'username': username, 'password': hashed_password, 'email': email}})
        response = jsonify({'message': 'User ' + id + ' updated successfully!'})
        # response = {'_id': str(id), 'username': username, 'password': hashed_password, 'email': email}
        return response, 201
    else:
        return not_found()

@app.route('/users/<id>', methods=['DELETE'])
def delete_user(id):
    user = mongo.db.users.find_one({'_id': ObjectId(id)})
    if user:
        mongo.db.users.delete_one({'_id': ObjectId(id)})
        response = jsonify({'message': 'Usuario' + id + 'eliminado'})
        return response, 204
    else:
        return not_found()

# @app.route('/users', methods=['GET'])
# def get_users():
#     users = mongo.db.users
#     output = []
#     for s in users.find():
#         output.append({'_id': str(s['_id']), 'username': s['username'], 'password': s['password'], 'email': s['email']})
#     return jsonify({'result': output})

@app.errorhandler(404)
def not_found(error=None):    
    return jsonify({'error': 'Not found: ' + request.url}), 404

if __name__ == '__main__':
    app.run(debug=True)