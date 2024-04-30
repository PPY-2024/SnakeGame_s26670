from SnakeGame import gameLogic


def test_collision_with_boundary():
    game = gameLogic.GameLogic()
    game.snake.coordinates[0] = (gameLogic.FIELD_SIZE, gameLogic.FIELD_SIZE)  # assigning out of bound coords to head
    assert game.check_boundary_collision() == True


def test_collision_with_snake_body():
    game = gameLogic.GameLogic()
    game.snake.coordinates = [(1, 1), (1, 2), (2, 2), (2, 1), (1, 1)]  # loop
    assert game.check_body_collision() == True


def test_no_collision_with_boundary():
    game = gameLogic.GameLogic()  # test for default snake position
    assert game.check_boundary_collision() == False


def test_no_collision_with_snake_body():
    game = gameLogic.GameLogic()
    game.snake.coordinates = [(1, 1), (1, 2), (2, 2), (2, 1)]  # not finished loop from above
    assert game.check_body_collision() == False
