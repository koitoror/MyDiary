import os


class Development(Config):
    """Sets Debug mode in Development to True"""
    DEBUG = True


class Testing(Config):
    """Testing environment"""
    DEBUG = True
    TESTING = True
    #SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL_TEST')


class Production(Config):
    """Production environment"""
    DEBUG = False
    TESTING = False
    MAIL_SUPPRESS_SEND = False
