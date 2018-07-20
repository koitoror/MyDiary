"""
import uuid
from versions import db
from passlib.hash import sha256_crypt

class User(db.Model):
    """Create table users
    One-to-Many relationship with Entries and entries
    User has many Entries
    User has many Entries
    delete-orphan to delete any attached child
    """
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    
    fullname = db.Column(db.String(), nullable=False)
    username = db.Column(db.String(), unique=True, nullable=False)
    email = db.Column(db.String(), unique=True, nullable=False)
    password = db.Column(db.String(), nullable=False)
    hash_key = db.Column(db.String(), unique=True, nullable=False)
    activate = db.Column(db.String(), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime,default=db.func.current_timestamp(),onupdate=db.func.current_timestamp())
    entries = db.relationship(
        'entries',
        backref='owner',
        cascade='all, delete-orphan'
    )
    Entries = db.relationship(
        'Entries',
        backref='owner',
        cascade='all, delete-orphan'
    )
    notifications = db.relationship(
        'Notification',
        backref='recipient',
        cascade='all, delete-orphan'
    )

    def __init__(self, username, fullname, email, password):
        """Sets defaults for creating user instance
        sets username and email to lower case
        encrypts password
        generates a random hash key
        sets activate to false, this will be changed later
        """
        self.username = username.lower().strip()
        self.fullname = fullname
        self.email = email.lower().strip()
        self.password = sha256_crypt.encrypt(str(password))
        self.hash_key = uuid.uuid1().hex
        self.activate = False

    def save(self):
        """Commits user instance to the database"""
        db.session.add(self)
        db.session.commit()


class Entries(db.Model):
    """Create table Entries
    One-to-Many relationship with user and entries
    Entry belongs to entries
    Entry belongs to user
    """
    __tablename__ = 'Entries'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String())
    desc = db.Column(db.String())
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(
        db.DateTime,
        default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp()
    )
    entryId = db.Column(
        db.Integer,
        db.ForeignKey('entries.id'),
        nullable=False
    )

    def __init__(self, title, desc, entries, Entrieser):
        self.title = title
        self.desc = desc
        self.entries = entries
        self.Entrieser = Entrieser

    def save(self):
        """Save a Entries to the database"""
        db.session.add(self)
        db.session.commit()

    def delete(self):
        """Delete a given Entries."""
        db.session.delete(self)
        db.session.commit()


class Notification(db.Model):
    """Handles notifications when user Entries on a entries"""
    __tablename__ = 'notifications'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    recipient_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    actor = db.Column(db.String(), nullable=False)
    entryId = db.Column(db.Integer, nullable=False)
    entryId = db.Column(db.Integer, nullable=False)
    action = db.Column(db.String(), nullable=False)
    read_at = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

    def __init__(self, recipient, actor, entryId, entryId, read_at=None):
        self.recipient = recipient
        self.actor = actor
        self.entryId = entryId
        self.entryId = entryId
        self.read_at = read_at
        self.action = ' has entered your entries'

    def save(self):
        """Save a Entries to the database"""
        db.session.add(self)
        db.session.commit()
"""    