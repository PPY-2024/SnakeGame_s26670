import json
from SnakeGame import gameLogic
from SnakeGame.packages.mongodb import initialize_database, store_game_result, dump_data_to_file, check_player_exists, get_top_scores, cleanup_database

from flask import Flask, render_template, jsonify, request, url_for

DIRECTIONS = {
    'up': (0, -1),
    'down': (0, 1),
    'left': (-1, 0),
    'right': (1, 0)
}

cleanup_database()
initialize_database()
app = Flask(__name__, static_folder='static')
gameLogic = gameLogic.GameLogic()


def read_game_init():
    with open('config/game-init.json', 'r') as file:
        data = json.load(file)
    return data


# Read game initialization data
game_init_data = read_game_init()

grid_size = game_init_data['grid_size']


@app.route('/menu')
def menu():
    return render_template('menu.html', scoreboard_url=url_for('scoreboard'), game_url=url_for('game'))


@app.route('/game', methods=['POST'])
def game():
    player_name = request.form['player_name']
    game.name = player_name
    return render_template('game.html', gameOver_url=url_for('gameOver'))


@app.route('/gameOver')
def gameOver():
    store_game_result(gameLogic.name, gameLogic.score)
    gameLogic.setup()
    return render_template('gameOver.html', player_name=gameLogic.name, score=gameLogic.score, menu_url=url_for('menu'))


@app.route('/scoreboard')
def scoreboard():
    scores = get_top_scores()
    return render_template('scoreboard.html', menu_url=url_for('menu'), scores=scores)


@app.route('/game/state', methods=['GET'])
def game_state():
    return jsonify({
        'active': gameLogic.active,
        'score': gameLogic.score,
        'snake': gameLogic.snake.coordinates,
        'food': gameLogic.food.coordinates
    })


@app.route('/game/move', methods=['POST', 'GET'])
def game_move():
    direction = request.json['direction']
    gameLogic.snake.change_direction(DIRECTIONS[direction])
    gameLogic.snake_move()
    return jsonify({'success': True, 'active': gameLogic.active})


if __name__ == '__main__':
    app.run(debug=True)
