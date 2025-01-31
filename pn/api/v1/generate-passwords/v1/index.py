from flask import Flask, request, jsonify
import random
import string

app = Flask(__name__)

def generate_random_password(length):
    # Define the characters to use in the password
    characters = string.ascii_letters + string.digits + string.punctuation
    # Randomly select characters from the pool
    password = ''.join(random.choice(characters) for _ in range(length))
    return password

@app.route('/generate-passwords', methods=['GET'])
def generate_passwords():
    # Get parameters from the query string
    try:
        length = int(request.args.get('length'))  # Length of each password
        num_passwords = int(request.args.get('num'))  # Number of passwords to generate
    except (TypeError, ValueError):
        return jsonify({'error': 'Invalid input! Please provide valid numbers for length and num.'}), 400
    
    if length <= 0 or num_passwords <= 0:
        return jsonify({'error': 'Length and num must be positive integers.'}), 400

    # Generate the specified number of passwords
    passwords = [generate_random_password(length) for _ in range(num_passwords)]

    return jsonify({'passwords': passwords})

if __name__ == '__main__':
    app.run(debug=True)
