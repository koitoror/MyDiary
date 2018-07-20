"""Defines routes for CRUD functions in entries
Calls methods from entries model
GET: Reads all entries
    Fetch all entries from db object
POST: Creates an entry
    Takes current_user ID and update data
GET: Read single entries info
PUT: Updates single entries
DELETE: Delete single entries
"""
from flask import Blueprint, jsonify, request
#from versions.v1.models import entries
from versions import login_required
from functools import wraps


mod = Blueprint('entries_v1', __name__)


def precheck(f):
    """Checks if entryID is available
    Check if entry belongs to current user
    """
    @wraps(f)
    def wrap(*args, **kwargs):
        entries = get_in_module('entries', kwargs['entryId'])

        if not entries:
            return jsonify({'warning': 'entries Not Found'}), 404

        if args[0] != entries.owner.id:
            return jsonify({'warning': 'Not Allowed, you are not owner'}), 401

        return f(*args, **kwargs)
    return wrap


@mod.route('/', methods=['GET'])
def read_all_entries():
    """Reads all entries
    user can search for entries via entries name
    response is paginated per limit
    """
    params = {
        'page': request.args.get('page', default=1, type=int),
        'limit': request.args.get('limit', default=5, type=int),
        'location': request.args.get('location', default=None, type=str),
        'category': request.args.get('category', default=None, type=str),
        '_query': request.args.get('q', default=None, type=str)
    }

    entries = entries().Search(params)

    if entries:
        return jsonify({
            'entries': [
                {   'id': entries.entryId,
                    'datetime': entries.date,
                    'title': entries.title,
                    'text': entries.text,
                    'owner': entries.owner.username,
                    'created_at': entries.created_at,
                    'updated_at': entries.updated_at
                } for entries in entries
            ]
        }), 200
    return jsonify({'warning': 'No entries, create one first'}), 404


@mod.route('/', methods=['POST'])
@login_required
def create_entries(current_user):
    """Creates a entries
    Takes current_user ID and update data
    test if actually saved
    """
    data = request.get_json()

    # Check if there is an existing entries with same name
    if existing_module('entries', data['name']):
        return jsonify({
            'warning': 'entries name {} already taken'.format(data['name'])
        }), 409

    entries_owner = get_in_module('user', current_user)

    # create new entries instances
    new_entries = entries(
        datetime=data['date'],
        title=data['title'],
        text=data['text'],
        id=data['entryId'],
        owner=entries_owner
    )

    # Commit changes to db
    new_entries.save()

    # Send response if entries was saved
    if new_entries.id:
        return jsonify({
            'success': 'successfully created entries',
            'entries': {
                'id': entries.entryId,
                'datetime': entries.date,
                'title': entries.title,
                'text': entries.text,
                'owner': entries.owner.username,
                'created_at': entries.created_at,
                'updated_at': entries.updated_at
            }
        }), 201

    return jsonify({'warning': 'Could not create new entries'}), 401


@mod.route('/<entryId>', methods=['GET'])
def read_entries(entryId):
    """Reads entries given a entries id"""
    entries = get_in_module('entries', entryId)

    if entries:
        return jsonify({
            'entries': {
                'id': entries.entryId,
                'datetime': entries.date,
                'title': entries.title,
                'text': entries.text,
                'owner': entries.owner.username,
                'created_at': entries.created_at,
                'updated_at': entries.updated_at
            }
        }), 200
    return jsonify({'warning': 'entries Not Found'}), 404


@mod.route('/<entryId>', methods=['PUT'])
@login_required
@precheck
def update_entries(current_user, entryId):
    """Updates a entries given a entries ID
    confirms if current user is owner of entries
    """
    data = request.get_json()
    entries = get_in_module('entries', entryId)

    entries.datetime = data['date']
    entries.title = data['title']
    entries.text = data['text']
    entries.id = data['entryId']

    entries.save()

    if entries.name == data['name']:
        return jsonify({
            'success': 'successfully updated',
            'entries': {
                'id': entries.entryId,
                'datetime': entries.date,
                'title': entries.title,
                'text': entries.text,
                'owner': entries.owner.username,
                'created_at': entries.created_at,
                'updated_at': entries.updated_at
            }
        }), 201

    return jsonify({'warning': 'entries Not Updated'}), 400


@mod.route('/<entryId>', methods=['DELETE'])
@login_required
@precheck
def delete_entries(current_user, entryId):
    """Deletes a entries
    confirms if current user is owner of entries
    """
    entries = get_in_module('entries', entryId)
    name = entries.name
    entries.delete()

    if not existing_module('entries', name):
        return jsonify({'success': 'entries Deleted'}), 200

    return jsonify({'warning': 'entries Not Deleted'}), 400
