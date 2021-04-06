import pygame


class VisualiserOneLiner:

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
        self.showable_surfaces = []

        self.cmd_arrow = (self.font.render("> ", 1, self.color), x, y)

        # update text after init
        self.update_text(self.text)

    def update_text(self, text):
        """
        Takes a text and turns each character into an individual pygame surface.

        :param text: string to be transformed
        :return:
        """
        self.text = text
        x = self.x + self.cmd_arrow[0].get_width()
        y = self.y

        # logic
        self.surfaces = []
        for character in self.text:
            word_surface = self.font.render(character, 1, self.color)
            word_width, _ = word_surface.get_size()
            self.surfaces.append((word_surface, x, y))
            x += word_width

    def render_text(self):
        """
        Shifts surfaces automatically to the left as long as the last surface does not fit
        into the specified frame width anymore.

        Renders the surfaces within the frame to the screen.

        :return: None
        """

        self.screen.blit(self.cmd_arrow[0], (self.cmd_arrow[1], self.cmd_arrow[2]))

        if len(self.text) == 0:
            return

        # shift all characters to the left until the last character is within the frame
        while self.surfaces[-1][1] + 20 > self.x + self.width:
            # get width of first showable letter
            for s, x, y in self.surfaces:
                if x >= self.x + self.cmd_arrow[0].get_width():
                    shift_by = s.get_width()
                    break

            # shift all letters by the first showable letter's width
            temp_storage = self.surfaces
            self.surfaces = []
            for s, x, y in temp_storage:
                self.surfaces.append((s, x - shift_by, y))

        # blit all character's which are within the frame.
        for s, x, y in self.surfaces:
            if x >= self.x + self.cmd_arrow[0].get_width():
                self.screen.blit(s, (x, y))
