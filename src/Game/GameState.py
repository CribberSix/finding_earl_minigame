import yaml
from src.Game.Character import Character


class GameState:

    def __init__(self):
        self.room_current = "Foyer"
        self.character = Character()
        with open('./ressources/texts.yml') as f:
            self.texts = yaml.load(f, Loader=yaml.FullLoader)

        with open('./ressources/map/items.yml') as f:
            self.items = yaml.load(f, Loader=yaml.FullLoader)

        with open('./ressources/map/rooms.yml') as f:
            self.rooms = yaml.load(f, Loader=yaml.FullLoader)

    def receive_input(self, command):
        """
        The functions takes the parser's arguments and executes the relevant game-functions
        as well as passes on the necessary parameters.

        :param command: The command to execute.
        :return:
        """

        if command == "help":
            return self.help()
        elif command == "info":
            return self.info()
        elif command == "look":
            room_description = self.rooms[self.room_current]["description"]
            path_description = self.rooms[self.room_current]["path_description"]
            items_description = ""
            for item in self.rooms[self.room_current]["items"]:
                name = self.items[item]["name"]
                adjective = self.items[item]["adjective"]
                location = self.items[item]["location"]

                # TODO: apply different sentence structures for items (not always "There is...")
                # "You notice a... " "There is ... " "A {adjective} {name} is {location}"  etc. 
                if adjective[0] in 'aoei':
                    sentence = f"There is an {adjective} {name} {location}. "
                else:
                    sentence = f"There is a {adjective} {name} {location}. "
                items_description += sentence
            return room_description + " " + items_description + "\n" + path_description
        else:
            return "I do not know this verb."

    def help(self):
        return self.texts["help"]

    def info(self):
        return self.texts["info"]