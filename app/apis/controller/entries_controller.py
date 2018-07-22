# third-party imports
from flask_restplus import Resource

# local imports
from ..models.entries import Entry as EntryClass
from ..utils.dto import EntriesDto, entry_parser, update_entry_parser

api = EntriesDto.api
entries = EntriesDto.entries
post_entries = EntriesDto.post_entries

entry = EntryClass()

@api.route("/entries")
class EntryList(Resource):
    """Displays a list of all entries and lets you POST to add new entries."""

    @api.expect(post_entries)
    @api.doc('creates an entry')
    @api.response(201, "Created")
    def post(self):
        """Creates a new Entry."""
        args = entry_parser.parse_args()
        return entry.create_entry(args),201

    @api.doc("list_entries")
    @api.response(404, "Entries Not Found")
    @api.marshal_list_with(entries, envelope="entries")
    def get(self):
        """List all Entries"""
        return entry.get_all()

@api.route("/entries/<int:entryId>")
@api.param("entryId", "entry identifier")
@api.response(404, 'Entry not found')
class Entry(Resource):
    """Displays a single entry item and lets you delete them."""

    @api.marshal_with(entries)
    @api.doc('get one entry')
    def get(self, entryId):
        """Displays a single Entry."""
        return entry.get_one(entryId)

    @api.marshal_with(entries)
    @api.doc('updates an entry')
    @api.expect(post_entries)
    def put(self, entryId):
        """Updates a single Entry."""
        args = update_entry_parser.parse_args()
        return entry.update_entry(entryId, args)

    @api.marshal_with(entries)
    @api.doc('deletes an entry')
    @api.response(204, 'Entry Deleted')
    def delete(self, entryId):
        """Deletes a single Entry."""
        entry.delete_entry(entryId)
        return '',204
