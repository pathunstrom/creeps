import pygame
import logging
import config
import engine
import scenes


def run():
    logging.basicConfig(level=config.LOG_LEVEL)
    pygame.init()
    logging.info("Pygame initialized.")
    if config.FULL_SCREEN:
        display = pygame.display.set_mode(config.RESOLUTION, pygame.FULLSCREEN | pygame.DOUBLEBUF | pygame.HWSURFACE)
    else:
        display = pygame.display.set_mode(config.RESOLUTION)
    logging.info("Display initialized.")
    pygame.display.set_caption(config.TITLE)
    logging.info("Title set")
    game_clock = pygame.time.Clock()
    logging.info("Clock started")
    engine.run(display, game_clock, scenes.Menu, config)
    pygame.quit()

if __name__ == "__main__":
    run()