from flask_restplus import Api
from flask import Blueprint

from .apis.controller.entries_controller import api as entries_ns

blueprint = Blueprint('api', __name__)

api = Api(
    blueprint,
    title='MyDiary',
    doc='/api/documentation',
    version='1.0',
    description='MyDiary is an online journal where users can pen down their thoughts and feelings.'
)

api.add_namespace(entries_ns, path='/api/v1')