from flask import Flask, request, jsonify

app = Flask(__name__)

products = []

@app.route('/api/products', methods=['GET', 'POST'])
def manage_products():
    if request.method == 'GET':
        return jsonify(products)
    elif request.method == 'POST':
        data = request.get_json()
        products.append(data)
        return jsonify({'message': 'Product added successfully'}), 201

@app.route('/api/products/<int:index>', methods=['PUT', 'DELETE'])
def edit_or_delete_product(index):
    if request.method == 'PUT':
        data = request.get_json()
        products[index] = data
        return jsonify({'message': 'Product edited successfully'})
    elif request.method == 'DELETE':
        if index < len(products):
            del products[index]
            return jsonify({'message': 'Product deleted successfully'})
        else:
            return jsonify({'message': 'Product not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)
