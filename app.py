import os
from flask import Flask, request, jsonify, abort, render_template
from sqlalchemy import exc
import json
import logging
from flask_cors import CORS
from models import setup_db, Member, Skill
from auth import AuthError, requires_auth, get_token_auth_header

logging.basicConfig(level=logging.DEBUG)

# app = Flask(__name__)

# Method to retrieve the user_id from the token`
def retrieve_user(token):
    # retrieve user_id from the token
    token_sub = token['sub'].split('|')
    user_id = token_sub[1]
    if user_id is None:
        abort(404)

    return user_id

def retrieve_profile(user_id):
    # use user_id to get relevant user profile information
    member = Member.query.filter(Member.user_id==user_id).one_or_none()
    if member is None:
        abort(404)

    return jsonify({
        'success': True,
        'member': member.format()
    })


def delete_profile(user_id):
    profile = Member.query.filter(Member.user_id == user_id).one_or_none()
    # if no match found - abort 404
    if profile is None:
        abort(404)
    else:
        try:
            profile.delete()
        except:
            abort(422)

    return jsonify({
        'success': True,
        'delete': profile.id
    })



def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    cors = CORS(app, resources={r"/*": {"origins": "*"}})

    # CORS Headers
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PATCH,POST,DELETE,OPTIONS')
        return response


    #
    # ## ROUTES
    #
    @app.route('/')
    def index():
        return render_template('index.html')


    # GET OWN PROFILE - T
    @app.route('/profile')
    @requires_auth('read:profile')
    def retrieve_own_profile(token):
        user_id = retrieve_user(token)
        # user_id = '5dd3f12f09cdf00efd979aac'  # bjorn
        return retrieve_profile(user_id)

    # GET MEMBER PROFILE - T
    @app.route('/member/<int:id>')
    @requires_auth('read:member')
    def retrieve_member_profile(token, id):
        mem = Member.query.get(id)
        if mem:
            return retrieve_profile(mem.user_id)
        else:
            abort(404)

    # GET MEMBER LIST - T
    @app.route('/members')
    @requires_auth('read:member')
    def retrieve_member_list(token):
        members = Member.query.order_by(Member.id).all()
        mem_list = []
        for member in members:
            mem_list.append({
                'id': member.id,
                'name': member.name,
                'location': member.location,
                'gender': member.gender
            })
        if mem_list:
            return jsonify({
                'success': True,
                'members': mem_list
            })
        else:
            abort(422)

    # GET SKILL LIST - T
    @app.route('/skills')
    @requires_auth('read:skills')
    def retrieve_skill_list(token):
        skills = Skill.query.order_by(Skill.id).all()
        skill_list = []
        for skill in skills:
            skill_list.append(
                skill.format()
            )
        if skill_list:
            return jsonify({
                'success': True,
                'skills': skill_list
            })
        else:
            abort(422)

    # GET INDIVIDUAL SKILL INFO - T
    @app.route('/skill/<int:id>')
    @requires_auth('read:skills')
    def retrieve_skill(token, id):
        skill = Skill.query.get(id)
        if skill:
            return jsonify({
                'success': True,
                'skill': skill.format()
            })
        else:
            abort(404)

    # POST PROFILE - T
    @app.route('/profile', methods=['POST'])
    @requires_auth('post:profile')
    def create_profile(token):
        new_user_id = retrieve_user(token)

        # Check if member already exists
        if Member.query.filter(Member.user_id==new_user_id).one_or_none():
            abort(422)
        else:
            new_name = request.json.get('name', None)
            new_location = request.json.get('location', None)
            new_gender = request.json.get('gender', None)
            new_match_location = request.json.get('match_location', None)
            new_skills_held = request.json.get('skills_held', None)
            new_skills_wanted = request.json.get('skills_wanted', None)

            new_profile = Member(
                name=new_name,
                location=new_location,
                gender=new_gender,
                match_location=new_match_location,
                user_id=new_user_id,
                skills_held=new_skills_held,
                skills_wanted=new_skills_wanted
            )
            try:
                new_profile.insert()
            except:
                abort(422)

            if new_user_id:
                return retrieve_profile(new_user_id)
            else:
                abort(404)


    # POST SKILL - T
    @app.route('/skill', methods=['POST'])
    @requires_auth('post:skills')
    def create_skill(token):
        new_name = request.json.get('name', None)
        new_description = request.json.get('description', None)
        new_category = request.json.get('category', None)
        new_equipment_reqd = request.json.get('equipment_reqd', None)

        new_skill = Skill(
            name=new_name,
            description=new_description,
            category=new_category,
            equipment_reqd=new_equipment_reqd
        )
        try:
            new_skill.insert()
        except:
            abort(422)

        skill_added = Skill.query.filter(Skill.name==new_name).one_or_none()

        if skill_added:
            return jsonify({
                'success': True,
                'skill': skill_added.format()
            })
        else:
            abort(404)


    # DELETE PROFILE - from user - T
    @app.route('/profile', methods=['DELETE'])
    @requires_auth('delete:profile')
    def delete_own_profile(token):
        # retrieve user_id from token
        user_id = retrieve_user(token)
        # use method to delete profile
        return delete_profile(user_id)


    # DELETE MEMBER PROFILE - from admin - T
    @app.route('/member/<int:id>', methods=['DELETE'])
    @requires_auth('delete:member')
    def delete_member_profile(token, id):
        mem = Member.query.get(id)
        if mem:
            return delete_profile(mem.user_id)
        else:
            abort(404)


    # DELETE SKILL - T
    @app.route('/skill/<int:id>', methods=['DELETE'])
    @requires_auth('delete:skills')
    def delete_skill(token, id):
        skill = Skill.query.get(id)
        # if no match found - abort 404
        if skill is None:
            abort(404)
        else:
            try:
                skill.delete()
            except:
                abort(422)

        return jsonify({
            'success': True,
            'delete': id
        })


    # PATCH PROFILE - T
    @app.route('/profile', methods=['PATCH'])
    @requires_auth('patch:profile')
    def edit_own_profile(token):
        upd_user_id = retrieve_user(token)
        upd_name = request.json.get('name', None)
        upd_location = request.json.get('location', None)
        upd_gender = request.json.get('gender', None)
        upd_match_location = request.json.get('match_location', None)
        upd_skills_held = request.json.get('skills_held', None)
        upd_skills_wanted = request.json.get('skills_wanted', None)

        # if no new details sent, then abort 400
        if (upd_name is None) and (upd_location is None) and (upd_gender is None) and (upd_match_location is None) and (upd_skills_held is None) and (upd_skills_wanted is None):
            abort(400)
        # else attempt update
        else:
            # locate profile to be updated
            upd_profile = Member.query.filter(Member.user_id == upd_user_id).one_or_none()
            # if no match found - abort 404 - not sure if will be used
            if upd_profile is None:
                print ('User ID not found')
                abort(404)
            else:
                if upd_name is not None:
                    upd_profile.name = upd_name
                if upd_location is not None:
                    upd_profile.location = upd_location
                if upd_gender is not None:
                    upd_profile.gender = upd_gender
                if upd_match_location is not None:
                    upd_profile.match_location = upd_match_location
                if upd_skills_held is not None:
                    # clear out existing skills held
                    upd_profile.skills_held.clear()
                    # use method to build a list of skills objects to re-add
                    upd_profile.skills_held = Member.construct_skills_obj_list(upd_profile, upd_skills_held)
                if upd_skills_wanted is not None:
                    # clear out existing skills held
                    upd_profile.skills_wanted.clear()
                    # use method to build a list of skills objects to re-add
                    upd_profile.skills_wanted = Member.construct_skills_obj_list(upd_profile, upd_skills_wanted)
                try:
                    upd_profile.update()
                except:
                    abort(422)

        return jsonify({
            'success': True,
            'profile': upd_profile.format()
        })

    # PATCH SKILL - T
    @app.route('/skill/<int:id>', methods=['PATCH'])
    @requires_auth('patch:skills')
    def edit_skill(token, id):
        upd_name = request.json.get('name', None)
        upd_description = request.json.get('description', None)
        upd_category = request.json.get('category', None)
        upd_equipment_reqd = request.json.get('equipment_reqd', None)

        # if no new details sent, then abort 400
        if (upd_name is None) and (upd_description is None) and (upd_category is None) and (upd_equipment_reqd is None):
            abort(400)
        # else attempt update
        else:
            # locate profile to be updated
            upd_skill = Skill.query.get(id)
            # if no match found - abort 404 - not sure if will be used
            if upd_skill is None:
                print ('Skill ID not found')
                abort(404)
            else:
                if upd_name is not None:
                    upd_skill.name = upd_name
                if upd_description is not None:
                    upd_skill.description = upd_description
                if upd_category is not None:
                    upd_skill.category = upd_category
                if upd_equipment_reqd is not None:
                    upd_skill.equipment_reqd = upd_equipment_reqd
                try:
                    upd_skill.update()
                except:
                    abort(422)

        return jsonify({
            'success': True,
            'skill': upd_skill.format()
        })


    ## Error Handling
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "Unable to process the request due to invalid data. Please reformat the request and resubmit."
        }), 400

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "The requested resource could not be found."
        }), 404

    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({
            "success": False,
            "error": 405,
            "message": "Method not allowed - please use an appropriate method with your request, or add a resource."
        }), 405

    @app.errorhandler(422)
    def unprocessable_entity(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "The request was valid, but there was an issue during processing. Data may be out of range. Please consult the documentation and resubmit."
        }), 422

    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify({
            "success": False,
            "error": 500,
            "message": "Internal Server Error. We don't quite know what happened here. Please consult the documentation to ensure your request is correctly formatted."
        }), 500


    # error handler found on Stack Overflow
    @app.errorhandler(AuthError)
    def handle_auth_error(ex):
        response = jsonify(ex.error)
        response.status_code = ex.status_code
        return response

    return app
