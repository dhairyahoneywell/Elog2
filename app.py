from flask import Flask, jsonify, request

app = Flask(__name__)

# Hard-coded JSON data
data = {"message": "Hello, World!", "status": "success"}


@app.route("/", methods=["GET", "POST"])
def hello_world():
    return "Hello,World!"


@app.route("/api/data", methods=["GET"])
def get_data():
    return jsonify(data)


@app.route("/api/data", methods=["POST"])
def post_data():
    new_data = request.get_json()
    return jsonify(new_data), 201


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5091, debug=True)
