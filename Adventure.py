import pygame
import sys
from src.Video.Visualiser import Visualiser
from src.Input.CommandModule import CommandModule
from src.Parser.Parser import Parser
from src.Game.GameState import GameState

pygame.init()
pygame.font.init()

# ________________ PYGAME SETUP ________________ #
systemWidth = 600
systemHeight = 500
screen = pygame.display.set_mode((systemWidth, systemHeight))
pygame.display.set_caption("Zork - The adventure awaits!")
clock = pygame.time.Clock()

# Instantiate classes
current_text = "You wake up, your dizzy head hurting. There is not much you can remember... "
visualiser = Visualiser(systemWidth * 0.1, systemHeight * 0.1, systemWidth * 0.8, systemHeight * 0.7, current_text)
cmd = CommandModule(systemWidth * 0.1, systemHeight * 0.8, systemWidth * 0.8, systemHeight * 0.1)
parser = Parser()
game = GameState()

# ________________ GAME LOOP ________________ #
while True:

    # pygame event handling
    pygame_events = pygame.event.get()
    keys_pressed = pygame.key.get_pressed()
    mouse_x, mouse_y = pygame.mouse.get_pos()  # mouse position
    mouse_pressed = pygame.mouse.get_pressed()
    for event in pygame_events:
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # get user input
    cmd_output = cmd.receive_input(pygame_events)

    # handle user input
    if cmd_output is not None:

        # print entered text with leading "> " in a new line
        current_text += "\n\n> " + cmd_output
        visualiser.update_text(current_text)

        # parse user input
        parser_output = parser.receive_input(cmd_output)

        # if the parser failed -> print the parser's message
        if parser_output is not None and parser_output[0] == 0:
            current_text += "\n" + parser_output[1]
            visualiser.update_text(current_text)

        # if the  parser succeeded -> handle parsed input in the GameState class
        elif parser_output is not None and parser_output[0] == 1:
            game_output = game.receive_input(parser_output[1])

            # print the game's message
            if game_output is not None:
                current_text += "\n" + game_output
                visualiser.update_text(current_text)

    # display
    pygame.display.get_surface().fill((200, 200, 200))  # background
    visualiser.render_text()  # instructional text
    cmd.render_text()  # typed text
    pygame.display.flip()  # update screen
    clock.tick(60)  # limit FPS
