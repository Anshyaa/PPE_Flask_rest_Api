from datetime import timedelta
from flask import Flask
from flask import jsonify
from flask import request
from flask.json import JSONEncoder
from bson import json_util

from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required, get_jwt
from flask_jwt_extended import JWTManager
from blocklist import BLOCKLIST
from flask_cors import CORS


import mongo
import bcrypt


app = Flask(__name__)
CORS(app)


# Setup the Flask-JWT-Extended extension
app.config["JWT_SECRET_KEY"] = "super-secret"
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(days=1)
jwt = JWTManager(app)


# Create a route to authenticate your users and return JWTs
# create_access_token() function is used to actually generate the JWT.
@app.route("/register", methods=["POST"])
def register():
    username = request.json.get("username", None)
    password = request.json.get("password", None)
    hashed = bcrypt.hashpw(password.encode('utf-8'),bcrypt.gensalt())
    password = hashed
    regi_info = {}
    use=mongo.check_user(username)
    if use is False:
        regi_info["username"]=username
        regi_info['password']=password
        mongo.add_user(regi_info)
        return jsonify({"message":"user succsesfully registered"})
    return jsonify({"message": "user alredy exit"}), 401


# Protect a route with jwt_required, which will kick out requests
# without a valid JWT present.
@app.route("/users", methods=["GET"])
@jwt_required()
def get_all_users():
    list_user = []
    all_user = mongo.get_allusers()
    for x in all_user:
        list_user.append(x)
    return jsonify(list_user), 200


#user login method
@app.route("/login",methods=["POST"])
def login():
    useName=request.json.get("username",None)
    pword=request.json.get("password",None)
    user=mongo.get_user(useName)
    if user is None:
        return {"message": "wrong username"},401
    raw = pword.encode('utf-8')
    bytes = bcrypt.checkpw(raw,user["password"])
    if bytes is True:
        acc_token=create_access_token(identity=useName)
        return jsonify(acc_token=acc_token)
    return jsonify({"message":"wrong password"})


@app.route("/change_password", methods=["POST"])
@jwt_required()
def change_password():
    useName = get_jwt_identity()
    pword = request.json.get("password",None)
    new_password = request.json.get("new_password", None)
    re_new_password = request.json.get("re_new_password",None)
    user = mongo.get_user(useName)
    bytes = bcrypt.checkpw(pword.encode('utf-8'),user["password"])
    if bytes is True:
        
        if new_password == re_new_password:
            hashed = bcrypt.hashpw(new_password.encode('utf-8'),bcrypt.gensalt())
            new_password = hashed
            mongo.change_password( useName,new_password)
            return jsonify({"message":"Password changed"})
        return jsonify({"message": "Password doesnt match"})
    return {"message":"Wrong password"}    
    

@jwt.token_in_blocklist_loader
def check_if_token_in_blocklist(jwt_header , jwt_payload):
    return jwt_payload["jti"] in BLOCKLIST


@jwt.revoked_token_loader
def revoked_token_callback(jwt_header, jwt_payload):
    return (
        jsonify(
            {"description": "The token has been revoked.", "error": "token_revoked"}
        ),
        401,
    )


@app.route("/logout", methods=["POST"])
@jwt_required()
def logout():
    jti = get_jwt()["jti"]
    BLOCKLIST.add(jti)
    return {"message": "Successfully logged out"}, 200


@app.route("/camera", methods=["POST"])
@jwt_required()
def addcamera():
    camera = request.json
    if camera is None:
        return {"message":"No Request found"}
    mongo.add_camera(camera)
    return {"message":"Camera successfully added"}
    

@app.route("/alert", methods=["POST"])
@jwt_required()
def addalert():
    msg = request.json
    if msg is None:
        return {"message": "No request found"},401
    mongo.add_alert(msg)
    return {"message":"msg successfully added"}


class CustomJSONEncoder(JSONEncoder): 
    def default(self, obj):
        return json_util.default(obj)
y = CustomJSONEncoder()
@app.route("/cameras",methods=["GET"])
@jwt_required()
def cameras():
    all_cameras = mongo.all_camera()
    if all_cameras is None:
        return {"message": "No Camera found"},401
    camera_list = []
    for x in all_cameras:
        camera_list.append(x)
    return jsonify(camera_list)

        
@app.route("/camera/id",methods=["GET"])
@jwt_required()
def camera_id():
    #geting cam_id
    camid=request.json.get("cam_id",None)
    return mongo.get_camera(camid)


@app.route("/alerts",methods=["GET"])
@jwt_required()
def alerts():
    mongo.all_alert() 
    all_alerts = mongo.all_camera()
    if all_alerts is None:
        return {"message": "No alert found"}
    alert_list = []
    for x in all_alerts:
        alert_list.append(x)
    return jsonify(alert_list)  
    
@app.route("/alert/msg_id",methods=["POST"])
@jwt_required()
def alert_msg():
    alrt=request.json.get("msg_id",None)
    return mongo.get_alert(alrt)


@app.route("/page", methods= ["POST"])
@jwt_required()
def get_page():
    page=request.json.get("page_no",None)
    entry=request.json.get("entry_no",None)
    pegina=mongo.pagination(page, entry)
    data=[]
    for x in pegina:
        x["_id"]=str(x["_id"])
        data.append(x)
    dict = {"entry_no":entry, "page_no":page, "pagination":data}
    return jsonify(dict)


if __name__ == "__main__":
    app.run(debug=True)


