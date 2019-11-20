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


def retrieve_user(token):
    # retrieve user_id from the token
    token_sub = token['sub'].split('|')
    user_id = token_sub[1]
    if user_id is None:
        # TODO Change the HTTP error to match more closely the issue
        abort(404)

    return user_id

# '''
# @TODO uncomment the following line to initialize the datbase
# !! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
# !! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
# '''
# # db_drop_and_create_all()
#
# ## ROUTES
#
@app.route('/profile')
@requires_auth('read:profile')
def retrieve_profile(token):
    user_id = retrieve_user(token)
    # user_id = '5dd3f12f09cdf00efd979aac'  # bjorn

    # use user_id to get relevant user profile information
    member = Member.query.filter(Member.user_id==user_id).one_or_none()
    if member is None:
        abort(404)

    profile = member.format()

    if profile is None:
        abort(404)

    return jsonify({
        'success': True,
        'member': profile
    })


@app.route('/profile', methods=['POST'])
@requires_auth('post:profile')
def create_profile(token):
    new_user_id = retrieve_user(token)
    new_name = request.json.get('name', None)
    new_location = request.json.get('location', None)
    new_gender = request.json.get('gender', None)
    new_match_gender = request.json.get('match_gender', None)
    new_match_location = request.json.get('match_location', None)
    new_skills_held = request.json.get('skills_held', None)
    new_skills_wanted = request.json.get('skills_wanted', None)

    new_profile = Member(
        name=new_name,
        location=new_location,
        gender=new_gender,
        match_gender=new_match_gender,
        match_location=new_match_location,
        user_id=new_user_id,
        skills_held=new_skills_held,
        skills_wanted=new_skills_wanted
    )
    try:
        new_profile.insert()
    except:
        abort(422)

    return 'test success'


          # recipe=json.dumps(new_recipe))
    #         try:
    #             new_drink.insert()
    #         except:
    #             abort(422)
    #


    # if profile is None:
    #     abort(404)
    #
    # return jsonify({
    #     'success': True,
    #     'member': profile
    # })


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
# @app.route('/drinks', methods=['POST'])
# @requires_auth('post:drinks')
# def add_new_drink(token):
#     new_title = request.json.get('title', None)
#     new_recipe = request.json.get('recipe', None)
#
#     # if missing info needed to create drink then abort 400
#     if (new_title is None) or (new_recipe is None):
#         abort(400)
#     # else attempt insert data into db
#     else:
#         # json.dumps used to convert recipe to string for entry into db
#         new_drink = Drink(title=new_title, recipe=json.dumps(new_recipe))
#         try:
#             new_drink.insert()
#         except:
#             abort(422)
#
#     # locate id of newly created drink (json.dumps used to read string from db)
#     created_drink = Drink.query.filter(Drink.title==new_title, Drink.recipe==json.dumps(new_recipe)).one_or_none()
#
#     if created_drink is None:
#         abort(404)
#     else:
#         return jsonify({
#             'success': True,
#             'drinks': created_drink.long()
#         })
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
# @app.route('/drinks/<int:id>', methods=['DELETE'])
# @requires_auth('delete:drinks')
# def delete_existing_drink(token, id):
#     # locate drink to be deleted
#     del_drink = Drink.query.filter(Drink.id == id).one_or_none()
#     # if no match found - abort 404
#     if del_drink is None:
#         print ('ID not found')
#         abort(404)
#     else:
#         try:
#             del_drink.delete()
#         except:
#             abort(422)
#
#     return jsonify({
#         'success': True,
#         'delete': id
#     })


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
