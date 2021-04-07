
class Parser:

    def __init__(self):
        """
        The parser is used to map the user's input to game functionality.
        It asks for clarification if it couldn't successfully parse the input.
        """
        self.last_input = ""  # no concrete usage so far

    def receive_input(self, input_text):
        """
        The parser takes the user's input string, splits it on spaces
        and tries to map the words to game-functionality.

        In case the parser can map a <verb> directly to a game function, it returns sucessfully.

        In case too many words were given, the parser returns unsuccessfully with a message.
        In case too little words were given, the parser returns unsuccessfully with a message.

        Expected syntax:
        <verb> <optional_pronoun> <optional_descriptive_adjective> <object>

        :param input_text:
        :return: Tuple
                    (0, message)         # unsucessful
                    (1, parsed_message)  # successful
        """

        # TODO: what should the parser handle?

        self.last_input = input_text.lower().split()

        if self.last_input[0] in ("help", "look", "info"):
            if len(self.last_input) > 1:
                return 0, f"I only understood you as far as wanting to {self.last_input[0]}."
            else:
                return 1, self.last_input[0]
        else:
            return 1, ' '.join(self.last_input)
