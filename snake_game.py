import pygame
import time
import random
import os

class SnakeGame:
    def __init__(self):
        pygame.init()

        self.snake_speed = 15
        self.window_x = 720
        self.window_y = 480

        self.display = pygame.display.set_mode((self.window_x, self.window_y))
        pygame.display.set_caption('Snake Game')

        self.clock = pygame.time.Clock()

        self.white = (255, 255, 255)
        self.black = (0, 0, 0)
        self.red = (255, 0, 0)
        self.green = (0, 255, 0)
        self.blue = (0, 0, 255)

        self.fps = pygame.time.Clock()

        self.snake_block = 20

        self.reset_game()
        self.high_score = self.load_high_score()

    def spawn_food(self):
        return [random.randrange(1, (self.window_x // self.snake_block)) * self.snake_block,
                random.randrange(1, (self.window_y // self.snake_block)) * self.snake_block]

    def load_high_score(self):
        if os.path.exists('highscore.txt'):
            with open('highscore.txt', 'r') as f:
                return int(f.read())
        return 0

    def save_high_score(self):
        with open('highscore.txt', 'w') as f:
            f.write(str(self.high_score))

    def show_score(self, choice, color, font, size):
        score_font = pygame.font.SysFont(font, size)
        score_surface = score_font.render('Score: ' + str(self.score), True, color)
        score_rect = score_surface.get_rect()
        self.display.blit(score_surface, score_rect)
        
        high_score_surface = score_font.render('High Score: ' + str(self.high_score), True, color)
        high_score_rect = high_score_surface.get_rect()
        high_score_rect.topright = (self.window_x - 10, 10)
        self.display.blit(high_score_surface, high_score_rect)

    def draw_snake(self):
        for i, pos in enumerate(self.snake_body):
            if i == 0:  # Snake's head
                pygame.draw.circle(self.display, self.green, (pos[0] + self.snake_block // 2, pos[1] + self.snake_block // 2), self.snake_block // 2)
                # Eyes
                eye_radius = self.snake_block // 8
                left_eye = (pos[0] + self.snake_block // 3, pos[1] + self.snake_block // 3)
                right_eye = (pos[0] + 2 * self.snake_block // 3, pos[1] + self.snake_block // 3)
                pygame.draw.circle(self.display, self.white, left_eye, eye_radius)
                pygame.draw.circle(self.display, self.white, right_eye, eye_radius)
                pygame.draw.circle(self.display, self.black, left_eye, eye_radius // 2)
                pygame.draw.circle(self.display, self.black, right_eye, eye_radius // 2)
            else:  # Snake's body
                pygame.draw.circle(self.display, self.green, (pos[0] + self.snake_block // 2, pos[1] + self.snake_block // 2), self.snake_block // 2 - 1)
        
        # Connect body segments with lines
        for i in range(1, len(self.snake_body)):
            prev = self.snake_body[i-1]
            current = self.snake_body[i]
            pygame.draw.line(self.display, self.green, 
                             (prev[0] + self.snake_block // 2, prev[1] + self.snake_block // 2),
                             (current[0] + self.snake_block // 2, current[1] + self.snake_block // 2),
                             self.snake_block - 2)

    def draw_food(self):
        pygame.draw.circle(self.display, self.red, (self.food_position[0] + self.snake_block // 2, self.food_position[1] + self.snake_block // 2), self.snake_block // 2)

    def draw_button(self, text, x, y, width, height, inactive_color, active_color):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        if x + width > mouse[0] > x and y + height > mouse[1] > y:
            pygame.draw.rect(self.display, active_color, (x, y, width, height))
            if click[0] == 1:
                return True
        else:
            pygame.draw.rect(self.display, inactive_color, (x, y, width, height))

        font = pygame.font.SysFont('times new roman', 20)
        text_surf = font.render(text, True, self.black)
        text_rect = text_surf.get_rect()
        text_rect.center = ((x + (width / 2)), (y + (height / 2)))
        self.display.blit(text_surf, text_rect)
        return False

    def game_over(self):
        if self.score > self.high_score:
            self.high_score = self.score
            self.save_high_score()

        self.display.fill(self.black)
        my_font = pygame.font.SysFont('times new roman', 70)
        game_over_surface = my_font.render('Your Score is: ' + str(self.score), True, self.red)
        game_over_rect = game_over_surface.get_rect()
        game_over_rect.midtop = (self.window_x/2, self.window_y/4)
        self.display.blit(game_over_surface, game_over_rect)
        
        retry_font = pygame.font.SysFont('times new roman', 50)
        retry_surface = retry_font.render('Press R to Retry or Q to Quit', True, self.white)
        retry_rect = retry_surface.get_rect()
        retry_rect.midtop = (self.window_x/2, self.window_y/2)
        self.display.blit(retry_surface, retry_rect)
        
        pygame.display.flip()
        
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        return True
                    if event.key == pygame.K_q:
                        pygame.quit()
                        quit()
        return False

    def settings_menu(self):
        self.display.fill(self.black)
        font = pygame.font.SysFont('times new roman', 50)
        title = font.render('Select Difficulty', True, self.white)
        easy = font.render('1. Easy', True, self.white)
        medium = font.render('2. Medium', True, self.white)
        hard = font.render('3. Hard', True, self.white)
        
        self.display.blit(title, (self.window_x/2 - title.get_width()/2, 50))
        self.display.blit(easy, (self.window_x/2 - easy.get_width()/2, 150))
        self.display.blit(medium, (self.window_x/2 - medium.get_width()/2, 250))
        self.display.blit(hard, (self.window_x/2 - hard.get_width()/2, 350))
        
        pygame.display.flip()
        
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_1:
                        self.snake_speed = 10
                        waiting = False
                    elif event.key == pygame.K_2:
                        self.snake_speed = 15
                        waiting = False
                    elif event.key == pygame.K_3:
                        self.snake_speed = 20
                        waiting = False

    def reset_game(self):
        self.snake_position = [100, 50]
        self.snake_body = [[100, 50], [90, 50], [80, 50]]
        self.food_position = self.spawn_food()
        self.food_spawn = True
        self.direction = 'RIGHT'
        self.change_to = self.direction
        self.score = 0

    def play_step(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP or event.key == ord('w'):
                    self.change_to = 'UP'
                if event.key == pygame.K_DOWN or event.key == ord('s'):
                    self.change_to = 'DOWN'
                if event.key == pygame.K_LEFT or event.key == ord('a'):
                    self.change_to = 'LEFT'
                if event.key == pygame.K_RIGHT or event.key == ord('d'):
                    self.change_to = 'RIGHT'

        if self.change_to == 'UP' and self.direction != 'DOWN':
            self.direction = 'UP'
        if self.change_to == 'DOWN' and self.direction != 'UP':
            self.direction = 'DOWN'
        if self.change_to == 'LEFT' and self.direction != 'RIGHT':
            self.direction = 'LEFT'
        if self.change_to == 'RIGHT' and self.direction != 'LEFT':
            self.direction = 'RIGHT'

        if self.direction == 'UP':
            self.snake_position[1] -= 10
        if self.direction == 'DOWN':
            self.snake_position[1] += 10
        if self.direction == 'LEFT':
            self.snake_position[0] -= 10
        if self.direction == 'RIGHT':
            self.snake_position[0] += 10

        self.snake_body.insert(0, list(self.snake_position))
        if self.snake_position[0] == self.food_position[0] and self.snake_position[1] == self.food_position[1]:
            self.score += 1
            self.food_spawn = False
        else:
            self.snake_body.pop()

        if not self.food_spawn:
            self.food_position = self.spawn_food()
        self.food_spawn = True

        self.display.fill(self.black)
        self.draw_snake()
        self.draw_food()

        if (self.snake_position[0] < 0 or self.snake_position[0] >= self.window_x or
            self.snake_position[1] < 0 or self.snake_position[1] >= self.window_y):
            return True, self.score

        for block in self.snake_body[1:]:
            if self.snake_position[0] == block[0] and self.snake_position[1] == block[1]:
                return True, self.score

        self.show_score(1, self.white, 'times new roman', 20)
        pygame.display.update()
        self.fps.tick(self.snake_speed)

        return False, self.score

    def run(self):
        self.settings_menu()
        game_over = False
        while not game_over:
            game_over, score = self.play_step()
        
        if self.game_over():
            self.reset_game()
            self.run()

if __name__ == "__main__":
    game = SnakeGame()
    game.run()