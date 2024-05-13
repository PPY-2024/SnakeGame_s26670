import random

FIELD_SIZE = 10

DIRECTIONS = {
    'up':   (0, -1),
    'down': (0, 1),
    'left': (-1, 0),
    'right': (1, 0)
}

SNAKE_DEFAULT_DIRECTION = DIRECTIONS['down']
SNAKE_DEFAULT_SIZE = 3


class GameLogic:
    def __init__(self):
        self.active = True
        self.size = FIELD_SIZE
        self.snake = Snake()
        self.food = Food()
        self.score = 0
        self.name = ""

    def setup(self):
        self.active = True
        self.size = FIELD_SIZE
        self.snake = Snake()
        self.food = Food()
        self.score = 0
        self.name = ""

    def check_collisions(self):
        return self.check_boundary_collision() or self.check_body_collision()

    def check_boundary_collision(self):
        x, y = self.snake.coordinates[0]

        if x < 0 or x >= FIELD_SIZE:
            return True
        elif y < 0 or y >= FIELD_SIZE:
            return True

        return False

    def check_body_collision(self):
        x, y = self.snake.coordinates[0]

        for snake_part in self.snake.coordinates[1:]:
            if x == snake_part[0] and y == snake_part[1]:
                return True

        return False

    def snake_move(self):
        x, y = self.snake.coordinates[0]

        x += self.snake.direction[0]
        y += self.snake.direction[1]

        self.snake.coordinates.insert(0, (x, y))

        if self.check_collisions():
            self.active = False
        else:
            if (self.snake.coordinates[0][0] == self.food.coordinates[0]
                    and self.snake.coordinates[0][1] == self.food.coordinates[1]):
                self.score += 1
                self.food.generate_coordinates(self.snake.coordinates)
            else:
                del self.snake.coordinates[-1]


class Snake:
    def __init__(self):
        self.body_size = SNAKE_DEFAULT_SIZE
        self.direction = SNAKE_DEFAULT_DIRECTION
        self.coordinates = []

        for i in range(0, SNAKE_DEFAULT_SIZE):
            self.coordinates.append((0, SNAKE_DEFAULT_SIZE - i - 1))

    def change_direction(self, direction):
        if direction == DIRECTIONS['left'] and self.direction == DIRECTIONS['right']:
            return
        if direction == DIRECTIONS['right'] and self.direction == DIRECTIONS['left']:
            return
        if direction == DIRECTIONS['up'] and self.direction == DIRECTIONS['down']:
            return
        if direction == DIRECTIONS['down'] and self.direction == DIRECTIONS['up']:
            return
        self.direction = direction


class Food:
    def __init__(self):
        self.coordinates = (FIELD_SIZE // 2, FIELD_SIZE // 2)

    def generate_coordinates(self, snake_coordinates):
        apple_generated_successfully = False
        while not apple_generated_successfully:
            self.coordinates = (random.randint(0, FIELD_SIZE - 1),
                                random.randint(0, FIELD_SIZE - 1))
            if self.coordinates not in snake_coordinates:
                apple_generated_successfully = True
