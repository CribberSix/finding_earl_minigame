
class Parser:

    def __init__(self):
        self.last_input = ""

    def handle_input(self, input_text):
        self.last_input = input_text

        if input_text == "help":
            return "Useful commands: \n" \
                   "    Only 'help' implemented - yet."

        return None
