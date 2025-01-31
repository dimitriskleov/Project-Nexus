from flask import Flask, jsonify
import random

app = Flask(__name__)

@app.route('/random_number', methods=['GET'])
def random_number():
    # Generate a random number between 1 and 100
    random_num = random.randint(1, 100)
    return jsonify({'random_number': random_num})

if __name__ == '__main__':
    app.run(debug=True)
