import pygame


class Visualiser:

    def __init__(self, x, y, w, h, text="", font=None, color=None):
        self.screen = pygame.display.get_surface()

        self.x = x
        self.y = y
        self.width = w
        self.height = h
        self.text = text

        self.font = font if font is not None else pygame.font.Font('./ressources/Courier_New.ttf', 15)
        self.color = color if color is not None else pygame.Color('black')

        self.word_height = self.font.render("Test-string for height", 1, self.color).get_size()[1]
        self.space_width = self.font.size(' ')[0]
        self.surfaces = []
        self.update_text(self.text)

    def update_text(self, text):
        """
        Takes a text and splits it into physical lines.

        Automatic new lines if a word does not fit in the same line anymore.
        :param text: string to be transformed
        :return: None
        """
        self.text = text
        x = self.x
        y = self.y

        # logic
        self.surfaces = []
        words = [line.split(' ') for line in self.text.splitlines()]  # 2D array where each row is a list of words.
        for line in words:
            for word in line:
                word_surface = self.font.render(word, 1, self.color)
                word_width, _ = word_surface.get_size()
                if x + word_width >= self.x + self.width:
                    x = self.x  # Reset the x.
                    y += self.word_height  # Start on new row.
                self.surfaces.append((word_surface, x, y))
                # self.screen.blit(word_surface, (x, y))
                x += word_width + self.space_width
            x = self.x  # Reset the x.
            y += self.word_height  # Start on new row.

    def render_text(self):
        """
        Moves surfaces upwards by one line-height as long as the last surface's y-coordinate
        is beneath the height.
        Renders the surfaces which are within the frame to the screen.

        :return: None
        """

        while self.surfaces[-1][2] + 2 * self.word_height > self.y + self.height:
            temp_storage = self.surfaces
            self.surfaces = []
            for s, x, y in temp_storage:
                self.surfaces.append((s, x, y - self.word_height))

        # render surfaces
        for s, x, y in self.surfaces:
            if y >= self.y:
                self.screen.blit(s, (x, y))
