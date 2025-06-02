from .app_db import db

class AdminPage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    rooms = db.Column(db.Integer, default=1)

    songs_sessions = db.relationship('SongSession', backref='admin', cascade="all, delete")
    base_schedule = db.relationship('BaseSchedule', backref='admin', cascade="all, delete")
    session_weights = db.relationship('SessionWeight', backref='admin', cascade="all, delete")
    persons = db.relationship('PersonAvailability', backref='admin', cascade="all, delete")
    schedules = db.relationship('ScheduleParticipant', backref='admin', cascade="all, delete")


class SongSession(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    admin_id = db.Column(db.Integer, db.ForeignKey('admin_page.id'))
    song = db.Column(db.String, nullable=False)
    session = db.Column(db.String, nullable=False)
    name = db.Column(db.String, nullable=False)


class BaseSchedule(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    admin_id = db.Column(db.Integer, db.ForeignKey('admin_page.id'))
    datetime = db.Column(db.DateTime, nullable=False)


class SessionWeight(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    admin_id = db.Column(db.Integer, db.ForeignKey('admin_page.id'))
    session = db.Column(db.String, nullable=False)
    weight = db.Column(db.Integer, default=1)


class PersonAvailability(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    admin_id = db.Column(db.Integer, db.ForeignKey('admin_page.id'))
    name = db.Column(db.String, nullable=False)

    times = db.relationship('AvailableTime', backref='person', cascade="all, delete")


class AvailableTime(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    person_id = db.Column(db.Integer, db.ForeignKey('person_availability.id'))
    datetime = db.Column(db.DateTime, nullable=False)


class ScheduleParticipant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    admin_id = db.Column(db.Integer, db.ForeignKey('admin_page.id'))
    datetime = db.Column(db.DateTime, nullable=False)
    song = db.Column(db.String, nullable=False)
    participants = db.Column(db.ARRAY(db.String), default=[])
    absentees = db.Column(db.ARRAY(db.String), default=[])
