import os
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy import *
from sqlalchemy.orm import *
from sqlalchemy.ext.declarative import declarative_base
from flask_sqlalchemy import SQLAlchemy
from flask import jsonify
import json
import logging
import psycopg2
from dotenv import load_dotenv

# load_dotenv('.env') # enable if running locally / disable for deployment to heroku

logging.basicConfig(level=logging.DEBUG)

database_path = os.environ.get('DATABASE_URL')

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
    db.Column('member_id', db.Integer, db.ForeignKey('members.id', ondelete='cascade'), primary_key=True),
    db.Column('skill_id', db.Integer, db.ForeignKey('skills.id', ondelete='cascade'), primary_key=True)
)

'''
mem_skills_wanted - many-to-many table
'''

mem_skills_wanted = db.Table('mem_skills_wanted',
    db.Column('member_id', db.Integer, db.ForeignKey('members.id', ondelete='cascade'), primary_key=True),
    db.Column('skill_id', db.Integer, db.ForeignKey('skills.id', ondelete='cascade'), primary_key=True)
)

'''
Members
'''
class Member(db.Model):
    __tablename__ = 'members'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    location = db.Column(db.String, nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    match_location = db.Column(db.Boolean, nullable=False)
    user_id = db.Column(db.String, nullable=False, unique=True)
    skills_held = db.relationship('Skill', secondary=mem_skills_held,
        backref=db.backref('members_held', lazy=True))
    skills_wanted = db.relationship('Skill', secondary=mem_skills_wanted,
        backref=db.backref('members_wanted', lazy=True))

    # construct a list of skill objects
    def construct_skills_obj_list(self, skills):
        skills_list = []
        for sk in skills:
            skills_list.append(Skill.query.filter(Skill.name==sk).one_or_none())
        return skills_list

    def __init__(self, name, location, gender, match_location, user_id, skills_held, skills_wanted):
        self.name = name
        self.location = location
        self.gender = gender
        self.match_location = match_location
        self.user_id = user_id
        self.skills_held = self.construct_skills_obj_list(skills_held)
        self.skills_wanted = self.construct_skills_obj_list(skills_wanted)

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


# Set of methods utilzed for retrieving skills and matching skills / members
    def retrieve_members(self):
        if self.match_location is True:
            members = Member.query.filter(Member.id!=self.id, Member.location==self.location).all()
        else:
            # takes into account other members' choice of matching on location
            members = Member.query.filter(Member.id!=self.id).filter(((Member.match_location.is_(False))&(Member.location==self.location))|(Member.match_location.is_(False))).all()
        return members

    def find_member_skills_held_matches(self, skill, mem_match=[]):
        # for mem in Member.query.filter(Member.id!=self.id).all():
        members = self.retrieve_members()
        for mem in members:
            # locate list of skills wanted for each member in list
            for memskill in mem.skills_wanted:
                # if the skill held matches a wanted skill
                if skill.id == memskill.id:
                    # add member details to mem_match list
                    mem_match.append({
                        'skill_type': 'held',
                        'member_id': mem.id,
                        'skill_name': memskill.name
                    })
        # if there were any matches, return them
        if mem_match:
            return mem_match

    def find_member_skills_wanted_matches(self, skill, memlist, mem_match=[]):
        # for each member in members already matched by skills_held
        for mem in memlist:
            memobj = Member.query.filter(Member.id==mem.get('member_id')).one_or_none()
            # locate list of skills wanted for each member in list
            for memskill in memobj.skills_held:
                # if the skill held matches a wanted skill
                if skill.id == memskill.id:
                    # add member details to mem_match list
                    mem_match.append({
                        'skill_type': 'wanted',
                        'member_id': memobj.id,
                        'skill_name': memskill.name
                    })
        # if there were any matches, return them
        if mem_match:
            return mem_match

    def retrieve_matching_members(self, skills_held_match_list, skills_wanted_match_list):
        # create empty list for all matching member information
        matching_members = []
        # for each member which has both a matching skill held and wanted
        for memwanted in skills_wanted_match_list:
            # create empty lists for the held and wanted matching skills
            held_skills_list=[]
            wanted_skills_list = []
            # set variable for the member id for each member in the wanted skills list
            memwanted_id = memwanted.get('member_id')
            # add skill to the list of wanted skills held by other members
            wanted_skills_list.append(memwanted.get('skill_name'))
            # loop through the list of skills held that other members want
            for memheld in skills_held_match_list:
                # if there is also a skill wanted that is held by that member (matching memwanted_id)
                if memheld['member_id'] == memwanted_id:
                    # add the skill to the list of skills held that are wanted by another member
                    held_skills_list.append(memheld.get('skill_name'))
            # instantiate class for member details for matching members
            memdetails = Member.query.filter(Member.id==memwanted_id).one_or_none()
            # append matching member details to list for display
            matching_members.append({
                'id':memdetails.id,
                'name': memdetails.name,
                'location': memdetails.location,
                'gender': memdetails.gender,
                'skills_held_wanted': held_skills_list,
                'skills_wanted_held': wanted_skills_list
            })

        if matching_members:
            return matching_members
            # logging.debug(matching_members)

    # END OF METHODS USED FOR RETRIEVING MATCHING MEMBERS / SKILLS

    '''
    TODO - maybe create a short version for returning on successful POST
    '''
    def format(self):
        mem_held_match = []
        skills_held = []
        mem_wanted_match = []
        skills_wanted = []

        # for each skill held by member
        for skill in self.skills_held:
            # add name to skills_held list
            skills_held.append(skill.name)
            # find other members who want that skill and add them to a list
            skills_held_match_list = self.find_member_skills_held_matches(skill, mem_held_match)

        # for each skill wanted by the member
        for skill in self.skills_wanted:
            # add skill name to list
            skills_wanted.append(skill.name)
            # find other members who want that skill and add them to a list
            skills_wanted_match_list = self.find_member_skills_wanted_matches(skill, mem_held_match, mem_wanted_match)

        # in case of no skills being set for member (shouldn't occur) set skills_wanted_match_list to empty list
        if (not self.skills_held) or (not self.skills_wanted):
            skills_wanted_match_list = []
        # if no skills matched with other members, return empty list for passing to requestor
        if not skills_wanted_match_list:
            member_matches = []
        else:
            member_matches = self.retrieve_matching_members(skills_held_match_list, skills_wanted_match_list)

        return {
          'id': self.id,
          'name': self.name,
          'location': self.location,
          'gender': self.gender,
          'match_location': self.match_location,
          # 'match_gender': self.match_gender,
          # 'user_id': self.user_id,
          'skills_held': skills_held,
          'skills_wanted': skills_wanted,
          'matching_members': member_matches
        }

'''
Skills

'''
class Skill(db.Model):
    __tablename__ = 'skills'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.String)
    category = db.Column(db.String(20))
    equipment_reqd = db.Column(db.String)

    __table_args__ = (UniqueConstraint('name', name='_sk_name_uc'),)

    def __init__(self, name, description='', category='', equipment_reqd=''):
        self.name = name
        self.description = description
        self.category = category
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
          'category': self.category,
          'equipment_reqd': self.equipment_reqd
        }
