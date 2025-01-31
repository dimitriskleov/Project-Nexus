from flask import Flask, jsonify
import random

app = Flask(__name__)

@app.route('/roll_dice', methods=['GET'])
def roll_dice():
    # Simulate a dice roll (e.g., a 6-sided dice)
    dice_roll = random.randint(1, 6)
    
    # Return the result in a JSON response
    return jsonify({
        'roll': dice_roll
    })

if __name__ == '__main__':
    app.run(debug=True)
