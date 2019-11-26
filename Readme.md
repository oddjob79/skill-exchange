Welcome to the Capstone Project for Udacity Full Stack Developer course

These are the first steps taken in creating an app for adults looking to learn new skills by finding people they can exchange skills with.
If you are someone who is looking to learn a new language for example, rather than paying for classes, you can offer to teach a skill of your own in exchange for learning the new language.
By entering some simple information together with the skills you are willing to offer and the skills you are looking for, the system engine will locate other members with compatible profiles (matching skills), so that you are subsequently able to arrange to exchange your skills with that member.

------------------------------------------------------------------------------------------------------------------------------------------------------------

Things to know:
Before running the test_app.py script, you will need to create a test postgres database and populate it with some test data.
Assuming you have postgres running on your machine, you will need to do the following:
dropdb skillx_test (only if you have previously run the test_app.py script)
createdb skillx_test
psql -U <postgres-user> -d skillx_test -a -f "skillx_test_db.sql"

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
curl <apiurl>/profile
- Uses the user_id stored in the authorization bearer token to query the database and return the user's member profile information. The user making the request must have an active login with AuthO which is associated with the 'User' role, and must already have a valid member profile added to the database.
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
curl <apiurl>/member/21
- Requires a request made with the member id to return the user's profile information. User making the request must have an active login with AuthO which is associated with the 'Admin' role.
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
curl <apiurl>/members
- Returns basic information about all members in the system. User making the request must have an active login with AuthO which is associated with the 'Admin' role.
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
curl <apiurl>/skills
- Returns basic information about all skills listed in the system. User making the request must have an active login with AuthO which is associated with either the 'Admin' or the 'User' role.
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
curl <apiurl>/skill/10
- Returns basic information about the skill matching the skill id specified in the request. User making the request must have an active login with AuthO which is associated with either the 'Admin' or the 'User' role.
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
} <apiurl>/profile
- Uses the user_id stored in the authorization bearer token to create a new member profile in the system. The user making the request must have an active login with AuthO which is associated with the 'User' role, and must NOT already have a valid user profile added to the database
All columns are required in order to successfully process the request.
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
} <apiurl>/skill
- Uses the json data included in the request to create a new skill record in the system. User making the request must have an active login with AuthO which is associated with the 'Admin' role. Only the 'name' field is required in order to successfully create a new skill.
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
curl -X DELETE <apiurl>/profile
- Uses the user_id stored in the authorization bearer token to query the database and delete the corresponding member profile record. The user making the request must have an active login with AuthO which is associated with the 'User' role, and must already have a valid member profile added to the database.
- Request Arguments: None
- Returns: An object containing a 'success' boolean, and a deleted key containing the member.id of the deleted profile.
Example -
{
  "delete": 21,
  "success": true
}

-----------------------------------
DELETE '/member/{id}'
curl -X DELETE <apiurl>/member/21
- Requires a request made with the member id to query the database and delete the corresponding member profile. User making the request must have an active login with AuthO which is associated with the 'Admin' role.
- Request Arguments: Member.id (integer)
- Returns: An object containing a 'success' boolean, and a deleted key containing the member.id of the deleted profile.
Example -
{
  "delete": 21,
  "success": true
}

-----------------------------------
DELETE '/skill/{id}'
curl -X DELETE <apiurl>/skill/11
- Requires a request made with the skill id to query the database and delete the corresponding Skill record. User making the request must have an active login with AuthO which is associated with the 'Admin' role.
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
  } <apiurl>/profile
- Uses the user_id stored in the authorization bearer token to update the corresponding member profile in the system. The user making the request must have an active login with AuthO which is associated with the 'User' role, and must already have a valid user profile added to the database
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
} <apiurl>/skill
- Uses the Skill.id included in the request to update the corresponding skill record in the system. User making the request must have an active login with AuthO which is associated with the 'Admin' role.
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
