from flask import Flask, request, jsonify

app = Flask(__name__)

countries = [
    {"id":'1', "name": "India", "capital":"Dehli"},
    {"id":'2', "name": "Bhutan", "capital":"Thimphu"},
    {"id":'3', "name": "Japan", "capital":"Tokyo"},
]


@app.route('/countries/', methods=["GET"])
def get_countries():
    return jsonify(countries)

@app.route('/countries/<id>', methods=["GET"])
def get_country(id):
    country = next(filter(lambda x: x['id'] == id, countries), None)
    if country is None:
        return jsonify({"error": "Country not found"}), 404
    return jsonify(country)

@app.route('/countries/', methods=["POST"])
def create_country():
    data = request.get_json()
    country_id = data["id"]
    if any(country for country in countries if country['id'] == country_id):
        return jsonify({"error": "Country already exists"}), 400
    countries.append(data)
    return jsonify(data), 201

@app.route('/countries/<id>', methods=["PUT"])
def update_country(id):
    global countries
    name = request.form.get("name")
    capital = request.form.get("capital")

    for n in countries:
        if n.get("id") == id:
            n['name'] = str(name)
            n['capital'] = str(capital)
        return jsonify(countries), 200


@app.route('/countries/<id>', methods=["PATCH"])
def update_country_partial(id):
    data = request.get_json()
    country = next(filter(lambda x: x['id'] == id, countries), None)
    if country is None:
        return jsonify({"error": "Country not found"}), 404
    country.update(data)
    return jsonify(country), 200

@app.route('/countries/<id>', methods=["DELETE"])
def delete_country(id):
    country = next(filter(lambda x: x['id'] == id, countries), None)
    if country is None:
        return jsonify({"error": "Country not found"}), 404
    countries.remove(country)
    return jsonify({"message": "Country deleted"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)