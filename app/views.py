from flask import Flask, jsonify, request, abort
from app import app
from app.models import Diary
from app.models import diaryItem


entryDB=[
 {
 'entry_id':'1',
 'title':'Hello',
 'body':'Greetings To Start Off My Diary Postings'
 },
 {
 'entry_id':'2',
 'title':'Hey',
 'body':'My Second Entry Ever'
 }
 ]
 
@app.route('/api/v1/entries/',methods=['GET'])
def getAllEntries():
    return jsonify({'entries':entryDB, 'message': 'All entries viewed.'}), 200

@app.route('/api/v1/entries/<int:entry_id>',methods=['GET'])
def getEntry(entry_id):
    usr = []
    usr = [ entry for entry in entryDB if (entry['entry_id'] == entry_id) ] 
    return jsonify({'entry':usr, 'message': 'Entry viewed.'}), 200

@app.route('/api/v1/entries/<int:entry_id>',methods=['POST'])
def createEntry():
    dat = {
    'entry_id':request.json['entry_id'],
    'title':request.json['title'],
    'body':request.json['body']
    }
    entryDB.append(dat)
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    r = request.post(url, data=json.dumps(data), headers=headers)

    return jsonify(dat, {'message': 'Entry created.'}), 201

@app.route('/api/v1/entries/<int:entry_id>',methods=['PUT'])
def updateEntry(entry_id):

    em = [ entry for entry in entryDB if (entry['entry_id'] == entry_id) ]
    if 'title' in request.json : 
        em[0]['title'] = request.json['title']
    if 'body' in request.json:
        em[0]['body'] = request.json['body']

    return jsonify({'entry':em[0], 'message': 'Entry updated.'}), 204

@app.route('/api/v1/entries/<int:entry_id>',methods=['DELETE'])
def deleteEntry(entry_id):

    em = [ entry for entry in entryDB if (entry['entry_id'] == entry_id) ]
    if len(em) == 0:
       abort(404)
    entryDB.remove(em[0])

    return jsonify({'response':'Success', 'message': 'Entry deleted.'}), 202