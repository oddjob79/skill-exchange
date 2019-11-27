Welcome to the Capstone Project for Udacity Full Stack Developer course
-------------------------------------------------------------------------

The project is hosted at Heroku and is available on the following URL - https://skill-exchange-rt.herokuapp.com

These are the first steps taken in creating an app for adults looking to learn new skills by finding people they can exchange skills with.
If you are someone who is looking to learn a new language for example, rather than paying for classes, you can offer to teach a skill of your own in exchange for learning the new language.
By entering some simple information together with the skills you are willing to offer and the skills you are looking for, the system engine will locate other members with compatible profiles (matching skills), so that you are subsequently able to arrange to exchange your skills with that member.

Please feel free to look through and let me know if you have any questions or feedback.

-----------------------------------
Things to know:
-----------------------------------
Authentication:
-----------------------------------
Please use the login link at https://skill-exchange-rt.herokuapp.com/ to get an JWT which can be used to access the API. There are two roles: User and Admin. The endpoints which can be accessed by these roles are specified in the API documentation below.
The following accounts can be utilized to gain a JWT. The password for each account is "Pa55word".
Admin:
admin@abba.com
Users:
benny@abba.com
bjorn@abba.com
anni@abba.com
agnetha@abba.com
herbie@hancock.com
user1@user.com
user2@user.com
user3@user.com
user4@user.com
user5@user.com

Please note that there can only be a one-to-one relationship between Auth0 logins and "Skills-Exchange" members. Each member in the system must be created by an Auth0 user, and the user_id is taken from the JWT used in the request.

-----------------------------------
Data:
-----------------------------------
I have added some skill and member data in order to demonstrate basic functionality of the API, otherwise you would need to post skills first followed by posting member data which utilizes the skills which already exist in the system. If you would rather use new data, all the "user.com" users and herbie@hancock.com are free to use, so can be utilized to create your own member "subset". Otherwise, please feel free to just delete it all and start from scratch.

-----------------------------------
Testing (unittest):
-----------------------------------
Before running the test_app.py script, you will need to create a test postgres database and populate it with some test data.
Assuming you have postgres running on your machine, you will need to do the following:
dropdb skillx_test (only if you have previously run the test_app.py script)
createdb skillx_test
psql -U <postgres-user> -d skillx_test -a -f "skillx_test_db.sql"
The test script utilizes two environment variables for the Authentication tokens for each role (User and Admin). These have been preset and should last for 24 hours. Please let me know if these aren't valid, or they need to be reset.

-----------------------------------
API documentation
-----------------------------------
Endpoints
-----------------------------------
GET '/profile'
GET '/member/{id}'
GET '/members'
GET '/skills'
GET '/skill/{id}'
POST '/profile'
POST '/skill'
DELETE '/profile'
DELETE '/member/{id}'
DELETE '/skill/{id}'
PATCH '/profile'
PATCH '/skill/{id}'

-----------------------------------
DETAILS:
-----------------------------------
GET '/profile'
curl https://skill-exchange-rt.herokuapp.com/profile
- Uses the user_id stored in the authorization bearer token to query the database and return the user's member profile information. The user making the request must have an active login with AuthO which is associated with the 'User' role, and must already have a valid member profile added to the database.
- Role(s) required: User
- Request Arguments: None
- Returns: An object containing a 'success' boolean, and a member key. The member key contains general information about the member, what skills the member holds and wants, as well as basic details about members who hold skills the member wants, and want skills the member holds.
Example -
{
  "member": {
    "gender": "Female",
    "id": 21,
    "location": "Sweden",
    "match_location": false,
    "matching_members": [
      {
        "gender": "Male",
        "id": 3,
        "location": "Barcelona",
        "name": "bjorn",
        "skills_held_wanted": [
          "Spanish"
        ],
        "skills_wanted_held": [
          "Russian"
        ]
      },
      {
        "gender": "Male",
        "id": 5,
        "location": "Barcelona",
        "name": "Herbie Hancock",
        "skills_held_wanted": [
          "Spanish"
        ],
        "skills_wanted_held": [
          "Piano"
        ]
      }
    ],
    "name": "Anni",
    "skills_held": [
      "English",
      "Spanish",
      "Singing"
    ],
    "skills_wanted": [
      "Russian",
      "French",
      "Piano"
    ]
  },
  "success": true
}

-----------------------------------
GET '/member/{id}'
curl https://skill-exchange-rt.herokuapp.com/member/21
- Requires a request made with the member id to return the user's profile information. User making the request must have an active login with AuthO which is associated with the 'Admin' role.
- Role(s) required: Admin
- Request Arguments: Member.id (integer)
- Returns: An object containing a 'success' boolean, and a member key. The member key contains general information about the member, what skills the member holds and wants, as well as basic details about members who hold skills the member wants, and want skills the member holds.
Example -
{
  "member": {
    "gender": "Female",
    "id": 21,
    "location": "Sweden",
    "match_location": false,
    "matching_members": [
      {
        "gender": "Male",
        "id": 3,
        "location": "Barcelona",
        "name": "bjorn",
        "skills_held_wanted": [
          "Spanish"
        ],
        "skills_wanted_held": [
          "Russian"
        ]
      },
      {
        "gender": "Male",
        "id": 5,
        "location": "Barcelona",
        "name": "Herbie Hancock",
        "skills_held_wanted": [
          "Spanish"
        ],
        "skills_wanted_held": [
          "Piano"
        ]
      }
    ],
    "name": "Anni",
    "skills_held": [
      "English",
      "Spanish",
      "Singing"
    ],
    "skills_wanted": [
      "Russian",
      "French",
      "Piano"
    ]
  },
  "success": true
}

-----------------------------------
GET '/members'
curl https://skill-exchange-rt.herokuapp.com/members
- Returns basic information about all members in the system. User making the request must have an active login with AuthO which is associated with the 'Admin' role.
- Role(s) required: Admin
- Request Arguments: None
- Returns: An object containing a 'success' boolean, and a 'members' key. The members key contains the members' id, name, location and gender.
Example -
{
  "members": [
    {
      "gender": "Male",
      "id": 2,
      "location": "Barcelona",
      "name": "benny"
    },
    {
      "gender": "Male",
      "id": 3,
      "location": "Barcelona",
      "name": "bjorn"
    },
    {
      "gender": "Male",
      "id": 5,
      "location": "Barcelona",
      "name": "Herbie Hancock"
    },
    {
      "gender": "Female",
      "id": 21,
      "location": "Sweden",
      "name": "Anni"
    }
  ],
  "success": true
}

-----------------------------------
GET '/skills'
curl https://skill-exchange-rt.herokuapp.com/skills
- Returns basic information about all skills listed in the system. User making the request must have an active login with AuthO which is associated with either the 'Admin' or the 'User' role.
- Role(s) required: User or Admin
- Request Arguments: None
- Returns: An object containing a 'success' boolean, and a 'skills' key. The skills key contains the skill id, name, description, category and equipment_reqd.
Example -
{
  "skills": [
    {
      "category": null,
      "description": "",
      "equipment_reqd": "",
      "id": 1,
      "name": "English"
    },
    {
      "category": null,
      "description": "",
      "equipment_reqd": "",
      "id": 2,
      "name": "Spanish"
    },
    {
      "category": null,
      "description": "",
      "equipment_reqd": "",
      "id": 4,
      "name": "Russian"
    },
    {
      "category": null,
      "description": "",
      "equipment_reqd": "",
      "id": 5,
      "name": "French"
    },
    {
      "category": null,
      "description": "",
      "equipment_reqd": "",
      "id": 6,
      "name": "Singing"
    },
    {
      "category": null,
      "description": "",
      "equipment_reqd": "",
      "id": 7,
      "name": "Dancing"
    },
    {
      "category": null,
      "description": "",
      "equipment_reqd": "",
      "id": 8,
      "name": "Guitar"
    },
    {
      "category": null,
      "description": "",
      "equipment_reqd": "",
      "id": 9,
      "name": "Piano"
    },
    {
      "category": "music",
      "description": "Play the harpsichord",
      "equipment_reqd": "harpsichord",
      "id": 10,
      "name": "Harpsichord"
    }
  ],
  "success": true
}

-----------------------------------
GET '/skill/{id}'
curl https://skill-exchange-rt.herokuapp.com/skill/10
- Returns basic information about the skill matching the skill id specified in the request. User making the request must have an active login with AuthO which is associated with either the 'Admin' or the 'User' role.
- Role(s) required: User or Admin
- Request Arguments: Skill.id
- Returns: An object containing a 'success' boolean, and a 'skill' key. The skills key contains the skill id, name, description, category and equipment_reqd.
Example -
{
  "skill": {
    "category": "music",
    "description": "Play the harpsichord",
    "equipment_reqd": "harpsichord",
    "id": 10,
    "name": "Harpsichord"
  },
  "success": true
}

-----------------------------------
POST '/profile'
curl -X POST -H "Content-Type: application/json" -d {
	"name": "Anni",
	"location": "Sweden",
	"gender": "Female",
	"match_location": false,
	"skills_held": ["English", "Spanish", "Singing"],
	"skills_wanted": ["Russian", "French", "Piano"]
} https://skill-exchange-rt.herokuapp.com/profile
- Uses the user_id stored in the authorization bearer token to create a new member profile in the system. The user making the request must have an active login with AuthO which is associated with the 'User' role, and must NOT already have a valid user profile added to the database
All columns are required in order to successfully process the request.
- Role(s) required: User
- Request Arguments: json data
- Returns: An object containing a 'success' boolean, and a member key. The member key contains general information about the newly created member, what skills the member holds and wants, as well as basic details about members who hold skills the member wants, and want skills the member holds.
Example -
{
  "member": {
    "gender": "Female",
    "id": 21,
    "location": "Sweden",
    "match_location": false,
    "matching_members": [
      {
        "gender": "Male",
        "id": 3,
        "location": "Barcelona",
        "name": "bjorn",
        "skills_held_wanted": [
          "Spanish"
        ],
        "skills_wanted_held": [
          "Russian"
        ]
      },
      {
        "gender": "Male",
        "id": 5,
        "location": "Barcelona",
        "name": "Herbie Hancock",
        "skills_held_wanted": [
          "Spanish"
        ],
        "skills_wanted_held": [
          "Piano"
        ]
      }
    ],
    "name": "Anni",
    "skills_held": [
      "English",
      "Spanish",
      "Singing"
    ],
    "skills_wanted": [
      "Russian",
      "French",
      "Piano"
    ]
  },
  "success": true
}

-----------------------------------
POST '/skill'
curl -X POST -H "Content-Type: application/json" -d {
	"name": "Furniture making",
	"description": "Building cabinets for your front room",
	"category": "trade",
	"equipment_reqd": "tools and wood"
} https://skill-exchange-rt.herokuapp.com/skill
- Uses the json data included in the request to create a new skill record in the system. User making the request must have an active login with AuthO which is associated with the 'Admin' role. Only the 'name' field is required in order to successfully create a new skill.
- Role(s) required: Admin
- Request Arguments: json data
- Returns: An object containing a 'success' boolean, and a 'skill' key. The skills key contains the skill id, name, description, category and equipment_reqd of the newly created record.
Example -
{
  "skill": {
    "category": "music",
    "description": "Play the harpsichord",
    "equipment_reqd": "harpsichord",
    "id": 10,
    "name": "Harpsichord"
  },
  "success": true
}

-----------------------------------
DELETE '/profile'
curl -X DELETE https://skill-exchange-rt.herokuapp.com/profile
- Uses the user_id stored in the authorization bearer token to query the database and delete the corresponding member profile record. The user making the request must have an active login with AuthO which is associated with the 'User' role, and must already have a valid member profile added to the database.
- Role(s) required: User
- Request Arguments: None
- Returns: An object containing a 'success' boolean, and a deleted key containing the member.id of the deleted profile.
Example -
{
  "delete": 21,
  "success": true
}

-----------------------------------
DELETE '/member/{id}'
curl -X DELETE https://skill-exchange-rt.herokuapp.com/member/21
- Requires a request made with the member id to query the database and delete the corresponding member profile. User making the request must have an active login with AuthO which is associated with the 'Admin' role.
- Role(s) required: Admin
- Request Arguments: Member.id (integer)
- Returns: An object containing a 'success' boolean, and a deleted key containing the member.id of the deleted profile.
Example -
{
  "delete": 21,
  "success": true
}

-----------------------------------
DELETE '/skill/{id}'
curl -X DELETE https://skill-exchange-rt.herokuapp.com/skill/11
- Requires a request made with the skill id to query the database and delete the corresponding Skill record. User making the request must have an active login with AuthO which is associated with the 'Admin' role.
- Role(s) required: Admin
- Request Arguments: Skill.id (integer)
- Returns: An object containing a 'success' boolean, and a deleted key containing the Skill.id of the deleted skill record.
Example -
{
  "delete": 11,
  "success": true
}

-----------------------------------
PATCH '/profile'
curl -X PATCH -H "Content-Type: application/json" -d {
  {
  	"name": "Anni-Frid",
  	"location": "London",
  	"skills_held": ["English", "Spanish", "Singing", "Dancing"],
  	"skills_wanted": ["Russian", "French", "Piano", "Guitar"]
  } https://skill-exchange-rt.herokuapp.com/profile
- Uses the user_id stored in the authorization bearer token to update the corresponding member profile in the system. The user making the request must have an active login with AuthO which is associated with the 'User' role, and must already have a valid user profile added to the database
- Role(s) required: User
- Request Arguments: json data
- Returns: An object containing a 'success' boolean, and a profile key. The member key contains general information about the newly created member, what skills the member holds and wants, as well as basic details about members who hold skills the member wants, and want skills the member holds.
Example -
{
  "profile": {
    "gender": "Female",
    "id": 21,
    "location": "London",
    "match_location": false,
    "matching_members": [
      {
        "gender": "Male",
        "id": 3,
        "location": "Barcelona",
        "name": "bjorn",
        "skills_held_wanted": [
          "Spanish"
        ],
        "skills_wanted_held": [
          "Russian"
        ]
      },
      {
        "gender": "Male",
        "id": 5,
        "location": "Barcelona",
        "name": "Herbie Hancock",
        "skills_held_wanted": [
          "Spanish"
        ],
        "skills_wanted_held": [
          "Piano"
        ]
      }
    ],
    "name": "Anni-Frid",
    "skills_held": [
      "English",
      "Spanish",
      "Singing",
      "Dancing"
    ],
    "skills_wanted": [
      "Russian",
      "French",
      "Guitar",
      "Piano"
    ]
  },
  "success": true
}

-----------------------------------
PATCH '/skill/{id}'
curl -X PATCH -H "Content-Type: application/json" -d {
	"description": "Learn to play the harpsichord like a pro",
	"category": "musical instrument",
	"equipment_reqd": "your own harpsichord"
} https://skill-exchange-rt.herokuapp.com/skill
- Uses the Skill.id included in the request to update the corresponding skill record in the system. User making the request must have an active login with AuthO which is associated with the 'Admin' role.
- Role(s) required: Admin
- Request Arguments: Skill.id & json data
- Returns: An object containing a 'success' boolean, and a 'skill' key. The skills key contains the skill id, name, description, category and equipment_reqd of the newly created record.
Example -
{
  "skill": {
    "category": "musical instrument",
    "description": "Learn to play the harpsichord like a pro",
    "equipment_reqd": "your own harpsichord",
    "id": 10,
    "name": "Harpsichord"
  },
  "success": true
}
