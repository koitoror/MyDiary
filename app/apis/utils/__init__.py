"""Main API Entry Point"""

from flask_restplus import Api

# initializing the api
api = Api(
    version='1.0',
    title='MyDiary',
    description='MyDiary is an online journal where users can pen down their thoughts and feelings.',
    doc='/api/documentation'
)
