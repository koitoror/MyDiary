from datetime import datetime
from ..utils.dto import EntriesDto

api = EntriesDto.api

class Entry(object):
    """ CLASS FOR ADDING, EDITING AND DELETING DIARY ENTRIES."""

    def __init__(self):
        """constructor method"""

        self.no_of_entries = []

    def create_entry(self, data):
        """Method for creating an entry"""

        data["id"] = int(len(self.no_of_entries) + 1)
        data["creation_date"] = str(datetime.now().strftime('%d-%b-%Y : %H:%M:%S'))
        self.no_of_entries.append(data)
        return data

    def get_one(self, entry_id):
        """Method for fetching one entry by its id"""
        entry = [entry for entry in self.no_of_entries if entry["id"] == entry_id]

        if not entry:
            api.abort(404, "Entry {} does not exist".format(entry_id))
        return entry

    def delete_entry(self, entry_id):
        "Method for deleting an entry"

        entry = self.get_one(entry_id)
        self.no_of_entries.remove(entry[0])

    def update_entry(self, entry_id, data):
        """Method for updating an entry"""

        entry = self.get_one(entry_id)
        data['modified_date'] = str(datetime.now().strftime('%d-%b-%Y : %H:%M:%S'))
        entry[0].update(data)
        return entry

    def get_all(self):
        """Method for returning all entries."""
        entries = [entries for entries in self.no_of_entries]
        if not entries:
            api.abort(404, "No Entries Found.")
        return entries
