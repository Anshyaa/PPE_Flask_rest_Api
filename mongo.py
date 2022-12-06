import pymongo


db = "my_db"
client = pymongo.MongoClient()


def get_camera(cam_id):
    return client["my_db"]["camera"].find_one({"cam_id":cam_id},{"_id":0})


def add_camera(camera):
    client["my_db"]["camera"].insert_one(camera)


def get_alert(msg_id):
    return client["my_db"]["alert"].find_one({"msg_id":msg_id},{"_id":0})

   
def add_alert(msg):
    client["my_db"]["alert"].insert_one(msg)
    

def all_camera():
    return client["my_db"]["camera"].find({},{"_id":0})


def all_alert():
    return client["my_db"]["alert"].find({},{"_id":0})

def add_user(user_and_password):
    client["my_db"]["user"].insert_one(user_and_password)


def get_user(username):
    return client["my_db"]["user"].find_one({"username":username})


def check_user(username):
    if client["my_db"]["user"].find_one({"username":username}):
        return True
    return False

def get_allusers():
    return client["my_db"]["user"].find({},{"password":0,"_id":0})


def pagination(entry,page):
    cursor_start = (page-1)*entry
    cursor_end = cursor_start + entry
    cursor = client["my_db"]["alert"].find().sort("Date_and_Time",-1)
    result = cursor[cursor_start:cursor_end]
    return result
