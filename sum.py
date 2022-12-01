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
import mongo
app = Flask(__name__)

# Setup the Flask-JWT-Extended extension
app.config["JWT_SECRET_KEY"] = "super-secret"  # Change this!
jwt = JWTManager(app)
user=[]
password=[]
username_password={"vinayak":"1234",
                    "anshuman":"5678" }

# Create a route to authenticate your users and return JWTs. The
# create_access_token() function is used to actually generate the JWT.
@app.route("/register", methods=["POST"])
def register():
    username = request.json.get("username", None)
    password = request.json.get("password", None)
    
   
    if username in user :
        return jsonify({"msg": "user alredy exit"}), 401
    else:
        # item={"username":username,"password":password}
         user.append(username)
         username_password[username]=password
       # user.append(password)
         return jsonify({'msg':"user succsesfully registered"})

    access_token = create_access_token(identity=username)
    return jsonify(access_token=access_token)


# Protect a route with jwt_required, which will kick out requests
# without a valid JWT present.
@app.route("/users", methods=["GET"])
@jwt_required()
def get_all_users():
    # Access the identity of the current user with get_jwt_identity
    #current_user = get_jwt_identity()
    return jsonify({ "user":user}), 200

#user login method

@app.route("/login",methods=["POST"])
def login():
    useName=request.json.get("username",None)
    pword=request.json.get("password",None)
    if useName in user and username_password[useName]==pword:
        acc_token=create_access_token(identity=useName)
        return jsonify(acc_token=acc_token)
   
    
    return jsonify({"msg":"wrong username or password"}),401


@jwt.token_in_blocklist_loader
def check_if_token_in_blocklist(jwt_header, jwt_payload):
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
def addcamera():
    camera = request.json
    if camera is None:
        return {"message":"No Request found"}
    mongo.add_camera(camera)
    return {"message":"Camera successfully added"}
    

@app.route("/alert", methods=["POST"])
def addalert():
    msg = request.json
    if msg is None:
        return {"message": "No request found"}
    mongo.add_alert(msg)
    return {"message":"msg successfully added"}


class CustomJSONEncoder(JSONEncoder): 
    def default(self, obj):
        return json_util.default(obj)

y = CustomJSONEncoder()
@app.route("/cameras",methods=["GET"])
def cameras():
    all_cameras = mongo.all_camera()
    if all_cameras is None:
        return {"message": "No Camera found"}
    camera_list = []
    for x in all_cameras:
        camera_list.append(x)
    return jsonify(camera_list)

        
@app.route("/camera/id",methods=["GET"])
def camera_id():
    #geting cam_id
    camid=request.json.get("cam_id",None)
    return mongo.get_camera(camid)


@app.route("/alerts",methods=["GET"])
def alerts():
    mongo.all_alert() 
    all_alerts = mongo.all_camera()
    if all_alerts is None:
        return {"message": "No alert found"}
    alert_list = []
    for x in all_alerts:
        alert_list.append(x)
    return jsonify(alert_list)  
    
@app.route("/alert/msg_id",methods=["GET"])
def alert_msg():
    alrt=request.json.get("msg_id",None)
    return mongo.get_alert(alrt)


@app.route("/page", methods= ["GET"])
def get_page():
    page=request.json.get("page_no",None)
    entry=request.json.get("entry_no",None)
    pegina=mongo.pagination(entry,page)
    data=[]
    for x in pegina:
        #x["_id"]=str(x["_id"])
        data.append(x)
    return jsonify(data)


if __name__ == "__main__":
    app.run(debug=True)


