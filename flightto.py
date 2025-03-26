# Importing the libraries
import pygame
import sys
import time
import random
import math
from pygame import mixer

# Initializing the pygame
pygame.init()


# Initialize the mixer
mixer.init()

# Frames per second
clock = pygame.time.Clock()

# Timer
elapsed_time = 0  # Track elapsed time in milliseconds
game_start_time = 0  # Track the start time of the game


# Load soundtracks
calm_sound = mixer.Sound("calm_track.wav")
intense_sound = mixer.Sound("intense_track.wav")
game_over_sound = mixer.Sound("game_over_track.wav")

# Volume settings
calm_sound.set_volume(0.5)
intense_sound.set_volume(0.7)
game_over_sound.set_volume(0.8)

# Current sound state
current_sound = None

def reset_game():
    global game_over, pipes, plane_movement, plane_rect, score, score_time, elapsed_time, game_start_time

    # Reset game variables
    game_over = False
    pipes = []
    plane_movement = 0
    plane_rect = plane_img.get_rect(center=(67, height // 2))
    score_time = True
    score = 0
    

    # Reset timer
    elapsed_time = 0
    game_start_time = pygame.time.get_ticks()


# Function to handle sound transitions
def manage_sound():
    global current_sound, game_over

    if game_over:
        # Play game over soundtrack
        if current_sound != "game_over":
            calm_sound.stop()
            intense_sound.stop()
            game_over_sound.play(-1)  # Loop game over sound
            current_sound = "game_over"
    else:
        # Determine if the game is in an intense phase
        intense_phase = any(pipe.left < plane_rect.right + 50 for pipe in pipes)
        
        if intense_phase:
            # Play intense soundtrack
            if current_sound != "intense":
                calm_sound.stop()
                game_over_sound.stop()
                intense_sound.play(-1)  # Loop intense sound
                current_sound = "intense"
        else:
            # Play calm soundtrack
            if current_sound != "calm":
                intense_sound.stop()
                game_over_sound.stop()
                calm_sound.play(-1)  # Loop calm sound
                current_sound = "calm"


# Function to create pipes
def create_pipes():
    pipe_y = random.choice(pipe_height)
    top_pipe = pipe_img.get_rect(midbottom=(467, pipe_y - 300))
    bottom_pipe = pipe_img.get_rect(midtop=(467, pipe_y))
    return top_pipe, bottom_pipe


# Function for animation
def pipe_animation():
    global game_over, score_time
    for pipe in pipes:
        if pipe.top < 0:
            flipped_pipe = pygame.transform.flip(pipe_img, False, True)
            screen.blit(flipped_pipe, pipe)
        else:
            screen.blit(pipe_img, pipe)

        pipe.centerx -= 3
        if pipe.right < 0:
            pipes.remove(pipe)

        if plane_rect.colliderect(pipe):
            game_over = True

# Function to draw score
def draw_score(game_state):
    if game_state == "game_on":
        score_text = score_font.render(str(score), True, (255, 255, 255))
        score_rect = score_text.get_rect(center=(width // 2, 66))
        screen.blit(score_text, score_rect)
    elif game_state == "game_over":
        score_text = score_font.render(f" Score: {score}", True, (255, 255, 255))
        score_rect = score_text.get_rect(center=(width // 2, 100))
        screen.blit(score_text, score_rect)

        high_score_text = score_font.render(f"High Score: {high_score}", True, (255, 255, 255))
        high_score_rect = high_score_text.get_rect(center=(width // 2, 530))
        screen.blit(high_score_text, high_score_rect)


# Function to update the score
def score_update():
    global score, score_time, high_score
    if pipes:
        for pipe in pipes:
            if 65 < pipe.centerx < 69 and score_time:
                score += 1
                score_time = False
            if pipe.left <= 0:
                score_time = True

    if score > high_score:
        high_score = score


# Game window
width, height = 350, 622
clock = pygame.time.Clock()
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Flight To")

# setting background and base image
back_img = pygame.image.load("img_46.png")
floor_x = 0

# Adding dynamic themes
themes = {
    "morning": {
        "background": pygame.image.load("morning.png"),
        
        "pipe": pygame.image.load("morning_pipe.png"),
    },
    "noon": {
        "background": pygame.image.load("noon.png"),
        
        "pipe": pygame.image.load("noon_pipe.png"),
    },
    "evening": {
        "background": pygame.image.load("evening.png"),
        
        "pipe": pygame.image.load("evening_pipe.png"),
    },
    "night": {
        "background": pygame.image.load("night.png"),
       
        "pipe": pygame.image.load("night_pipe.png"),
    },
}

current_theme = "morning"  # Initial theme

# Adding a timer to switch themes
theme_switch_event = pygame.USEREVENT + 2
pygame.time.set_timer(theme_switch_event, 15000)  # Switch every 15 seconds


# Snowflake Class for Winter Effect
class Snowflake(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((5, 5))
        self.image.fill((255, 255, 255))
        self.rect = self.image.get_rect(center=(random.randint(0, width), random.randint(-20, height)))

    def update(self):
        self.rect.y += 2  # Move down
        if self.rect.top > height:
            self.rect.center = (random.randint(0, width), random.randint(-20, -1))


# Group for seasonal animations
snowflakes = pygame.sprite.Group()

# different stages of plane
plane_up = pygame.image.load("img_47.png")
plane_down = pygame.image.load("img_48.png")
plane_mid = pygame.image.load("img_49.png")
plane = [plane_up, plane_mid, plane_down]
plane_index = 0
plane_fly = pygame.USEREVENT
pygame.time.set_timer(plane_fly, 200)
plane_img = plane[plane_index]
plane_rect = plane_img.get_rect(center=(67, 622 // 2))
plane_movement = 0
gravity = 0.17

# Loading pipe image
pipe_img = pygame.image.load("greenpipe.png")
pipe_height = [400, 350, 533, 490]

# for the pipes to appear
pipes = []
create_pipe = pygame.USEREVENT + 1
pygame.time.set_timer(create_pipe, 1200)

# Displaying game over image
game_over = False
over_img = pygame.image.load("img_45.png").convert_alpha ()
over_rect = over_img.get_rect(center=(width // 2, height // 2))

# setting variables and font for score
score = 0
high_score = 0
score_time = True
score_font = pygame.font.Font("freesansbold.ttf", 27)

def draw_timer():
    timer_text = score_font.render(f"Time: {elapsed_time // 1000}s", True, (255, 255, 255))
    timer_rect = timer_text.get_rect(center=(width // 2, 30))
    screen.blit(timer_text, timer_rect)


# game loop

running = True
while running:
    clock.tick(120)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            sys.exit()
        if not game_over:
           elapsed_time = pygame.time.get_ticks() - game_start_time
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not game_over:
                plane_movement = -7
            if event.key == pygame.K_SPACE and game_over:
                reset_game()
                

        # Handle plane animation
        if event.type == plane_fly:
            plane_index += 1
            if plane_index > 2:
                plane_index = 0
            plane_img = plane[plane_index]

        # Add pipes
        if event.type == create_pipe:
            pipes.extend(create_pipes())

        # Handle theme switching
        if event.type == theme_switch_event:
            themes_list = list(themes.keys())
            current_index = themes_list.index(current_theme)
            current_theme = themes_list[(current_index + 1) % len(themes_list)]

            # Update images
            back_img = themes[current_theme]["background"]
            pipe_img = themes[current_theme]["pipe"]

            # Add snowflakes if it's winter
            if current_theme == "winter":
                for _ in range(20):  # Add 20 snowflakes
                    snowflakes.add(Snowflake())
            # Update seasonal animations
            if current_theme == "winter":
               snowflakes.update()
               snowflakes.draw(screen)

    # Draw current background
    screen.blit(back_img, (0, 0))

    # Game over conditions
    if not game_over:
        plane_movement += gravity
        plane_rect.centery += plane_movement
        rotated_plane = pygame.transform.rotozoom(plane_img, plane_movement * -6, 1)

        if plane_rect.top < 5 or plane_rect.bottom >= 550:
            game_over = True

        screen.blit(rotated_plane, plane_rect)
        pipe_animation()
        score_update()
        draw_score("game_on")
        draw_timer()

    else:
        screen.blit(over_img, over_rect)
        draw_score("game_over")

    # Manage sound based on the game state
    manage_sound()

    # Update the game window
    pygame.display.update()

# Cleanup
mixer.stop()
pygame.quit()
sys.exit()


