import pygame
import sys
from src.Video.Visualiser import Visualiser
from src.Input.CommandModule import CommandModule
from src.Parser.Parser import Parser

pygame.init()
pygame.font.init()

# ________________ PYGAME SETUP ________________ #
systemWidth = 600
systemHeight = 500
screen = pygame.display.set_mode((systemWidth, systemHeight))
pygame.display.set_caption("Zork - The adventure awaits!")
clock = pygame.time.Clock()

# Instantiate classes
example_text = "„Lorem ipsum dolor sit amet, consectetur adipisici elit, ist ein Blindtext, der nichts bedeuten soll, sondern als Platzhalter im Layout verwendet wird, um einen Eindruck vom fertigen Dokument zu erhalten. Die Verteilung der Buchstaben und der Wortlängen des pseudo-lateinischen Textes entspricht in etwa der natürlichen lateinischen Sprache. Der Text ist absichtlich unverständlich, damit der Betrachter nicht durch den Inhalt abgelenkt wird."
visualiser = Visualiser(systemWidth * 0.1, systemHeight * 0.1, systemWidth * 0.8, systemHeight * 0.7, example_text)
cmd = CommandModule(systemWidth * 0.1, systemHeight * 0.8, systemWidth * 0.8, systemHeight * 0.1)
parser = Parser()

# ________________ GAME LOOP ________________ #
while True:

    # pygame
    pygame_events = pygame.event.get()
    keys_pressed = pygame.key.get_pressed()
    mouse_x, mouse_y = pygame.mouse.get_pos()  # mouse position
    mouse_pressed = pygame.mouse.get_pressed()

    # event handling
    for event in pygame_events:
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            pass  # print("clicked at: ", mouse_x, mouse_y)

    # get input
    cmd_output = cmd.receive_input(pygame_events)

    # handle input
    if cmd_output is not None:

        # print entered text with leading "> " in a new line
        example_text += "\n\n> " + cmd_output
        visualiser.update_text(example_text)

        # parse the input and print the parser's / the game's answer
        parser_output = parser.handle_input(cmd_output)
        if parser_output is not None:
            example_text += "\n" + parser_output
            visualiser.update_text(example_text)

    # display
    pygame.display.get_surface().fill((200, 200, 200))  # background
    visualiser.render_text()  # instructional text
    cmd.render_text()  # typed text
    pygame.display.flip()  # update screen
    clock.tick(60)  # limit FPS
