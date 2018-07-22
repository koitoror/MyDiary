class User:
    """
    User model class 
    """

    def __init__(self, username, password, name=None):
        self.username = username
        self.name = name
        self.password = password
        self.entries = {}

    def create_diary(self, diary):
        """
        Create a diary if it does not exist already
        :param diary: 
        :return: 
        """
        if diary.id in self.entries.keys():
            return False
        else:
            self.entries[diary.id] = diary
            return True

    def update_diary(self, entry_id, name):
        """
        This method first checks whether the diary exists,
        if it does it changes the diary name to the
        new one
        :param entry_id: 
        :param name: 
        :return: 
        """
        if entry_id in self.entries.keys():
            diary = self.entries[entry_id]
            diary.name = name
            return True
        return False

    def delete_diary(self, entry_id):
        """
        Delete a diary from the User's diary if
        it exists.
        :param entry_id: 
        :return: 
        """
        if entry_id in self.entries.keys():
            self.entries.pop(entry_id)
            return True
        return False

    def get_entries(self):
        """
        Get a user's entries
        :return: 
        """
        return self.entries

    def get_diary(self, entry_id):
        """
        Get a user's diary by Id
        :param entry_id: 
        :return: 
        """
        if entry_id in self.entries.keys():
            return self.entries[entry_id]
        return None


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

    def get_item(self, item_id):
        """
        Get the item by its Id
        :param item_id: 
        :return: 
        """
        if item_id in self.items.keys():
            return self.items[item_id]
        return None

    def update_item(self, item_id, name, description, deadline):
        """
        Method to update the item in the diary.
        :param item_id: 
        :param name: 
        :param description: 
        :param deadline: 
        :return: 
        """
        if item_id in self.items.keys():
            item = self.items[item_id]
            item.name = name
            item.description = description
            item.deadline = deadline
            return True
        return False

    def delete_item(self, item_id):
        """
        Delete an item from the diary.
        :param item_id: 
        :return: 
        """
        if item_id in self.items.keys():
            self.items.pop(item_id)
            return True
        return False


class diaryItem:
    """
    diaryItem class
    """

    def __init__(self, item_id, name, description, deadline):
        self.id = item_id
        self.name = name
        self.description = description
        self.deadline = deadline
