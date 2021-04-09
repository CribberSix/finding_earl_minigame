import yaml
from src.Game.Character import Character


class GameState:

    def __init__(self):
        self.room_current = "Foyer"
        self.character = Character()
        self.displayed_win = False

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

        :param command: String - The command to execute.
        :return: String
        """

        if command[0] == "help":
            return self.help()
        elif command[0] == "info":
            return self.info()
        elif command[0] == "look":
            return self.look()
        elif command[0] in ("inventory", "i"):
            return self.inventory()
        elif command[0] == "go":
            return self.go(command[1])
        elif command[0] in ("inspect", "read"):
            return self.inspect(command[1:])
        elif command[0] == "take":
            return self.take(command[1:])
        elif command[0] == "drop":
            return self.drop(command[1:])
        elif command[0] == "open":
            if len(command[1:]) == 1:
                return self.open(command[1:])
            else:
                return self.open_with(command[1:])

    def open_with(self, command_string):
        """
        Syntax:  open... <optional-ajdective> <object>  with <optional-adjective> <object>
        Syntax:  open... <optional-ajdective> <object>  with <object>
        Syntax:  open... <object>  with <optional-adjective> <object>
        Syntax:  open ... <object> with <object>

        Checks for the 4 different Syntaxes - if it finds no match, error message concerning syntax is given.
        Loads items in the room to check for <object to open>
        Loads items in the inventory to check for <object to open with>

        If it can identify exactly one of both, proceeds, otherwise relevant error messages.

        Final check is whether the item which should be opened can actually be opened with the other item.

        If successful, the item is unlocked and opened.

        :param command_str:
        :return:
        """
        c_length = len(command_string)
        try:
            with_index = command_string.index("with")
        except ValueError:
            return "I don't understand the structure of your sentence. Open it with what?"

        if with_index == 1:  # with as second word
            adjective_open = None
            name_open = command_string[0]
            if c_length == 4:
                adjective_with = command_string[2]
                name_with = command_string[3]
                # print(f"C2 - opening {name_open} with {adjective_with} {name_with}")
            elif c_length == 3:
                adjective_with = None
                name_with = command_string[2]
                # print(f"C3 - opening {name_open} with {name_with}")
            elif c_length == 2:
                return "With what?"

        elif with_index == 2:  # with as third word
            adjective_open = command_string[0]
            name_open = command_string[1]
            if c_length == 5:
                adjective_with = command_string[3]
                name_with = command_string[4]
                # print(f"C5 - opening {adjective_open} {name_open} with {adjective_with} {name_with}")
            elif c_length == 4:
                adjective_with = None
                name_with = command_string[3]
                # print(f"C4 - opening {adjective_open} {name_open} with {name_with}")
            elif c_length == 3:
                return "With what?"
        else:
            return "I don't understand the structure of your sentence. Open it with what?"

        to_open_objects = self.get_room_items_by_name(name_open, adjective_open)
        if len(to_open_objects) == 0:
            return "There is no such object here which you can open."  # found no matching object
        elif len(to_open_objects) > 1:
            return "There is more than one of these objects around here. Which one do you want to open?"

        open_with_objects = self.get_inventory_items_by_name(name_with, adjective_with)
        if len(open_with_objects) == 0:
            return "There is no such object in your inventory which you can use to open it."  # found no matching object
        elif len(open_with_objects) > 1:
            return "There is more than one of these objects in your inventory. Which one do you want to use to open it?"

        if len(to_open_objects) == 1 and len(open_with_objects) == 1:

            if self.items[to_open_objects[0]["id"]]["lockedby"] != open_with_objects[0]["id"]:
                return "This doesn't seem to work..."

            self.items[to_open_objects[0]["id"]]["locked"] = False  # unlock
            self.items[to_open_objects[0]["id"]]["opened"] = True   # is opened

            return f"You use the {open_with_objects[0]['adjective']} {open_with_objects[0]['name']} to open " \
                   f"the {to_open_objects[0]['adjective']} {to_open_objects[0]['name']}. " + \
                   self.inspect([to_open_objects[0]["adjective"], to_open_objects[0]["name"]])

    def open(self, description):
        """
        Syntax:  open... <optional-ajdective> <object>

        :param description: Strings > the object description
        :return: String
        """
        # retrieve matching items
        adjective, object_name = self.parse_description(description)
        objects = self.get_room_items_by_name(object_name, adjective)

        # return based on number of objects in resulting list
        if len(objects) == 0:
            return "There is no such object here."  # found no matching object
        elif len(objects) > 1:
            return "There is more than one of these objects around here. Which one do you want to take?"
        elif len(objects) == 1:
            if not objects[0]["open"]:
                return "You can't open this."
            elif objects[0]["locked"]:
                return "It is locked. With what do you want to open it?"
            else:  # open-able and not locked
                self.items[objects[0]["id"]]["opened"] = True
                return "You open it. " + self.get_inner_inspection(objects[0]["id"])

    def check_winning_condition(self):
        """
        Checks if the teddy bear is in the character's inventory - once it is, we display the congratulatory message.

        :return: String or None
        """
        if not self.displayed_win:
            if len(self.get_inventory_items_by_name("teddybear", "fluffy")) == 1:
                self.displayed_win = True
                return self.texts["win"]
                return "" \
                       "\n          *" \
                       "\n         /_\\" \
                       "\n       { 0_0 } " \
                       "\n        ( Y )  " \
                       "\n       ()~*~()    " \
                       "\n       (_)-(_)    " \
                       "\n\nCongratulations! You found Earl! \n\nFeel free to walk around and explore all rooms and items " \
                       "if you haven't already. Thank you for playing!"

    def get_inventory_items_by_name(self, name, adjective):
        """
        Collect all items in the inventory matching the name (and optionally adjective).

        :param name: String > the name of the item
        :param adjective: String > adjective of the item
        :return: List
        """
        objects = []
        for obj_id in self.character.inventory:
            if self.items[obj_id]["name"] == name:
                objects.append(self.items[obj_id])

        # filter objects for adjective if one was given
        if adjective is not None:
            objects = [obj for obj in objects if obj["adjective"] == adjective]
        return objects

    def get_room_items_by_name(self, name, adjective):
        """
        Collect all items in the room matching the name (and optionally adjective),
        also looks into open container items and checks contents (one level depth)

        :param name: String > the name of the item
        :param adjective: String > adjective of the item
        :return: List
        """
        objects = []
        if self.rooms[self.room_current]["items"] is not None:
            for obj_id in self.rooms[self.room_current]["items"]:
                if self.items[obj_id]["name"] == name:  # filter items
                    objects.append(self.items[obj_id])

                # opened item and contains other items
                if self.items[obj_id]["opened"] and self.items[obj_id]["contains"] is not None:
                    for inner_obj_id in self.items[obj_id]["contains"]:
                        if self.items[inner_obj_id]["name"] == name:  # filter inner items
                            objects.append(self.items[inner_obj_id])

        # filter objects for adjective if one was given
        if adjective is not None:
            objects = [obj for obj in objects if obj["adjective"] == adjective]

        return objects

    def drop(self, description):
        """
       Collects all objects in the inventory and tries to match the given description.

       Returns error/clarification messages if no object or multiple objects were found.
       Returns a "You dropped the <adjective> <object> of the matching object if exactly one was found.

       :param description: String to parse into the object description
       :return: String
       """
        adjective, object_name = self.parse_description(description)
        objects = self.get_inventory_items_by_name(object_name, adjective)

        # return based on number of objects in resulting list
        if len(objects) == 0:  # found no matching object
            return "There is no such object in your inventory."
        elif len(objects) == 1:  # found exactly one matching object

            # remove id from the inventory
            self.character.inventory.remove(objects[0]["id"])

            # append id of the object to the room's items
            self.rooms[self.room_current]["items"].append(objects[0]["id"])
            self.items[objects[0]["id"]]["location"] = "on the floor"  # dropped

            return f"You drop the {objects[0]['adjective']} {objects[0]['name']}."

        elif len(objects) > 1:  # multiple objects fitting the description (description without adjective)
            return "There is more than one of these objects in your inventory. Which one do you want to drop?"

    def inventory(self):
        """
        Returns a string of the inventory's contents.
        :return:
        """

        if len(self.character.inventory) == 0:
            return "Your inventory is empty."

        # collect items and build strings
        i_string = "Your inventory includes:\n"
        for item_id in self.character.inventory:
            item = self.items[item_id]
            i_string += "   - a " + item["adjective"] + " " + item["name"] + "\n"
        return i_string

    def parse_description(self, description):
        """
        Parses a string into an adjective and an object if possible.

        :param description: string to parse.
        :return: Tuple (adjective, object)   - adject could be None.
        """
        if len(description) > 1:
            adj = description[0]
            obj = description[1]
        else:
            adj = None
            obj = description[0]
        return adj, obj

    def take(self, description):
        """
        Collects all objects in the room and tries to match the given description.

        Returns error/clarification messages if no object or multiple objects were found.
        Returns a "You take the <adjective> <object> of the matching object if exactly one was found.

        :param description: String to parse into the object description
        :return: String
        """
        adjective, object_name = self.parse_description(description)
        objects = self.get_room_items_by_name(object_name, adjective)

        # return based on number of objects in resulting list
        if len(objects) == 0:
            return "There is no such object here."  # found no matching object
        elif len(objects) == 1:
            if not objects[0]["collect"]:
                return "You can't seriously want to take this..."

            # append id to inventory
            self.character.inventory.append(objects[0]["id"])

            # remove item from room / from within items in the room
            self.remove_item_from_room(objects[0]["id"])


            # return string
            return f"You take the {objects[0]['adjective']} {objects[0]['name']}."  # found exactly one matching object

        elif len(objects) > 1:
            return "There is more than one of these objects around here. Which one do you want to take?"

    def remove_item_from_room(self, item_id):
        if item_id in self.rooms[self.room_current]["items"]:  # directly in the room
            self.rooms[self.room_current]["items"].remove(item_id)
        else:  # inside something in the room
            for roomitem in self.rooms[self.room_current]["items"]:
                if self.items[roomitem]["contains"] is not None and item_id in self.items[roomitem]["contains"]:
                    self.items[roomitem]["contains"].remove(item_id)

    def inspect(self, description):
        """
        Collects all objects in the room as well as in the inventory of the player
        and tries to match the given description.

        Returns error/clarification messages if no object or multiple objects were found.
        Returns the "inspection" attribute of an object if only one was found.

        :param description: String to parse into the object description
        :return: String
        """

        adjective, object_name = self.parse_description(description)
        # collect all objects in inventory + room which fit the name
        objects = self.get_inventory_items_by_name(object_name, adjective)
        objects = objects + self.get_room_items_by_name(object_name, adjective)

        # return based on number of objects in resulting list
        if len(objects) == 0:
            return "There is no such object here or in your inventory."  # found no matching object
        elif len(objects) == 1:
            inner_item_string = self.get_inner_inspection(objects[0]["id"])
            inner_item_string = " " + inner_item_string if inner_item_string is not None else ""
            return objects[0]["inspection"] + inner_item_string  # found exactly one matching object
        elif len(objects) > 1:
            return "There is more than one of these objects around here / in your inventory. Which one do you mean?"

    def get_inner_inspection(self, item_id):
        """
        Gets inner items based on ID.

        :param item_id: Integer
        :return: String
        """

        sentence = ""
        if not self.items[item_id]["open"]:  # cannot be opened
            return ""
        elif not self.items[item_id]["opened"]:  # can be opened, but is closed.
            return "You will need to open it first. "

        else:  # can be opened and is opened
            if self.items[item_id]["contains"] is None or len(self.items[item_id]["contains"]) == 0:
                sentence += " There is nothing inside."

            else:  # items exist
                sentence += " Inside is "
                for i, inner_item_id in enumerate(self.items[item_id]["contains"]):

                    # create sentence for each item
                    inner_name = self.items[inner_item_id]["name"]
                    inner_adjective = self.items[inner_item_id]["adjective"]
                    inner_article = 'an' if inner_adjective[0] in 'aoeiu' else 'a'
                    if i == 0:
                        sentence += f"{inner_article} {inner_adjective} {inner_name}"
                    elif i > 0 and i == len(self.items[item_id]["contains"]) - 1:
                        sentence += f" and {inner_article} {inner_adjective} {inner_name}"
                    else:
                        sentence += f", {inner_article} {inner_adjective} {inner_name}"
                sentence += ". "
            return sentence

    def help(self):
        return self.texts["help"]

    def info(self):
        return self.texts["info"]

    def look(self):
        """
        Compiles all accessible items in the room and in open items of the room and returns a describing string.

        :return: String
        """
        room_description = self.rooms[self.room_current]["description"]
        path_description = self.rooms[self.room_current]["path_description"]
        items_description = ""
        if self.rooms[self.room_current]["items"] is None:
            return room_description + " \n" + path_description

        for item in self.rooms[self.room_current]["items"]:
            name = self.items[item]["name"]
            adjective = self.items[item]["adjective"]
            article = 'an' if adjective[0] in 'aoeiu' else 'a'
            location = self.items[item]["location"]

            # TODO: apply different sentence structures for items (not always "There is...")
            # "You notice a... " "There is ... " "A {adjective} {name} is {location}"  etc.
            if self.items[item]["open"]:  # can be opened
                status = ", it is opened" if self.items[item]["opened"] else ", but it is closed"
                sentence = f"There is {article} {adjective} {name} {location}{status}. "
            else:
                sentence = f"There is {article} {adjective} {name} {location}. "

            sentence += self.get_inner_inspection(item)
            items_description += sentence
        return room_description + " " + items_description + "\n" + path_description

    def go(self, direction):
        """
        Changes room if a path in the desired direction exists
        and returns the description of the new room.

        Blocks the player if no path exists in the desired direction.

        :param direction: String
        :return: String
        """
        next_room = self.rooms[self.room_current]["paths"][direction]

        if next_room is None:
            return "You cannot go that way."
        else:
            self.room_current = next_room
            return self.look()
