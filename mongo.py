import pymongo

db = "my_db"
client = pymongo.MongoClient()


def get_camera(cam_id):
    (client["my_db"]["camera"].find_one({"cam_id":cam_id}))


def add_camera(camera):
    client["my_db"]["camera"].insert_one(camera)


def get_alert(msg_id):
    (client["my_db"]["camera"].find_one({"msg_id":msg_id}))

   
def add_alert(msg):
    client["my_db"]["alert"].insert_one(msg)
    

def all_camera():
    return client["my_db"]["camera"]


def all_alert():
    return {client["my_db"]["alert"].find().sort({"timestamp":-1})}


