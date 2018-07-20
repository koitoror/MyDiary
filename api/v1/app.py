#!flask/bin/python
from flask import Flask, jsonify, abort, request, make_response, url_for
from flask.ext.httpauth import HTTPBasicAuth

app = Flask(__name__, static_url_path = "")
auth = HTTPBasicAuth()

@app.route('/')
def index():
    #return render_template('index.html')
    return 'Hello, World'
@auth.get_password
def get_password(username):
    if username == 'Admin':
        return '12345'
    return None

@auth.error_handler
def unauthorized():
    return make_response(jsonify( { 'error': 'Unauthorized access' } ), 403)
    # return 403 instead of 401 to prevent browsers from displaying the default auth dialog
    
@app.errorhandler(400)
def not_found(error):
    return make_response(jsonify( { 'error': 'Bad request' } ), 400)

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify( { 'error': 'Not found' } ), 404)

entries = [
    {
        'id': 1,
        'title': u'Buy groceries',
        'description': u'Milk, Cheese, Pizza, Fruit, Tylenol', 
        'done': False
    },
    {
        'id': 2,
        'title': u'Learn Python',
        'description': u'Need to find a good Python tutorial on the web', 
        'done': False
    }
]

def make_public_entries(entries):
    new_entries = {}
    for field in entries:
        if field == 'id':
            new_entries['uri'] = url_for('get_entries', entryId = entries['id'], _external = True)
        else:
            new_entries[field] = entries[field]
    return new_entries
    
@app.route('/entries', methods = ['GET'])
@auth.login_required
def get_all_entries():
    return jsonify( { 'entries': map(make_public_entries, entries) } )

@app.route('/entries/<int:entryId>', methods = ['GET'])
@auth.login_required
def get_one_entry(entryId):
    entries = filter(lambda t: t['id'] == entryId, entries)
    if len(entries) == 0:
        abort(404)
    return jsonify( { 'entries': make_public_entries(entries[0]) } )

@app.route('/entries', methods = ['POST'])
@auth.login_required
def create_entries():
    if not request.json or not 'title' in request.json:
        abort(400)
    entries = {
        'id': entries[-1]['id'] + 1,
        'title': request.json['title'],
        'description': request.json.get('description', ""),
        'done': False
    }
    entries.append(entries)
    return jsonify( { 'entries': make_public_entries(entries) } ), 201

@app.route('/entries/<int:entryId>', methods = ['PUT'])
@auth.login_required
def update_entries(entryId):
    entries = filter(lambda t: t['id'] == entryId, entries)
    if len(entries) == 0:
        abort(404)
    if not request.json:
        abort(400)
    if 'title' in request.json and type(request.json['title']) != unicode:
        abort(400)
    if 'description' in request.json and type(request.json['description']) is not unicode:
        abort(400)
    if 'done' in request.json and type(request.json['done']) is not bool:
        abort(400)
    entries[0]['title'] = request.json.get('title', entries[0]['title'])
    entries[0]['description'] = request.json.get('description', entries[0]['description'])
    entries[0]['done'] = request.json.get('done', entries[0]['done'])
    return jsonify( { 'entries': make_public_entries(entries[0]) } )
    
@app.route('/entries/<int:entryId>', methods = ['DELETE'])
@auth.login_required
def delete_entries(entryId):
    entries = filter(lambda t: t['id'] == entryId, entries)
    if len(entries) == 0:
        abort(404)
    entries.remove(entries[0])
    return jsonify( { 'result': True } )
    
if __name__ == '__main__':
    app.run(debug = True)