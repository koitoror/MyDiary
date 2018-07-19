"""Modulizing the app
Split the routes into modules i.e User, Entries, Review

object `app` is created here so that each module can import it safely
and the __name__ variable will resolve to the correct package.

Its important to import the modules after the application object is created.

Why do this; it reduces lines of code within a single file
and its an easy read
"""
import os
from flask import Flask, request, jsonify
from flask_cors import CORS



app = Flask(__name__)
app.config.from_object('config.{}'.format(os.getenv('ENVIRON')))
CORS(app)


import versions.routes
import versions.v1.entries
import versions.v1.notifications

# version 1 routes

app.register_blueprint(
    versions.v1.entries.mod, url_prefix='/api/v1/entries')
app.register_blueprint(
    versions.v1.notifications.mod, url_prefix='/api/v1/notifications')
