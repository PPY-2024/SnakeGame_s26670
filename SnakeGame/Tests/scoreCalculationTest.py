import pytest
from SnakeGame.SourceCode import gameLogic


def test_initial_score():
    game = gameLogic.Game()
    assert game.score == 0


def test_score_increment_on_food_eaten():
    game = gameLogic.Game()
    initial_score = game.score

    game.snake.coordinates = [(0, 0)]
    game.snake.direction = gameLogic.DIRECTIONS['down']
    game.food.coordinates = (0, 1)
    game.snake_move()

    assert game.score == initial_score + 1


def test_score_not_incremented_on_move():
    game = gameLogic.Game()
    initial_score = game.score

    game.snake.coordinates = [(0, 0)]
    game.snake.direction = gameLogic.DIRECTIONS['down']
    game.food.coordinates = (1, 1)
    game.snake_move()

    assert game.score == initial_score


def test_score_not_incremented_on_collision():
    game = gameLogic.Game()
    initial_score = game.score

    game.snake.coordinates = [(0, 0)]
    game.snake.direction = gameLogic.DIRECTIONS['left']
    game.food.coordinates = (1, 1)
    game.snake_move()

    assert game.score == initial_score
    assert game.check_collisions() == True
