from flask import Flask, request, jsonify

# Create the Flask application
app = Flask(__name__)

# GET endpoint
@app.route('/', methods=['GET'])
def home():
    return "Welcome to the Flask application!"

# POST endpoint
@app.route('/submit', methods=['POST'])
def submit():
    data = request.get_json()  # Parse JSON data from the request body
    if not data:
        return jsonify({"error": "No JSON data provided"}), 400

    # Respond with the received data
    return jsonify({"message": "Data received successfully!", "data": data})

# Run the application
if __name__ == '__main__':
    app.run(debug=True)
