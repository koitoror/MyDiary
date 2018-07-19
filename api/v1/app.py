from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
import uuid
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime
from functools import wraps

app = Flask(__name__)

@app.route('/entries', methods=['GET'])
#@token_required
def get_all_entries():
    """
    entries = entries.query.filter_by(user_id=current_user.id).all()

    output = []

    for entries in entries:
        entries_data = {}
        entries_data['id'] = entries.id
        entries_data['date'] = entries.datetime
        entries_data['title'] = entries.title
        entries_data['text'] = entries.text
        entries_data['modify'] = entries.modify
        output.append(entries_data)

    return jsonify({'entries' : output})
    """

    return jsonify({'message' : 'all entries fetched!'})

@app.route('/entries/<entryId>', methods=['GET'])
#@token_required
def get_one_entries():
    """
    entries = entries.query.filter_by(id=entryId, user_id=current_user.id).first()

    if not entries:
        return jsonify({'message' : 'No entries found!'})

    entries_data = {}
    entries_data['id'] = entries.id
    entries_data['text'] = entries.text
    entries_data['modify'] = entries.modify

    return jsonify(entries_data)
    """

    data = request.get_json()

    datetime = data ['date']
    title = data['title']
    text = data['text']
    entryId = data['entryId']

    return jsonify({'message' : 'single entry fetched!',  "date": datetime, 'title': title, 'text': text, 'entryId': entryId[0]})

@app.route('/entries', methods=['POST', 'GET'])
#@token_required
def create_entries():
    """
    new_entries = entries(text=data['text'], modify=False, user_id=current_user.id)
    db.session.add(new_entries)
    db.session.commit()
    """

    data = request.get_json()

    datetime = data ['date']
    title = data['title']
    text = data['text']
    entryId = data['entryId']

    return jsonify({"message" : "entry created!", "date": datetime, 'title': title, 'text': text, 'entryId': entryId[1]})

@app.route('/entries/<entryId>', methods=['PUT'])
#@token_required
def modify_entries():
    """
    entries = entries.query.filter_by(id=entryId, user_id=current_user.id).first()

    if not entries:
        return jsonify({'message' : 'No entries found!'})

    entries.modify = True
    db.session.commit()
    """
    data = request.get_json()

    datetime = data ['date']
    title = data['title']
    text = data['text']
    entryId = data['entryId']
    return jsonify({'message' : 'entry item has been modified!',  "date": datetime, 'title': title, 'text': text, 'entryId': entryId[2]})

@app.route('/entries/<entryId>', methods=['DELETE'])
#@token_required
def delete_entries():
    """
    entries = entries.query.filter_by(id=entryId, user_id=current_user.id).first()

    if not entries:
        return jsonify({'message' : 'No entries found!'})

    db.session.delete(entries)
    db.session.commit()
    """

    data = request.get_json()

    datetime = data ['date']
    title = data['title']
    text = data['text']
    entryId = data['entryId']
    return jsonify({'message' : 'entries item deleted!',  "date": datetime, 'title': title, 'text': text, 'entryId': entryId[3]})

if __name__ == '__main__':
    app.run(debug=True)