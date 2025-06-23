from flask import Flask, render_template, jsonify, request
from flask import send_from_directory
from flask_cors import CORS

app = Flask(__name__, template_folder="../templates", static_folder="../static")
CORS(app)

# Global game state
game_state = {
    'board': ["" for _ in range(9)],
    'current_player': 'X',
    'winner': None
}

def check_winner(board):
    win_positions = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],
        [0, 3, 6], [1, 4, 7], [2, 5, 8],
        [0, 4, 8], [2, 4, 6]
    ]
    for pos in win_positions:
        if board[pos[0]] == board[pos[1]] == board[pos[2]] != "":
            return board[pos[0]]
    return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/move', methods=['POST'])
def move():
    data = request.get_json()
    index = data.get('index')
    if game_state['board'][index] == "" and game_state['winner'] is None:
        game_state['board'][index] = game_state['current_player']
        game_state['winner'] = check_winner(game_state['board'])
        if not game_state['winner']:
            game_state['current_player'] = 'O' if game_state['current_player'] == 'X' else 'X'
    return jsonify(game_state)

@app.route('/reset', methods=['POST'])
def reset():
    game_state['board'] = ["" for _ in range(9)]
    game_state['current_player'] = 'X'
    game_state['winner'] = None
    return jsonify(game_state)

# Export the app for Vercel
app = app
