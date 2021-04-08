
class Parser:

    def __init__(self):
        """
        The parser is used to map the user's input to game functionality.
        It asks for clarification if it couldn't successfully parse the input.
        """
        self.last_input = ""  # no concrete usage so far
        self.directions = ["west", "east", "south", "north", "forward", "backward", "left", "right"]

    def receive_input(self, input_text):
        """
        The parser takes the user's input string, splits it on spaces
        and tries to map the words to game-functionality.

        In case the parser can map a <verb> directly to a game function, it returns sucessfully.

        The parser returns unsuccessfully with a message, if:
        - too many words were given
        - too little words were given
        - confusing words were given
        - the parser does not know the <verb> or the <object> or any other <parameter>

        Expected syntax:
        <verb> <optional_pronoun> <optional_descriptive_adjective> <object>

        :param input_text:
        :return: Tuple
                    0, ["message"]    # unsuccessful
                    1, [<**args>]     # successful
        """

        self.last_input = input_text.lower().split()

        if self.last_input[0] in ("help", "look", "info", "inventory", "i"):
            return self.parse_one_word_command()
        elif self.last_input[0] in ("go", "walk"):
            return self.parse_go()
        elif self.last_input[0] in ("inspect", "take", "drop", "open"):
            return self.parse_object_command()

        else:
            return 0, ["I do not know this verb."]

    def parse_one_word_command(self):

        if len(self.last_input) > 1:
            return 0, [f"I only understood you as far as wanting to {self.last_input[0]}."]
        else:
            if self.last_input == "i":  # map shortcut to game function
                self.last_input = "inventory"
            return 1, self.last_input

    def parse_object_command(self):
        # depending on the environment, pass on to GameState if an object is given.
        try:
            _ = self.last_input[1]  # at least one more word has to be given (object), optionally with an adjective
            return 1, self.last_input
        except IndexError:
            return 0, [f"What do you want to {self.last_input[0]}?"]

    def parse_go(self):
        """
        Expection:  'go <direction>'
            - Expects a valid direction as the second input
            - Expect no other input

        :return: Tuple
                    0, ["message"]    # unsuccessful
                    1, [<**args>]     # successful
        """
        # get direction
        try:
            desired_direction = self.last_input[1]
            if desired_direction not in self.directions:
                return 0, [f"I only understood you as far as wanting to {self.last_input[0]}."]  # no valid direction given
        except IndexError:
            return 0, [f"Where do you want to {self.last_input[0]} to?"]  # no direction given

        # test if there is another word
        try:
            _ = self.last_input[2]  # second  input is not expected after the direction
            if desired_direction in self.directions:
                return 0, [f"I only understood you as far as wanting to {self.last_input[0]} {self.last_input[1]}."]
            else:
                return 0, [f"I only understood you as far as wanting to {self.last_input[0]}."]

        except IndexError:
            pass  # we don't expect any other arguments

        # Map various expressions to the game functionality
        if desired_direction == "west":
            return 1, ["go", "right"]
        elif desired_direction == "north":
            return 1, ["go", "forward", "forwards"]
        elif desired_direction == "south":
            return 1, ["go", "backward", "backwards"]
        elif desired_direction == "east":
            return 1, ["go", "left"]
        else:
            return 1, ["go", desired_direction]
