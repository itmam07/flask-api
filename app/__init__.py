from flask import Flask, jsonify, request

app = Flask(__name__)

# Dummy-Daten
items = [
    {"id": 1, "name": "Item 1", "description": "This is item 1"},
    {"id": 2, "name": "Item 2", "description": "This is item 2"},
    {"id": 3, "name": "Item 3", "description": "This is item 3"}
]

# Route 1: Alle Items abrufen
@app.route('/items', methods=['GET'])
def get_items():
    return jsonify({"items": items})

# Route 2: Ein einzelnes Item abrufen
@app.route('/items/<int:item_id>', methods=['GET'])
def get_item(item_id):
    item = next((item for item in items if item["id"] == item_id), None)
    if item is None:
        return jsonify({"message": "Item not found"}), 404
    return jsonify(item)

# Route 3: Ein neues Item erstellen
@app.route('/items', methods=['POST'])
def create_item():
    new_item = request.get_json()
    if not new_item or "name" not in new_item or "description" not in new_item:
        return jsonify({"message": "Invalid data"}), 400
    item_id = max([item["id"] for item in items]) + 1
    new_item["id"] = item_id
    items.append(new_item)
    return jsonify(new_item), 201

# Route 4: Ein Item aktualisieren
@app.route('/items/<int:item_id>', methods=['PUT'])
def update_item(item_id):
    item = next((item for item in items if item["id"] == item_id), None)
    if item is None:
        return jsonify({"message": "Item not found"}), 404
    updated_item = request.get_json()
    item.update(updated_item)
    return jsonify(item)

# Route 5: Ein Item löschen
@app.route('/items/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    item = next((item for item in items if item["id"] == item_id), None)
    # if item is None:
    #    return jsonify({"message": "Item not found"}), 404
    items.remove(item)
    return jsonify({"message": "Item deleted successfully"}), 200

if __name__ == '__main__':
    app.run(debug=True)
