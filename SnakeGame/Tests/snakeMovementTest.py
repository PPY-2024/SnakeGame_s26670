import pytest
from SnakeGame.SourceCode import gameLogic


def test_all_directions():
    for direction in gameLogic.DIRECTIONS:
        game = gameLogic.Game()
        tested_direction = gameLogic.DIRECTIONS[direction]

        test_pos = (gameLogic.FIELD_SIZE // 2, gameLogic.FIELD_SIZE // 2)
        expected_pos = (test_pos[0] + tested_direction[0], test_pos[1] + tested_direction[1])

        game.snake.coordinates = [test_pos]
        game.snake.direction = tested_direction

        game.snake_move()

        assert game.snake.coordinates[0] == expected_pos
