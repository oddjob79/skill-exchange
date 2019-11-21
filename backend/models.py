import os
# from sqlalchemy import Column, String, Integer, create_engine, UniqueConstraint
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy import *
from sqlalchemy.orm import *
from sqlalchemy.ext.declarative import declarative_base
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
TODO - Change Unique Constraint to user_id
TODO - Remove match gender
'''
class Member(db.Model):
    __tablename__ = 'members'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    location = db.Column(db.String, nullable=False)
    gender = db.Column(db.String(10), nullable=False) # M/F/Neither/Unspecified
    match_location = db.Column(db.Boolean, nullable=False)
    # match_gender = db.Column(db.Boolean, nullable=False)
    user_id = db.Column(db.String, nullable=False, unique=True)
    skills_held = db.relationship('Skill', secondary=mem_skills_held,
        backref=db.backref('members_held', lazy=True))
    skills_wanted = db.relationship('Skill', secondary=mem_skills_wanted,
        backref=db.backref('members_wanted', lazy=True))

    # __table_args__ = (UniqueConstraint('name', 'location', 'gender', name='_m_name_loc_gen_uc'),)

    # def __init__(self, name, location, gender, match_location, match_gender, user_id, skills_held, skills_wanted):
    def __init__(self, name, location, gender, match_location, user_id, skills_held, skills_wanted):

        self.name = name
        self.location = location
        self.gender = gender
        self.match_location = match_location
        # self.match_gender = match_gender
        self.user_id = user_id

        # construct a list of objects to hold all the skills held
        skillsh = []
        for sk in skills_held:
            skillsh.append(Skill.query.filter(Skill.name==sk).one_or_none())
        self.skills_held = skillsh

        # construct a list of objects to hold all the skills wanted
        skillsw = []
        for sk in skills_wanted:
            skillsw.append(Skill.query.filter(Skill.name==sk).one_or_none())
        self.skills_wanted = skillsw

    # def build_skills_list(skills):
    #     skills_list = []
    #     for skl in skills:
    #         skills_list.append(Skill.query.filter(Skill.name==skl).one_or_none())
    #     return skills_list

    def insert(self):
        # self.skills_held = build_skills_list(self.skills_held)
        # self.skills_wanted = build_skills_list(self.skills_wanted)

        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def retrieve_members(self):
        if self.match_location is True:
            members = Member.query.filter(Member.id!=self.id, Member.location==self.location).all()
        else:
            # takes into account other members' choice of matching on location
            members = Member.query.filter(Member.id!=self.id).filter(((Member.match_location.is_(False))&(Member.location==self.location))|(Member.match_location.is_(False))).all()
        return members

    def find_member_skills_held_matches(self, skill, mem_match=[]):
        # for each member in db aside from member
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

    def format(self):
        # define empty dictionary for members who have a wanted skill which matched a skill held by the current member
        mem_held_match = []
        # define empty list for skills held by member
        skills_held = []
        # for each skill held by member
        for skill in self.skills_held:
            # add name to skills_held list
            skills_held.append(skill.name)
            # find other members who want that skill and add them to a list
            skills_held_match_list = self.find_member_skills_held_matches(skill, mem_held_match)
            # logging.debug('skills_held_match_list')
            # logging.debug(skills_held_match_list)

        # define empty dictionary for members who have a held skill which matched a skill wanted by the current member
        mem_wanted_match = []
        # define empty list for skills wanted by the member
        skills_wanted = []
        # for each skill wanted by the member
        for skill in self.skills_wanted:
            # add skill name to list
            skills_wanted.append(skill.name)
            # find other members who want that skill and add them to a list
            skills_wanted_match_list = self.find_member_skills_wanted_matches(skill, mem_held_match, mem_wanted_match)
            # logging.debug(skills_wanted_match_list)

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
            # logging.debug(matching_members)



        return {
          'id': self.id,
          'name': self.name,
          'location': self.location,
          'gender': self.gender,
          'match_location': self.match_location,
          # 'match_gender': self.match_gender,
          'user_id': self.user_id,
          'skills_held': skills_held,
          'skills_wanted': skills_wanted,
          'matching_members': matching_members
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
