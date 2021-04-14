

class Character:

    def __init__(self):
        self.inventory = []  # list of item-keys

    def take(self, obj_id):
        """
        Appends an object-id to the inventory.

        :param obj_id: String
        :return: None
        """
        self.inventory.append(obj_id)

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
