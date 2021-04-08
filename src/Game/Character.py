

class Character:

    def __init__(self):
        self.hp = 3
        self.hp_max = 3
        self.inventory = []  # list of item-keys

    def func(self):
        pass

    def take(self, obj):
        self.inventory.append(obj)

    def drop(self, obj_name):
        """
        Deletes an object based on the passed object-name (optionally with descriptive adjective) from the
        inventory.

        :param obj_name: string consisting of object name or object adjective + name
        :return: json object
        """

        for i, item in enumerate(self.inventory):
            if item["name"] == obj_name or item["adjective"] + " " + item["name"]:
                obj = item
                del self.inventory[i]
                return obj
