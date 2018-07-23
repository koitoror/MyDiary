from flask_restplus import Namespace, fields, reqparse

class EntriesDto(object):
    api = Namespace("entries", description="Entries related operations")
    entries = api.model(
        "entries", {
        "id": fields.Integer(),
        "creation_date": fields.String(),
        "modified_date": fields.String(),
        "title":fields.String(required=True, description="The entry title"),
        "contents":fields.String(required=True, description="The entry contents")
        }
    )
    post_entries = api.model("post_entries",{
        "title": fields.String("entries title"),
        "contents": fields.String("entries contents")
    })

entry_parser = reqparse.RequestParser()
entry_parser.add_argument('title', required=True, type=str, help='title should be a string')
entry_parser.add_argument('contents', required=True, type=str, help='contents should be a string')
update_entry_parser = reqparse.RequestParser()

update_entry_parser.add_argument('title', type=str, help='title should be a string')
update_entry_parser.add_argument('contents', type=str, help='contents should be a string')



