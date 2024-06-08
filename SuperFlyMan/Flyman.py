import pygame
import random
import time

pygame.init()

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (50, 50, 50)
gravity = 0.5
pipe_speed = 3
pipe_gap = 200

clock = pygame.time.Clock()
font = pygame.font.Font(None, 32)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Flappy Bird")

background = pygame.image.load('background.jpg').convert()
bird_img = pygame.image.load('bird.png').convert_alpha()
pipe_img = pygame.image.load('pipe.jpg').convert_alpha()
jump_sound = pygame.mixer.Sound('jump.wav')
game_over_sound = pygame.mixer.Sound('game_over.wav')

bird_img = pygame.transform.scale(bird_img, (30, 21))  # Mengubah ukuran gambar burung
pipe_img = pygame.transform.scale(pipe_img, (60, 400))  # Mengubah ukuran gambar pipa

play_button_img = pygame.image.load('play.png').convert_alpha()
restart_button_img = pygame.image.load('restart.png').convert_alpha()
exit_button_img = pygame.image.load('exit.png').convert_alpha()
game_over_img = pygame.image.load('gameover.png').convert_alpha()

# Mengubah ukuran gambar tombol
play_button_img = pygame.transform.scale(play_button_img, (280, 80))
restart_button_img = pygame.transform.scale(restart_button_img, (280, 80))
exit_button_img = pygame.transform.scale(exit_button_img, (280, 80))

def draw_background():
    screen.blit(background, (0, 0))

def draw_bird(bird_y):
    screen.blit(bird_img, (50, bird_y))

def draw_pipe(pipe_x, pipe_y):
    screen.blit(pipe_img, (pipe_x, pipe_y))
    screen.blit(pipe_img, (pipe_x, pipe_y + pipe_img.get_height() + pipe_gap))

def check_collision(pipe_x, pipe_y, bird_rect):
    pipe_top_rect = pygame.Rect(pipe_x, pipe_y, pipe_img.get_width(), pipe_img.get_height())
    pipe_bottom_rect = pygame.Rect(pipe_x, pipe_y + pipe_img.get_height() + pipe_gap, pipe_img.get_width(), pipe_img.get_height())
    if bird_rect.colliderect(pipe_top_rect) or bird_rect.colliderect(pipe_bottom_rect):
        return True
    if bird_rect.top <= 0 or bird_rect.bottom >= SCREEN_HEIGHT:
        return True
    return False

def display_score(score, highscore, level):
    shadow_offset = 2

    score_surface = font.render(f'Score: {score}', True, WHITE)
    highscore_surface = font.render(f'Highscore: {highscore}', True, WHITE)
    level_surface = font.render(f'Level: {level}', True, WHITE)

    score_shadow = font.render(f'Score: {score}', True, GRAY)
    highscore_shadow = font.render(f'Highscore: {highscore}', True, GRAY)
    level_shadow = font.render(f'Level: {level}', True, GRAY)

    screen.blit(score_shadow, (10 + shadow_offset, 10 + shadow_offset))
    screen.blit(highscore_shadow, (10 + shadow_offset, 40 + shadow_offset))
    screen.blit(level_shadow, (10 + shadow_offset, 70 + shadow_offset))

    screen.blit(score_surface, (10, 10))
    screen.blit(highscore_surface, (10, 40))
    screen.blit(level_surface, (10, 70))

def game_over_screen():
    screen.blit(game_over_img, (SCREEN_WIDTH // 2 - game_over_img.get_width() // 2, SCREEN_HEIGHT // 2 - game_over_img.get_height() // 2))

    restart_button = pygame.Rect(SCREEN_WIDTH // 2 - restart_button_img.get_width() // 2, SCREEN_HEIGHT // 2 + 100, restart_button_img.get_width(), restart_button_img.get_height())
    screen.blit(restart_button_img, (restart_button.x, restart_button.y))

    exit_button = pygame.Rect(SCREEN_WIDTH // 2 - exit_button_img.get_width() // 2, SCREEN_HEIGHT // 2 + 200, exit_button_img.get_width(), exit_button_img.get_height())
    screen.blit(exit_button_img, (exit_button.x, exit_button.y))

    pygame.display.update()
    return restart_button, exit_button


def reset_game():
    global bird_movement, bird_y, pipe_x, pipe_y, score, level, pipe_speed, game_active, pipes
    bird_movement = 0
    bird_y = 200
    pipe_x = SCREEN_WIDTH
    pipe_y = random.randint(-300, -100)
    score = 0
    level = 1
    pipe_speed = 3
    game_active = True
    pipes = [(SCREEN_WIDTH, pipe_y)]

def start_game():
    global game_active
    game_active = True
    jump_sound.play()

bird_y = 200
pipe_x = SCREEN_WIDTH
pipe_y = random.randint(-300, -100)
game_active = False
highscore = 0
level = 1
score = 0
bird_movement = 0
pipes = [(SCREEN_WIDTH, pipe_y)]

lobby_image = pygame.image.load('lobby.png').convert()
lobby_image = pygame.transform.scale(lobby_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
screen.blit(lobby_image, (0, 0))

play_button_x = SCREEN_WIDTH // 2 - play_button_img.get_width() // 2
play_button_y = SCREEN_HEIGHT // 2 - play_button_img.get_height() // 2
screen.blit(play_button_img, (play_button_x, play_button_y))

welcome_font = pygame.font.Font(None, 64)
welcome_text = welcome_font.render('Welcome To Super Fly Man', True, BLACK)
welcome_text_x = SCREEN_WIDTH // 2 - welcome_text.get_width() // 2
welcome_text_y = play_button_y - 100
screen.blit(welcome_text, (welcome_text_x, welcome_text_y))

pygame.display.update()


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN and not game_active:
            mouse_pos = event.pos
            if (play_button_x <= mouse_pos[0] <= play_button_x + play_button_img.get_width() and
                play_button_y <= mouse_pos[1] <= play_button_y + play_button_img.get_height()):
                for i in range(3, 0, -1):
                    draw_background()
                    countdown_text = font.render(str(i), True, BLACK)
                    screen.blit(countdown_text, (SCREEN_WIDTH // 2 - 20, SCREEN_HEIGHT // 2 - 20))
                    pygame.display.update()
                    time.sleep(1)
                start_game()

        if event.type == pygame.KEYDOWN and game_active:
            if event.key == pygame.K_SPACE:
                bird_movement = -8


    if game_active:

        bird_movement += gravity
        bird_y += bird_movement

        draw_background()

        for i, (pipe_x, pipe_y) in enumerate(pipes):
            pipes[i] = (pipe_x - pipe_speed, pipe_y)

        if pipes and pipes[0][0] <= -pipe_img.get_width():
            pipes.pop(0)
        if not pipes or pipes[-1][0] <= SCREEN_WIDTH - 400:
            pipe_y = random.randint(-300, -100)
            pipes.append((SCREEN_WIDTH, pipe_y))

        for pipe_x, pipe_y in pipes:
            draw_pipe(pipe_x, pipe_y)

        for pipe_x, _ in pipes:
            if 45 <= pipe_x <= 55:
                score += 1
                break

        bird_rect = bird_img.get_rect(center=(50, bird_y))
        collision = False
        for pipe_x, pipe_y in pipes:
            if check_collision(pipe_x, pipe_y, bird_rect):
                collision = True
                break

        if collision:
            game_over_sound.play()
            if score > highscore:
                highscore = score
            game_active = False
            restart_button, exit_button = game_over_screen()
            while True:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        quit()
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        mouse_pos = event.pos
                        if restart_button.collidepoint(mouse_pos):
                            reset_game()
                            break
                        elif exit_button.collidepoint(mouse_pos):
                            pygame.quit()
                            quit()
                if game_active:
                    break
                pygame.display.update()

        draw_bird(bird_y)
        display_score(score, highscore, level)

        pygame.display.update()

        clock.tick(30)
        
pygame.quit()
quit()
