import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db, Member, Skill, db

USERTOKEN = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImtpZCI6Ik1qSTRRakkyTlRSQ09UaENPVGsyTVRjNFFqTkZOME14T1RKQlJFWTFNRGRCUWtVeE1FRTVSUSJ9.eyJpc3MiOiJodHRwczovL3NraWxsLWV4Y2hhbmdlLmV1LmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw1ZGQzZjBjN2EwNzJkMjBmMTJhMTFlMmEiLCJhdWQiOiJza2lsbHNleGNoYW5nZSIsImlhdCI6MTU3NDg0NDQ3NCwiZXhwIjoxNTc0OTMwODc0LCJhenAiOiJSSkZ5MUpoRE9zOHpaaVlxQlBUa2xvQ0JYanA1RnlFYiIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOnByb2ZpbGUiLCJwYXRjaDpwcm9maWxlIiwicG9zdDpwcm9maWxlIiwicmVhZDpwcm9maWxlIiwicmVhZDpza2lsbHMiXX0.ohJUPIFSN8L8_urHXe2L-VWsSO5-xn3pqSI31sjjbe4q0guddRm5nOGPuNoWN0dnII1nQsi1fkpr94DeT7Se7NRvEgzsFXa8nNmN4uIn_I-ezk1iRPHCCqLmsTO7dbjEUzA3BB77BhK2aGlPYbanQ5_DywytpxeO8LYrVAwGb7mmJNCbNZOmkNSi7_7cnCZYst84T0hyca5_-uh1XMTzTKnDl-xPUfQ7HJ4DTZtu72LpXzn1TeKaqC1xOE_N6s-xzxTUevVTnezGFn1RMeQfOEwUsEgvyqznMMnEG5jlLuX5CrMNT4FG1Ij_5rzF7aasOhYvHSHwyEHgQRLDY8TiNQ'
ADMINTOKEN = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImtpZCI6Ik1qSTRRakkyTlRSQ09UaENPVGsyTVRjNFFqTkZOME14T1RKQlJFWTFNRGRCUWtVeE1FRTVSUSJ9.eyJpc3MiOiJodHRwczovL3NraWxsLWV4Y2hhbmdlLmV1LmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw1ZGQzZjE3ZDNmOWMwZTBlZjkwNjAyNTEiLCJhdWQiOiJza2lsbHNleGNoYW5nZSIsImlhdCI6MTU3NDg0NDAwNywiZXhwIjoxNTc0OTMwNDA3LCJhenAiOiJSSkZ5MUpoRE9zOHpaaVlxQlBUa2xvQ0JYanA1RnlFYiIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOm1lbWJlciIsImRlbGV0ZTpza2lsbHMiLCJwYXRjaDpza2lsbHMiLCJwb3N0OnNraWxscyIsInJlYWQ6bWVtYmVyIiwicmVhZDpza2lsbHMiXX0.hK-nbFpu-mVYOS3rudyGOWIFwSbRtCNgIk5eYZYQxW8zjXtJ3UH6UBfsrjfbOfpyIPbfeGg5fEQMctrROpq3KwOrB3bKNIpx8-9aSkTNM6Gh5DxneGxcTL1ATkowHW3W3TmRrOb38KvY5US78hTrr2KAL0SU6hA7P0zZW76kRlFKKNrsRoaMofFNQf4tgbnHFL8gQeNRbLlmQRREDpjdORV8H3lWrMYj4JrIYn9gyOgF886G_OxJcGmFI1mJZt1tsbgSChmC4LtsNziMLTjQwNmL8uqrYkupfMPq_kbfXkKxQmD_f5OpMPZGySW6jOyc8DvtKqVbF9kr8fALm44S_A'

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

## GET ALL MEMBERS (USER) - 401 error - user doesn't have permission
    def test_0011_HTTP_401_retrieve_all_members(self):
        res = self.client().get('/members', headers=self.userheaders)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['code'], "unauthorized")
        self.assertEqual(data['description'], "Permission not in payload.")

## GET ALL MEMBERS (USER) - 401 error - no auth provided
    def test_0012_HTTP_401_retrieve_all_members(self):
        res = self.client().get('/members')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['code'], "no_auth_in_header")
        self.assertEqual(data['description'], "No authorization details in request header.")

# TEST FOR 404 ERROR
    def test_0015_HTTP_404_unable_to_retrieve_member_list(self):
        res = self.client().get('/members/1', headers=self.adminheaders)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'The requested resource could not be found.')

# TEST FOR 405 ERROR ON MEMBERS (POST)
    def test_0016_HTTP_405_unable_to_post_member_list(self):
        res = self.client().post('/members', headers=self.adminheaders, json=self.new_profile_anni)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Method not allowed - please use an appropriate method with your request, or add a resource.')

## GET INDIVIDUAL MEMBER (ADMIN)
    def test_0020_retrieve_member_profile(self):
        res = self.client().get('/member/1', headers=self.adminheaders)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['member'])

## GET INDIVIDUAL MEMBER (USER) - 401 error - user doesn't have permission
    def test_0021_HTTP_401_retrieve_member_1(self):
        res = self.client().get('/member/1', headers=self.userheaders)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['code'], "unauthorized")
        self.assertEqual(data['description'], "Permission not in payload.")

# TEST FOR 404 ERROR
    def test_0025_HTTP_404_unable_to_find_member(self):
        res = self.client().get('/member/1000', headers=self.adminheaders)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'The requested resource could not be found.')

# TEST FOR 405 ERROR ON MEMBER (POST)
    def test_0026_HTTP_405_unable_to_post_member(self):
        res = self.client().post('/member/1', headers=self.adminheaders, json=self.new_profile_anni)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Method not allowed - please use an appropriate method with your request, or add a resource.')

# TEST FOR 405 ERROR ON MEMBER (PATCH)
    def test_0027_HTTP_405_unable_to_patch_member(self):
        res = self.client().patch('/member/1', headers=self.adminheaders, json=self.edit_profile_anni)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Method not allowed - please use an appropriate method with your request, or add a resource.')

## GET ALL SKILLS (ADMIN)
    def test_0030_retrieve_all_skills_admin(self):
        res = self.client().get('/skills', headers=self.adminheaders)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['skills'])

## GET ALL SKILLS (USER)
    def test_0031_retrieve_all_skills_user(self):
        res = self.client().get('/skills', headers=self.userheaders)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['skills'])

## GET ALL SKILLS (USER) - 401 error - no auth
    def test_0036_HTTP_401_retrieve_all_skills(self):
        res = self.client().get('/skills')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['code'], "no_auth_in_header")
        self.assertEqual(data['description'], "No authorization details in request header.")

# TEST FOR 404 ERROR
    def test_0037_HTTP_404_unable_to_retrieve_skill_list(self):
        res = self.client().get('/skills/1', headers=self.adminheaders)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'The requested resource could not be found.')

# TEST FOR 405 ERROR ON SKILLS (POST)
    def test_0038_HTTP_405_unable_to_post_skills(self):
        res = self.client().post('/skills', headers=self.adminheaders, json=self.new_skill_esp)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Method not allowed - please use an appropriate method with your request, or add a resource.')

## GET INDIVIDUAL SKILL (ADMIN)
    def test_0040_retrieve_skill_admin(self):
        res = self.client().get('/skill/1', headers=self.adminheaders)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['skill'])

## GET INDIVIDUAL SKILL (USER)
    def test_0041_retrieve_skill_user(self):
        res = self.client().get('/skill/1', headers=self.userheaders)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['skill'])

## GET INDIVIDUAL SKILL (USER) - 401 error - no auth
    def test_0046_HTTP_401_retrieve_skill_no_auth(self):
        res = self.client().get('/skill/1')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['code'], "no_auth_in_header")
        self.assertEqual(data['description'], "No authorization details in request header.")

# TEST FOR 404 ERROR
    def test_0047_HTTP_404_unable_to_retrieve_skill(self):
        res = self.client().get('/skills/1000', headers=self.adminheaders)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'The requested resource could not be found.')

## POST SKILL (ADMIN)
    def test_0050_create_skill(self):
        res = self.client().post('/skill', headers=self.adminheaders, json=self.new_skill_esp)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['skill'])

## POST SKILL (USER) - 401 error - user doesn't have permission
    def test_0051_HTTP_401_create_skill(self):
        res = self.client().post('/skill', headers=self.userheaders, json=self.new_skill_esp)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['code'], "unauthorized")
        self.assertEqual(data['description'], "Permission not in payload.")

## ERROR 422 - duplicate skill
    def test_0055_422_unable_to_create_new_skill(self):
        res = self.client().post('/skill', headers=self.adminheaders, json=self.new_skill_esp)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'The request was valid, but there was an issue during processing. Data may be out of range. Please consult the documentation and resubmit.')

## PATCH SKILL (ADMIN)
    def test_0060_edit_skill(self):
        res = self.client().patch('/skill/1', headers=self.adminheaders, json=self.edit_skill_eng)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['skill'])

## PATCH SKILL (USER) - 401 error - user doesn't have permission
    def test_0061_HTTP_401_edit_skill(self):
        res = self.client().patch('/skill/1', headers=self.userheaders, json=self.edit_skill_eng)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['code'], "unauthorized")
        self.assertEqual(data['description'], "Permission not in payload.")

## ERROR 400 - PATCH SKILL NO DATA
    def test_0065_400_edit_skill_no_data(self):
        res = self.client().patch('/skill/1', headers=self.adminheaders)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Unable to process the request due to invalid data. Please reformat the request and resubmit.')

## DELETE SKILL (ADMIN)
    def test_0070_delete_skill(self):
        res = self.client().delete('/skill/1', headers=self.adminheaders)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['delete'], 1)

## DELETE SKILL (USER) - 401 error - user doesn't have permission
    def test_0071_HTTP_401_delete_skill(self):
        res = self.client().delete('/skill/1', headers=self.userheaders)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['code'], "unauthorized")
        self.assertEqual(data['description'], "Permission not in payload.")

# TEST FOR 404 ERROR
    def test_0075_HTTP_404_skill_does_not_exist(self):
        res = self.client().delete('/skill/1000', headers=self.adminheaders)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'The requested resource could not be found.')

## DELETE PROFILE (ADMIN)
    def test_0080_delete_member_profile(self):
        res = self.client().delete('/member/1', headers=self.adminheaders)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['delete'], 1)

## DELETE SKILL (USER) - 401 error - user doesn't have permission
    def test_0081_HTTP_401_delete_member_profile(self):
        res = self.client().delete('/member/1', headers=self.userheaders)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['code'], "unauthorized")
        self.assertEqual(data['description'], "Permission not in payload.")

# TEST FOR 404 ERROR
    def test_0085_HTTP_404_member_profile_does_not_exist(self):
        res = self.client().delete('/member/1000', headers=self.adminheaders)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'The requested resource could not be found.')

## POST PROFILE (USER)
    def test_0090_create_member_profile(self):
        res = self.client().post('/profile', headers=self.userheaders, json=self.new_profile_anni)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['member'])

## POST PROFILE (ADMIN) - 401 error - user doesn't have permission
    def test_0091_HTTP_401_create_profile(self):
        res = self.client().post('/profile', headers=self.adminheaders, json=self.new_profile_anni)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['code'], "unauthorized")
        self.assertEqual(data['description'], "Permission not in payload.")

## ERROR 422 - duplicate member
    def test_0095_422_unable_to_create_new_profile(self):
        res = self.client().post('/profile', headers=self.userheaders, json=self.new_profile_anni)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'The request was valid, but there was an issue during processing. Data may be out of range. Please consult the documentation and resubmit.')

## GET PROFILE (USER)
    def test_0100_retrieve_own_profile(self):
        res = self.client().get('/profile', headers=self.userheaders)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['member'])

## GET PROFILE (ADMIN) - 401 error - user doesn't have permission
    def test_0101_HTTP_401_get_profile_permission(self):
        res = self.client().get('/profile', headers=self.adminheaders)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['code'], "unauthorized")
        self.assertEqual(data['description'], "Permission not in payload.")

## GET PROFILE (ADMIN) - 401 error - no auth provided
    def test_0102_HTTP_401_get_profile_no_auth(self):
        res = self.client().get('/profile')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['code'], "no_auth_in_header")
        self.assertEqual(data['description'], "No authorization details in request header.")

# TEST FOR 404 ERROR on GET PROFILE (endpoint uses token to establish UserId so run test before user created)
    def test_0088_HTTP_404_profile_does_not_exist(self):
        res = self.client().get('/profile', headers=self.userheaders)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'The requested resource could not be found.')

## PATCH PROFILE (USER)
    def test_0110_edit_own_profile(self):
        res = self.client().patch('/profile', headers=self.userheaders, json=self.edit_profile_anni)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['profile'])

## PATCH PROFILE (ADMIN) - 401 error - user doesn't have permission
    def test_0111_HTTP_401_edit_profile(self):
        res = self.client().patch('/profile', headers=self.adminheaders, json=self.edit_profile_anni)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['code'], "unauthorized")
        self.assertEqual(data['description'], "Permission not in payload.")

## ERROR 400 - PATCH PROFILE NO DATA
    def test_0115_400_edit_profile_no_data(self):
        res = self.client().patch('/profile', headers=self.userheaders)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Unable to process the request due to invalid data. Please reformat the request and resubmit.')

## DELETE PROFILE (USER)
    def test_0120_delete_member_profile(self):
        res = self.client().delete('/profile', headers=self.userheaders)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['delete'])

## DELETE PROFILE (ADMIN) - 401 error - user doesn't have permission
    def test_0121_HTTP_401_delete_profile(self):
        res = self.client().delete('/profile', headers=self.adminheaders)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['code'], "unauthorized")
        self.assertEqual(data['description'], "Permission not in payload.")

# TEST FOR 404 ERROR on DELETE PROFILE (endpoint uses token to establish UserId so run test before user created)
    def test_0089_HTTP_404_delete_profile_does_not_exist(self):
        res = self.client().delete('/profile', headers=self.userheaders)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'The requested resource could not be found.')

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
