class Diary:
    """
    diary class
    """

    def __init__(self, entry_id, name):
        self.id = entry_id
        self.name = name
        self.items = {}

    def create_item(self, item):
        """
        Create a diary item if it does not already exist
        :param item: 
        :return: 
        """
        if item.id in self.items.keys():
            return False
        else:
            self.items[item.id] = item
            return True

    def get_item(self, entry_id):
        """
        Get the item by its Id
        :param entry_id: 
        :return: 
        """
        if entry_id in self.items.keys():
            return self.items[entry_id]
        return None

    def update_item(self, entry_id, name, description, deadline):
        """
        Method to update the item in the diary.
        :param entry_id: 
        :param name: 
        :param description: 
        :param deadline: 
        :return: 
        """
        if entry_id in self.items.keys():
            item = self.items[entry_id]
            item.name = name
            item.description = description
            item.deadline = deadline
            return True
        return False

    def delete_item(self, entry_id):
        """
        Delete an item from the diary.
        :param entry_id: 
        :return: 
        """
        if entry_id in self.items.keys():
            self.items.pop(entry_id)
            return True
        return False


class diaryItem:
    """
    diaryItem class
    """

    def __init__(self, entry_id, name, description, deadline):
        self.id = entry_id
        self.name = name
        self.description = description
        self.deadline = deadline
