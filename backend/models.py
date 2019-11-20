import os
from sqlalchemy import Column, String, Integer, create_engine, UniqueConstraint
from flask_sqlalchemy import SQLAlchemy
from flask import jsonify
import json
import logging
logging.basicConfig(level=logging.DEBUG)

database_name = "skillx"
database_path = "postgres://{}:{}@{}/{}".format('udacity', 'udacity', 'localhost:5432', database_name)

db = SQLAlchemy()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''
def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()

'''
mem_skills_held - many-to-many table
'''

mem_skills_held = db.Table('mem_skills_held',
    db.Column('member_id', db.Integer, db.ForeignKey('members.id'), primary_key=True),
    db.Column('skill_id', db.Integer, db.ForeignKey('skills.id'), primary_key=True)
)

'''
mem_skills_wanted - many-to-many table
'''

mem_skills_wanted = db.Table('mem_skills_wanted',
    db.Column('member_id', db.Integer, db.ForeignKey('members.id'), primary_key=True),
    db.Column('skill_id', db.Integer, db.ForeignKey('skills.id'), primary_key=True)
)

'''
Members
'''
class Member(db.Model):
    __tablename__ = 'members'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    location = db.Column(db.String, nullable=False)
    gender = db.Column(db.String(10), nullable=False) # M/F/Neither/Unspecified
    match_location = db.Column(db.Boolean, nullable=False)
    match_gender = db.Column(db.Boolean, nullable=False)
    user_id = db.Column(db.String, nullable=False)
    skills_held = db.relationship('Skill', secondary=mem_skills_held,
        backref=db.backref('members_held', lazy=True))
    skills_wanted = db.relationship('Skill', secondary=mem_skills_wanted,
        backref=db.backref('members_wanted', lazy=True))

    __table_args__ = (UniqueConstraint('name', 'location', 'gender', name='_m_name_loc_gen_uc'),)

    def __init__(self, name, location, gender, match_location, match_gender, user_id, skills_held, skills_wanted):

        self.name = name
        self.location = location
        self.gender = gender
        self.match_location = match_location
        self.match_gender = match_gender
        self.user_id = user_id

        # construct a list to hold all the skills held - as objects
        skillsh = []
        for skill in skills_held:
            skillsh.append(Skill.query.filter(Skill.name==skills_held).one_or_none())
        self.skills_held = skillsh

        # construct a list to hold all the skills wanted - as objects
        skillsw = []
        for skill in skills_wanted:
            skillsw.append(Skill.query.filter(Skill.name==skills_wanted).one_or_none())
        self.skills_wanted = skillsw

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        skills_held = []
        member_match_a = []
        for skill in self.skills_held:
            skills_held.append(skill.name)

            for mem in Member.query.all():
                logging.debug('mem.skills_wanted')
                logging.debug(mem.skills_wanted)
                # logging.debug('skill.id')
                # logging.debug(skill.id)
                # member_match_a.append(mem.query.filter(Skill.id.in_(mem.skills_wanted)))
                # logging.debug(member_match_a)



        skills_wanted = []
        for skill in self.skills_wanted:
            skills_wanted.append(skill.name)

        return {
          'id': self.id,
          'name': self.name,
          'location': self.location,
          'gender': self.gender,
          'match_location': self.match_location,
          'match_gender': self.match_gender,
          'user_id': self.user_id,
          'skills_held': skills_held,
          'skills_wanted': skills_wanted
        }

'''
Skills

'''
class Skill(db.Model):
    __tablename__ = 'skills'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.String)
    mental_physical = db.Column(db.String(10))
    equipment_reqd = db.Column(db.String)

    __table_args__ = (UniqueConstraint('name', name='_sk_name_uc'),)

    def __init__(self, name, description='', mental_physical='', equipment_reqd=''):
        self.name = name
        self.description = description
        self.mental_physical = mental_physical
        self.equipment_reqd = equipment_reqd

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
          'id': self.id,
          'name': self.name,
          'description': self.description,
          'mental_physical': self.mental_physical,
          'equipment_reqd': self.equipment_reqd
        }
