import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://faceattendacerealtime-ad7d1-default-rtdb.firebaseio.com/',
})
ref = db.reference('People')

data = {
    "0001" :
        {
            "name": "Nguyen Thanh Hien",
            "major": "Backend",
            "starting_year": 2023,
            "total_attendance": 6,
            "standing" : 1,
            "year": 4,
            "last_attendance_time": "2024-03-18 00:00:00"
        },
    "0002" :
        {
            "name": "Nguyen Hoang Anh",
            "major": "Backend",
            "starting_year": 2023,
            "total_attendance": 1,
            "standing" : 1,
            "year": 4,
            "last_attendance_time": "2024-03-18 00:00:00"
        },
    "0003" :
        {
            "name": "Nguyen Thanh Nhan",
            "major": "AI",
            "starting_year": 2023,
            "total_attendance": 4,
            "standing" : 3,
            "year": 4,
            "last_attendance_time": "2024-03-18 00:00:00"
        },
    "0004" :
        {
            "name": "Huynh Thanh Hai",
            "major": "Cybersecurity",
            "starting_year": 2023,
            "total_attendance": 5,
            "standing" : 4,
            "year": 4,
            "last_attendance_time": "2025-03-18 00:00:00"
        },
}

for key, value in data.items():
    ref.child(key).set(value)