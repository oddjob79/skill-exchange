import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
import logging
from flask_cors import CORS
from models import setup_db, Member, Skill
from auth import AuthError, requires_auth, get_token_auth_header

logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)
setup_db(app)
CORS(app)

# Method to retrieve the user_id from the token`
def retrieve_user(token):
    # retrieve user_id from the token
    token_sub = token['sub'].split('|')
    user_id = token_sub[1]
    if user_id is None:
        # TODO Change the HTTP error to match more closely the issue
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


# '''
# @TODO uncomment the following line to initialize the datbase
# !! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
# !! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
# '''
# # db_drop_and_create_all()
#
# ## ROUTES
#

# GET OWN PROFILE
@app.route('/profile')
@requires_auth('read:profile')
def retrieve_own_profile(token):
    user_id = retrieve_user(token)
    # user_id = '5dd3f12f09cdf00efd979aac'  # bjorn
    return retrieve_profile(user_id)

# GET MEMBER PROFILE
@app.route('/member/<int:id>')
@requires_auth('read:member')
def retrieve_member_profile(token, id):
    mem = Member.query.get(id)
    if mem:
        return retrieve_profile(mem.user_id)
    else:
        abort(404)

# GET MEMBER LIST
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
    if members:
        return jsonify({
            'success': True,
            'members': mem_list
        })
    else:
        abort(401)

# GET SKILL LIST
@app.route('/skills')
@requires_auth('read:skills')
def retrieve_skill_list(token):
    skills = Skill.query.order_by(Skill.id).all()
    skill_list = []
    for skill in skills:
        skill_list.append(
            skill.format()
        )
    if skills:
        return jsonify({
            'success': True,
            'skills': skill_list
        })
    else:
        abort(401)

# GET INDIVIDUAL SKILL INFO
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

# POST PROFILE
@app.route('/profile', methods=['POST'])
@requires_auth('post:profile')
def create_profile(token):
    new_user_id = retrieve_user(token)
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


# POST SKILL
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


# DELETE PROFILE - from user
@app.route('/profile', methods=['DELETE'])
@requires_auth('delete:profile')
def delete_own_profile(token):
    # retrieve user_id from token
    user_id = retrieve_user(token)
    # use method to delete profile
    return delete_profile(user_id)


# DELETE MEMBER PROFILE - from admin
@app.route('/member/<int:id>', methods=['DELETE'])
@requires_auth('delete:member')
def delete_member_profile(token, id):
    mem = Member.query.get(id)
    if mem:
        return delete_profile(mem.user_id)
    else:
        abort(404)


# DELETE SKILL
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


# PATCH PROFILE

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





#
# # '''
# # @TODO implement endpoint
# #     GET /drinks-detail
# #         it should require the 'get:drinks-detail' permission
# #         it should contain the drink.long() data representation
# #     returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
# #         or appropriate status code indicating reason for failure
# # '''
# @app.route('/drinks-detail')
# @requires_auth('get:drinks-detail')
# def retrieve_drink_details(token):
#     drinks = Drink.query.all()
#     if drinks is None:
#         abort(404)
#
#     long_drinks = [dr.long() for dr in drinks]
#     if long_drinks is None:
#         print('unable to get short_drinks')
#         abort(404)
#
#     return jsonify({
#         'success': True,
#         'drinks': long_drinks
#     })
#
#
#
# # '''
# # @TODO implement endpoint
# #     POST /drinks
# #         it should create a new row in the drinks table
# #         it should require the 'post:drinks' permission
# #         it should contain the drink.long() data representation
# #     returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the newly created drink
# #         or appropriate status code indicating reason for failure
# # '''
#
#
#
#
# # '''
# # @TODO implement endpoint
# #     PATCH /drinks/<id>
# #         where <id> is the existing model id
# #         it should respond with a 404 error if <id> is not found
# #         it should update the corresponding row for <id>
# #         it should require the 'patch:drinks' permission
# #         it should contain the drink.long() data representation
# #     returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the updated drink
# #         or appropriate status code indicating reason for failure
# # '''
#
# @app.route('/drinks/<int:id>', methods=['PATCH'])
# @requires_auth('patch:drinks')
# def edit_existing_drink(token, id):
#     # Retreieve updated data from form
#     upd_title = request.json.get('title', None)
#     upd_recipe = request.json.get('recipe', None)
#
#     # if no new details sent, then abort 400
#     if (upd_title is None) and (upd_recipe is None):
#         abort(400)
#     # else attempt update
#     else:
#         # locate drink to be updated
#         upd_drink = Drink.query.filter(Drink.id == id).one_or_none()
#         # if no match found - abort 404
#         if upd_drink is None:
#             print ('ID not found')
#             abort(404)
#         else:
#             if upd_title is not None:
#                 upd_drink.title = upd_title
#             if upd_recipe is not None:
#                 # json.dumps used to convert recipe to string for entry into db
#                 upd_drink.recipe = json.dumps(upd_recipe)
#             try:
#                 upd_drink.update()
#             except:
#                 abort(422)
#
#         # build array for return to requestor
#         upd_drink_arr = []
#         upd_drink_arr.extend((upd_drink.title, upd_drink.recipe))
#
#     return jsonify({
#         'success': True,
#         'drinks': upd_drink_arr
#     })
#
#
# # '''
# # @TODO implement endpoint
# #     DELETE /drinks/<id>
# #         where <id> is the existing model id
# #         it should respond with a 404 error if <id> is not found
# #         it should delete the corresponding row for <id>
# #         it should require the 'delete:drinks' permission
# #     returns status code 200 and json {"success": True, "delete": id} where id is the id of the deleted record
# #         or appropriate status code indicating reason for failure
# # '''
#


## Error Handling
'''
Example error handling for unprocessable entity
'''
@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": "unprocessable"
        }), 422

# '''
# @TODO implement error handlers using the @app.errorhandler(error) decorator
#     each error handler should return (with approprate messages):
#              jsonify({
#                     "success": False,
#                     "error": 404,
#                     "message": "resource not found"
#                     }), 404
#
# '''

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


# '''
# @TODO implement error handler for 404
#     error handler should conform to general task above
# '''


# '''
# @TODO implement error handler for AuthError
#     error handler should conform to general task above
# '''
# error handler found on Stack Overflow
@app.errorhandler(AuthError)
def handle_auth_error(ex):
    response = jsonify(ex.error)
    response.status_code = ex.status_code
    return response
