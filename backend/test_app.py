import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db, Member, Skill, db

USERTOKEN = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImtpZCI6Ik1qSTRRakkyTlRSQ09UaENPVGsyTVRjNFFqTkZOME14T1RKQlJFWTFNRGRCUWtVeE1FRTVSUSJ9.eyJpc3MiOiJodHRwczovL3NraWxsLWV4Y2hhbmdlLmV1LmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw1ZGQzZjBjN2EwNzJkMjBmMTJhMTFlMmEiLCJhdWQiOiJza2lsbHNleGNoYW5nZSIsImlhdCI6MTU3NDc1Nzc5NSwiZXhwIjoxNTc0NzY0OTk1LCJhenAiOiJSSkZ5MUpoRE9zOHpaaVlxQlBUa2xvQ0JYanA1RnlFYiIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOnByb2ZpbGUiLCJwYXRjaDpwcm9maWxlIiwicG9zdDpwcm9maWxlIiwicmVhZDpwcm9maWxlIiwicmVhZDpza2lsbHMiXX0.Cf2FshEqldWq1TJzimNlj6b25e0_tMR10G1wzp5GANXxXOUjbyp89BM9ZUbLN4f5nP2ZRxlAk3gVaGqERekasaLtcv1bJyXrkGWAA12_d1OmDXQwubdk1GWpTqgWy_ej8TD9uzSY7OtVz4bM1JNnv9IX0iykGfPL-0XtddGgX2uTI9qL1s6lQyXcXZ6uuxoH-mFjqMhEOSiAHF7XqvWUi55F0Q33QI3r0klatYQIXs9qykeHeC6EW5Sp9Gu6Gdcu4ShYPgndm5Bk-bWJN-75hyvf3yisCs55okWDVFqKRebRRMUW4ozeVp41TWnn3MKwq0ylUsUp7foWJPDr2_B72g'
ADMINTOKEN = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImtpZCI6Ik1qSTRRakkyTlRSQ09UaENPVGsyTVRjNFFqTkZOME14T1RKQlJFWTFNRGRCUWtVeE1FRTVSUSJ9.eyJpc3MiOiJodHRwczovL3NraWxsLWV4Y2hhbmdlLmV1LmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw1ZGQzZjE3ZDNmOWMwZTBlZjkwNjAyNTEiLCJhdWQiOiJza2lsbHNleGNoYW5nZSIsImlhdCI6MTU3NDc1NzcxNSwiZXhwIjoxNTc0NzY0OTE1LCJhenAiOiJSSkZ5MUpoRE9zOHpaaVlxQlBUa2xvQ0JYanA1RnlFYiIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOm1lbWJlciIsImRlbGV0ZTpza2lsbHMiLCJwYXRjaDpza2lsbHMiLCJwb3N0OnNraWxscyIsInJlYWQ6bWVtYmVyIiwicmVhZDpza2lsbHMiXX0.A3dhnJseivx-vwLOhWFSesQB5-Pk2dEg4V_lG19WQtSVOgCsfXArzkABd6SSxve-eNugr1Gj8PhJZiHlk567GX7C_3FaqAuA_3WQnw56zoW6n8ULFheF3eYusB1_qY5ihMABwmLbR4zB2GO_4d58w34HeAiQkSCC4lOUfg1WdxLZLoT2jX90hYBIsNfFvYNHSIz37T_q1vZHZW_2b_1zahPtLm0AndnBJfkXcOwnIzGQE-J-WtY6afgQmrG8aKE54lbx0ULjtsHBQAkKWwdD-HTpObpK_kWFCVHoMWIJhlF6CRLwFF_IPCIxoohwSJqU4oDzk75p1j3GIQCupDn-hA'

class SkillXTestCase(unittest.TestCase):
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
            "match_location": False,
            "skills_held": ["Piano"],
            "skills_wanted": ["Swimming"]
        }

        self.edit_profile_anni = {
            "name": "Anni-Frid",
            "location": "London",
            "skills_wanted": ["Swimming", "Chinese cooking"]
        }

        self.new_skill_esp = {
        	"name": "Spanish",
        	"description": "Spanish language to native speaker level",
        	"category": "language",
        	"equipment_reqd": "pen and paper"
        }

        self.edit_skill_eng = {
        	"description": "English language to native speaker level",
        	"category": "language",
        	"equipment_reqd": "pen and paper"
        }

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after each test"""
        # db.drop_all()
        pass

## GET ALL MEMBERS (ADMIN)
    def test_0010_retrieve_all_members(self):
        res = self.client().get('/members', headers=self.adminheaders)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['members'])

## GET INDIVIDUAL MEMBER (ADMIN)
    def test_0020_retrieve_member_profile(self):
        res = self.client().get('/member/1', headers=self.adminheaders)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['member'])

## GET ALL SKILLS (ADMIN)
    def test_0030_retrieve_all_skills(self):
        res = self.client().get('/skills', headers=self.adminheaders)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['skills'])

## GET INDIVIDUAL SKILL (ADMIN)
    def test_0040_retrieve_skill(self):
        res = self.client().get('/skill/1', headers=self.adminheaders)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['skill'])

## POST SKILL (ADMIN)
    def test_0050_create_skill(self):
        res = self.client().post('/skill', headers=self.adminheaders, json=self.new_skill_esp)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['skill'])

## PATCH SKILL (ADMIN)
    def test_0060_edit_skill(self):
        res = self.client().patch('/skill/1', headers=self.adminheaders, json=self.edit_skill_eng)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['skill'])

## DELETE SKILL (ADMIN)
    def test_0070_delete_skill(self):
        res = self.client().delete('/skill/1', headers=self.adminheaders)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['delete'], 1)

## DELETE PROFILE (ADMIN)
    def test_0080_delete_member_profile(self):
        res = self.client().delete('/member/1', headers=self.adminheaders)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['delete'], 1)

## POST PROFILE (USER)
    def test_0090_create_member_profile(self):
        res = self.client().post('/profile', headers=self.userheaders, json=self.new_profile_anni)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['member'])

## GET PROFILE (USER)
    def test_0100_retrieve_own_profile(self):
        res = self.client().get('/profile', headers=self.userheaders)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['member'])

## PATCH PROFILE (USER)
    def test_0110_edit_own_profile(self):
        res = self.client().patch('/profile', headers=self.userheaders, json=self.edit_profile_anni)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['profile'])

## DELETE PROFILE (USER)
    def test_0120_delete_member_profile(self):
        res = self.client().delete('/profile', headers=self.userheaders)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['delete'])



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
