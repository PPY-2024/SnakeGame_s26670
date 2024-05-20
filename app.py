import json
from SnakeGame import gameLogic
from SnakeGame.packages import mongodb

from flask import Flask, render_template, jsonify, request, url_for, redirect

db = mongodb
db.initialize_database()

app = Flask(__name__, static_folder='static')
game_logic = gameLogic.GameLogic()


def read_game_init():
    with open('config/game-init.json', 'r') as file:
        data = json.load(file)
    return data


# Read game initialization data
game_init_data = read_game_init()
grid_size = game_init_data['grid_size']


@app.route('/')
def menu_redirect():
    return redirect(url_for('menu'))


@app.route('/menu')
def menu():
    return render_template('menu.html', scoreboard_url=url_for('scoreboard'), game_url=url_for('game'))


@app.route('/game', methods=['POST'])
def game():
    player_name = request.form['player_name']
    game_logic.name = player_name
    return render_template('game.html', gameOver_url=url_for('gameOver'))


@app.route('/gameOver')
def gameOver():
    db.store_game_result(game_logic.name, game_logic.score)
    db.update_database_file()
    game_score = game_logic.score
    game_logic.setup()
    return render_template('gameOver.html', player_name=game_logic.name, score=game_score,
                           menu_url=url_for('menu'))


@app.route('/scoreboard')
def scoreboard():
    scores = db.get_top_scores()
    scores_count = len(scores)
    return render_template('scoreboard.html', menu_url=url_for('menu'), scores=scores, scores_count=scores_count)


@app.route('/game/state', methods=['GET'])
def game_state():
    return jsonify({
        'active': game_logic.active,
        'score': game_logic.score,
        'snake': game_logic.snake.coordinates,
        'food': game_logic.food.coordinates
    })


@app.route('/game/move', methods=['POST', 'GET'])
def game_move():
    direction = request.json['direction']
    game_logic.snake.change_direction(gameLogic.DIRECTIONS[direction])
    game_logic.snake_move()
    return jsonify({'success': True, 'active': game_logic.active})


if __name__ == '__main__':
    app.run(debug=True)
