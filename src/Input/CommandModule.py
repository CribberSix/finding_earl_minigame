import pygame
from src.Video.Visualiser import Visualiser


class CommandModule:

    def __init__(self, x, y, w):
        self.current = ""
        self.visualiser = Visualiser(x, y, w)
        self.visualiser.update_text("> " + self.current)
        self.history = [""]
        self.index_h = 0

    def receive_input(self, events):

        for event in [e for e in events if e.type == pygame.KEYDOWN]:

            if event.key == pygame.K_UP:
                self.index_h = self.index_h - 1 if abs(self.index_h) < len(self.history) else self.index_h
                self.current = self.history[self.index_h]

            elif event.key == pygame.K_DOWN:
                self.index_h = self.index_h + 1 if self.index_h < 0 else self.index_h
                self.current = self.history[self.index_h]

            elif event.key == pygame.K_SPACE:
                self.current += " "
            elif event.key == pygame.K_BACKSPACE:
                self.current = self.current[:-1]

            elif event.key == pygame.K_RETURN:  # ___RETURN
                self.history.append(self.current.strip())
                self.current = ""  # reset
                self.index_h = 0  # reset
                self.visualiser.update_text("> " + self.current)
                return self.history[-1]  # return last entry

            elif event.unicode.isalpha():  # This covers all letters and numbers
                self.current += event.unicode

        self.visualiser.update_text("> " + self.current)
        return None

    def render_text(self):
        self.visualiser.render_text()
