import logging
from pygame.locals import K_w, K_a, K_s, K_d

# Application Settings
FPS = 60
RESOLUTION = 600, 400
FULL_SCREEN = False

# Game Settings
CONTROLS = {0: {'up': K_w, 'down': K_s, 'left': K_a, 'right': K_d}}
PLAYER_SPEED = 40
INITIAL_SPAWN = 5

# Developer Settings
LOG_LEVEL = logging.CRITICAL
TITLE = "Creeps"
SPLASH_LENGTH = .25