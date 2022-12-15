from pymongo import MongoClient
import datetime
import random


client = MongoClient()
db =client["my_db"]


detection = ["Safety Equipment Missing","Accident"]
employee = ["Noddy","Geeyan","Shizuka","Kaaliya","Chutki","Tom","Jerry","Bunny","Jim","Chota bhim"]
location = ["Front gate", "Back gate", "Assembley line"]
record_no = 15
date_time = datetime.datetime.now()

for i in range(1,record_no+1):
    loc = random.randrange(0,3)
    db["camera"].insert_one(
    
        {"cam_id": i,
        "Camera_Name": f"Camera {i}",
        "Location": location[loc],
        "Date_and_Time": date_time,
        "is_working": True,
        "is_paused": False
        }
)

#no of alerts
alert_no= 10

for j in range(1,alert_no+1):
    detc = random.randrange(0,2)
    emp = random.randrange(0,10)
    loc = random.randrange(0,3)
    db["alert"].insert_one(

    {
        "msg_id" : f"{100+j}",
        "Camera_Name": f"Camera {j}",
        "Location": location[loc],
        "Date_and_Time": date_time,
        "Detection_Type": detection[detc],
        "Employee_Name": employee[emp],
        "Reference_Number": f"{1000+j}",
        "Annotated_Image": "url_link [for image resource]",
        "Details": [
        {
        "id": 1,
        "text": "Safety Hand-Gloves Missing"
        },
        {
        "id": 2,
        "text": "Safety Shoes Missing"
        },
        {
        "id" :3,
        "text":"safety Helmet Missing"
        }
        ]
}
)
