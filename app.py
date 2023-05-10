from flask import Flask, jsonify, request
from pymongo import MongoClient

app = Flask(__name__)
client = MongoClient('mongodb://root:password@localhost:27017/')
db = client['mydatabase']
collection = db['mycollection']


@app.route('/api/items', methods=['GET'])
def get_items():
    items = collection.find()
    output = []
    for item in items:
        output.append({
            'id': str(item['_id']),
            'name': item['name'],
            'description': item['description']
        })
    return jsonify(output)


@app.route('/api/items', methods=['POST'])
def add_item():
    data = request.get_json()
    name = data.get('name')
    description = data.get('description')

    if name and description:
        item = {
            'name': name,
            'description': description
        }
        item_id = collection.insert_one(item).inserted_id
        return jsonify({'id': str(item_id), 'message': 'Item added successfully.'}), 201
    else:
        return jsonify({'message': 'Invalid data provided.'}), 400


@app.route('/api/items/<item_id>', methods=['GET'])
def get_item(item_id):
    item = collection.find_one({'_id': ObjectId(item_id)})
    if item:
        output = {
            'id': str(item['_id']),
            'name': item['name'],
            'description': item['description']
        }
        return jsonify(output)
    else:
        return jsonify({'message': 'Item not found.'}), 404


@app.route('/api/items/<item_id>', methods=['PUT'])
def update_item(item_id):
    data = request.get_json()
    name = data.get('name')
    description = data.get('description')

    if name and description:
        updated_item = {
            'name': name,
            'description': description
        }
        result = collection.update_one({'_id': ObjectId(item_id)}, {'$set': updated_item})
        if result.modified_count > 0:
            return jsonify({'message': 'Item updated successfully.'})
        else:
            return jsonify({'message': 'Item not found.'}), 404
    else:
        return jsonify({'message': 'Invalid data provided.'}), 400


@app.route('/api/items/<item_id>', methods=['DELETE'])
def delete_item(item_id):
    result = collection.delete_one({'_id': ObjectId(item_id)})
    if result.deleted_count > 0:
        return jsonify({'message': 'Item deleted successfully.'})
    else:
        return jsonify({'message': 'Item not found.'}), 404


if __name__ == '__main__':
    app.run()
