import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db, Member, Skill, db

USERTOKEN = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImtpZCI6Ik1qSTRRakkyTlRSQ09UaENPVGsyTVRjNFFqTkZOME14T1RKQlJFWTFNRGRCUWtVeE1FRTVSUSJ9.eyJpc3MiOiJodHRwczovL3NraWxsLWV4Y2hhbmdlLmV1LmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw1ZGQzZjBjN2EwNzJkMjBmMTJhMTFlMmEiLCJhdWQiOiJza2lsbHNleGNoYW5nZSIsImlhdCI6MTU3NDQzMjE1NywiZXhwIjoxNTc0NDM5MzU3LCJhenAiOiJSSkZ5MUpoRE9zOHpaaVlxQlBUa2xvQ0JYanA1RnlFYiIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOnByb2ZpbGUiLCJwYXRjaDpwcm9maWxlIiwicG9zdDpwcm9maWxlIiwicmVhZDpwcm9maWxlIiwicmVhZDpza2lsbHMiXX0.0wjJOxDkWTbKba6zibHYAfuJbavxORKzqKaMYd30mkV1fnTVtuWZbQF-ZdpcxJjDwu7J7B3gE1scuUZPhjyCFZP8vPLHaBSSNm49S7Q-LeZsMzOEl44Zll85qgHfClbppOm03iOuR3yJViEIxhWIbeQ9jTaLUFSGqr--x0DjRJRz2msobZqHZeSsWUhcIdJs4k210l0yI-qRLaGf7AVN4oM8KApAd-FRRSI-yin-5YqB-7DMc643G5dbCRLkd-5PnIQgCxMCNn5q6ClfPWEPNLOGh1s1MhXUbuh4AYDrY08oaGQ3skr0mfWw1dywgo9e-x9X8sC2TTnyd0_RbSr7Ew'
ADMINTOKEN = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImtpZCI6Ik1qSTRRakkyTlRSQ09UaENPVGsyTVRjNFFqTkZOME14T1RKQlJFWTFNRGRCUWtVeE1FRTVSUSJ9.eyJpc3MiOiJodHRwczovL3NraWxsLWV4Y2hhbmdlLmV1LmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw1ZGQzZjE3ZDNmOWMwZTBlZjkwNjAyNTEiLCJhdWQiOiJza2lsbHNleGNoYW5nZSIsImlhdCI6MTU3NDQzNTM4NywiZXhwIjoxNTc0NDQyNTg3LCJhenAiOiJSSkZ5MUpoRE9zOHpaaVlxQlBUa2xvQ0JYanA1RnlFYiIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOm1lbWJlciIsImRlbGV0ZTpza2lsbHMiLCJwYXRjaDpza2lsbHMiLCJwb3N0OnNraWxscyIsInJlYWQ6bWVtYmVyIiwicmVhZDpza2lsbHMiXX0.CSHB0KEqDSs9io_J0V-UNYR5EJ6ZcAoShVybY3hmZKbVJbU4Wy9vGd9k7RXmul-FciXB_qWVs1Trss01IZ3exhhFA4WDzGYnEainBtgqP1_ujVaZfhXaMK9rDWgBCHJLdxTDoDM2PNbSj58SJpgwv_5UPoAPchyV4Uyu3aw5cNqua1h7bc93CfCT6mj-R59s0HNi3LSri2_sdt2K3FE70HXCaHq4FlY3ygu2MSlbgA6VwAvWJ1KYj2vBfWkhlYOF7Lfmx0wLJfhrj6RgsVy2uauXH2_ttorBWsFY7AN7fOc9GL7uA7UrfAEDZY2-yT-gSk_HPNBFsfUgqKsT9FOo5A'

class SkillXTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "skillx_test"
        self.database_path = "postgres://{}:{}@{}/{}".format('udacity', 'udacity', 'localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # Manually set tokens - taken from Stack Overflow
        self.userheaders = {'Content-Type': 'application/json', 'Authorization': "Bearer " + USERTOKEN}
        self.adminheaders = {'Content-Type': 'application/json', 'Authorization': "Bearer " + ADMINTOKEN}

        # self.new_question = {
        #     'question': 'Why do birds suddenly appear, every time you are near?',
        #     'answer': 'Just like me, they long to be, close to you',
        #     'category': 5,
        #     'difficulty': 2
        # }

        self.new_profile_anni = {
            "name": "Anni",
            "location": "Sweden",
            "gender": "Female",
            "match_location": "False",
            "skills_held": ["English"],
            "skills_wanted": ["Spanish"]
        }

        self.new_skill_eng = {
        	"name": "English",
        	"description": "English language to native speaker level",
        	"category": "language",
        	"equipment_reqd": "none"
        }

        self.new_skill_esp = {
        	"name": "Spanish",
        	"description": "Spanish language to native speaker level",
        	"category": "language",
        	"equipment_reqd": "none"
        }

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        # db.drop_all()
        pass

# POST SKILL
    def test_create_skill_eng(self):
        res = self.client().post('/skill', headers=self.adminheaders, json=self.new_skill_eng)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['skill'])

    def test_create_skill_esp(self):
        res = self.client().post('/skill', headers=self.adminheaders, json=self.new_skill_esp)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['skill'])

# POST MEMBER PROFILE
    def test_create_profile(self):
        res = self.client().post('/profile', headers=self.userheaders, json=self.new_profile_anni)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['member'])


    # # GET OWN PROFILE
    # def test_retrieve_own_profile(self):
    #     # test request path
    #     res = self.client().get('/profile', headers=self.userheaders)
    #     # load the data received from the response
    #     data = json.loads(res.data)
    #
    #     self.assertEqual(res.status_code, 200) # Check the response is 200 response
    #     self.assertEqual(data['success'], True) # Check json success = true
    #     self.assertTrue(data['member']) # Check meber is populated

# # GET ALL QUESTIONS
#     def test_retrieve_all_questions(self):
#         res = self.client().get('/questions')
#         data = json.loads(res.data)
#
#         self.assertEqual(res.status_code, 200) # Check the response is 200 response
#         self.assertEqual(data['success'], True) # Check json success = true
#         self.assertTrue(data['total_questions']) # Check total_questions var is populated
#         self.assertTrue(data['current_category']) # Check current_category var is populated
#         self.assertTrue(data['categories']) # Check categories var is populated
#
#     def test_404_sent_requesting_question_list(self):
#         res = self.client().get('/questions?page=77')
#         data = json.loads(res.data)
#
#         self.assertEqual(res.status_code, 404)
#         self.assertEqual(data['success'], False)
#         self.assertEqual(data['message'], 'The requested resource could not be found.')
#
# # POST QUESTIONS
#     def test_create_question(self):
#         res = self.client().post('/questions', json=self.new_question)
#         data = json.loads(res.data)
#
#         self.assertEqual(res.status_code, 200)
#         self.assertEqual(data['success'], True)
#         self.assertTrue(data['created'])
#         self.assertTrue(len(data['questions']))
#         self.assertTrue(data['total_questions'])
#
#     def test_400_sent_create_question_missing_data(self):
#         res = self.client().post('/questions', json=self.new_question_missing_data)
#         data = json.loads(res.data)
#
#         self.assertEqual(res.status_code, 400)
#         self.assertEqual(data['success'], False)
#         self.assertEqual(data['message'], 'Unable to process the request due to invalid data. Please reformat the request and resubmit.')
#
#     def test_422_sent_unable_to_insert_question(self):
#         res = self.client().post('/questions', json=self.new_question_data_out_of_range)
#         data = json.loads(res.data)
#
#         self.assertEqual(res.status_code, 422)
#         self.assertEqual(data['success'], False)
#         self.assertEqual(data['message'], 'The request was valid, but there was an issue during processing. Data may be out of range. Please consult the documentation and resubmit.')
#
#     def test_404_sent_creating_new_question(self):
#         res = self.client().post('/questions?page=77', json=self.new_question)
#         data = json.loads(res.data)
#
#         self.assertEqual(res.status_code, 404)
#         self.assertEqual(data['success'], False)
#         self.assertEqual(data['message'], 'The requested resource could not be found.')
#
# # SEARCH QUESTIONS
#     def test_search_questions(self):
#         res = self.client().post('/questions', json=({'searchTerm': 'oCCe'}))
#         data = json.loads(res.data)
#
#         self.assertEqual(res.status_code, 200)
#         self.assertEqual(data['success'], True)
#         self.assertTrue(len(data['questions']))
#         self.assertTrue(data['total_questions'])
#
#     def test_404_no_search_results_found(self):
#         res = self.client().post('/questions', json=({'searchTerm': 'kerffuffelump'}))
#         data = json.loads(res.data)
#
#         self.assertEqual(res.status_code, 404)
#         self.assertEqual(data['success'], False)
#         self.assertEqual(data['message'], 'The requested resource could not be found.')
#
# # DELETE QUESTIONS
#     def test_delete_question(self):
#         res = self.client().delete('/questions/5')
#         data = json.loads(res.data)
#
#         self.assertEqual(res.status_code, 200)
#         self.assertEqual(data['success'], True)
#         self.assertTrue(len(data['questions']))
#         self.assertTrue(data['total_questions'])
#
#     def test_404_question_not_found(self):
#         res = self.client().delete('/questions/09879876')
#         data = json.loads(res.data)
#
#         self.assertEqual(res.status_code, 404)
#         self.assertEqual(data['success'], False)
#         self.assertEqual(data['message'], 'The requested resource could not be found.')
#
#     def test_405_method_not_allowed(self):
#         res = self.client().delete('/questions')
#         data = json.loads(res.data)
#
#         self.assertEqual(res.status_code, 405)
#         self.assertEqual(data['success'], False)
#         self.assertEqual(data['message'], 'Method not allowed - please use an appropriate method with your request, or add a resource.')
#
# # # GET QUESTIONS BY CATEGORY
#     def test_get_questions_by_category(self):
#         res = self.client().get('/categories/1/questions')
#         data = json.loads(res.data)
#
#         self.assertEqual(res.status_code, 200) # Check the response is 200 response
#         self.assertEqual(data['success'], True) # Check json success = true
#         self.assertTrue(data['total_questions']) # Check total_questions var is populated
#         self.assertTrue(data['current_category']) # Check current_category var is populated
#         self.assertTrue(data['categories']) # Check categories var is populated
#
#     def test_404_question_not_found(self):
#         res = self.client().get('/categories/88/questions')
#         data = json.loads(res.data)
#
#         self.assertEqual(res.status_code, 404)
#         self.assertEqual(data['success'], False)
#         self.assertEqual(data['message'], 'The requested resource could not be found.')
#
# # QUIZ
#     def test_retrieve_next_quiz_question(self):
#         res = self.client().post('/quizzes', json=self.quiz_example_1)
#         data = json.loads(res.data)
#
#         self.assertEqual(res.status_code, 200)
#         self.assertEqual(data['success'], True)
#         self.assertTrue(len(data['question']))
#
#     def test_404_next_quiz_question_not_found(self):
#         res = self.client().post('/quizzes', json=self.quiz_example_2)
#         data = json.loads(res.data)
#
#         self.assertEqual(res.status_code, 404)
#         self.assertEqual(data['success'], False)
#         self.assertEqual(data['message'], 'The requested resource could not be found.')
#
#     def test_422_sent_unable_to_filter_quiz_questions(self):
#         res = self.client().post('/quizzes', json=self.quiz_example_3)
#         data = json.loads(res.data)
#
#         self.assertEqual(res.status_code, 422)
#         self.assertEqual(data['success'], False)
#         self.assertEqual(data['message'], 'The request was valid, but there was an issue during processing. Data may be out of range. Please consult the documentation and resubmit.')
#
#
#     def test_400_sent_json_sent_for_quiz_questions_not_formatted_correctly(self):
#         res = self.client().post('/quizzes', json=self.quiz_example_4)
#         data = json.loads(res.data)
#
#         self.assertEqual(res.status_code, 400)
#         self.assertEqual(data['success'], False)
#         self.assertEqual(data['message'], 'Unable to process the request due to invalid data. Please reformat the request and resubmit.')

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
