import pygame


class Visualiser:

    def __init__(self, x, y, w, text="", font=None, color=None):
        self.screen = pygame.display.get_surface()

        self.x = x
        self.y = y
        self.width = w
        self.text = text

        self.font = font if font is not None else pygame.font.Font('./ressources/Courier_New.ttf', 15)
        self.color = color if color is not None else pygame.Color('black')

        self.word_height = self.font.render("Test-string for height", 1, self.color).get_size()[1]
        self.space_width = self.font.size(' ')[0]

    def update_text(self, text):
        self.text = text

    def render_text(self):
        """
        Renders a specific text:
            - Automatic new lines if a word does not fit in the same line anymore.
        """
        x = self.x
        y = self.y

        # logic
        words = [line.split(' ') for line in self.text.splitlines()]  # 2D array where each row is a list of words.
        for line in words:
            for word in line:
                word_surface = self.font.render(word, 1, self.color)
                word_width, _ = word_surface.get_size()
                if x + word_width >= self.x + self.width:
                    x = self.x  # Reset the x.
                    y += self.word_height  # Start on new row.
                self.screen.blit(word_surface, (x, y))
                x += word_width + self.space_width
            x = self.x  # Reset the x.
            y += self.word_height  # Start on new row.
