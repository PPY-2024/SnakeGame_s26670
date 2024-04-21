import pygame
import sys
import gameLogic


class GameInterface:
    def __init__(self, game):
        self.game = game

    def update(self):
        self.game.snake_move()
        if not self.game.active:
            pygame.quit()
            sys.exit()

    def draw(self):
        apple_rect = pygame.Rect(
            int(self.game.food.coordinates[0] * cell_size),
            int(self.game.food.coordinates[1] * cell_size),
            cell_size,
            cell_size)
        pygame.draw.rect(screen, 'red', apple_rect)

        for part in self.game.snake.coordinates:
            part_rect = pygame.Rect(
                int(part[0] * cell_size),
                int(part[1] * cell_size),
                cell_size,
                cell_size)
            pygame.draw.rect(screen, 'green', part_rect)

        score_surface = game_font.render(str(self.game.score), True, (255, 255, 255))
        score_x = int(cell_size * cell_number - 20)
        score_y = int(cell_size * cell_number - 10)
        score_rect = score_surface.get_rect(center=(score_x, score_y))
        screen.blit(score_surface, score_rect)


pygame.init()
gameLogic = gameLogic.GameLogic()
gameInterface = GameInterface(gameLogic)

tick = 1000
framerate = 60
cell_size = 50
cell_number = gameLogic.size

screen = pygame.display.set_mode((cell_number * cell_size, cell_number * cell_size))
clock = pygame.time.Clock()

game_font = pygame.font.Font(None, 36)

SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE, tick)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == SCREEN_UPDATE:
            gameInterface.update()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                gameLogic.snake.change_direction((0, -1))
            if event.key == pygame.K_RIGHT:
                gameLogic.snake.change_direction((1, 0))
            if event.key == pygame.K_DOWN:
                gameLogic.snake.change_direction((0, 1))
            if event.key == pygame.K_LEFT:
                gameLogic.snake.change_direction((-1, 0))

    screen.fill((200, 200, 70))
    gameInterface.draw()
    pygame.display.update()
    clock.tick(framerate)
