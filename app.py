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
import bcrypt

app = Flask(__name__)

# Setup the Flask-JWT-Extended extension
app.config["JWT_SECRET_KEY"] = "super-secret"  # Change this!
jwt = JWTManager(app)

# Create a route to authenticate your users and return JWTs. The
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
        return jsonify({"msg":"user succsesfully registered"})
    return jsonify({"msg": "user alredy exit"}), 401


# Protect a route with jwt_required, which will kick out requests
# without a valid JWT present.
@app.route("/users", methods=["GET"])
@jwt_required()
def get_all_users():
    list_user = []
    all_user = mongo.get_allusers()
    for x in all_user:
        list_user.append(x)
    
    # Access the identity of the current user with get_jwt_identity
    #current_user = get_jwt_identity()
    return jsonify(list_user), 200

#user login method

@app.route("/login",methods=["POST"])
def login():
    useName=request.json.get("username",None)
    pword=request.json.get("password",None)

    user=mongo.get_user(useName)
    if user is None:
        return {"message": "wrong username"}
    if user["password"]==pword:
        acc_token=create_access_token(identity=useName)
        return jsonify(acc_token=acc_token)
    return jsonify({"msg":"wrong password"}),401


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
        return {"message": "No request found"}
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
        return {"message": "No Camera found"}
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
    
@app.route("/alert/msg_id",methods=["GET"])
@jwt_required()
def alert_msg():
    alrt=request.json.get("msg_id",None)
    return mongo.get_alert(alrt)


@app.route("/page", methods= ["GET"])
@jwt_required()
def get_page():
    page=request.json.get("page_no",None)
    entry=request.json.get("entry_no",None)
    pegina=mongo.pagination(entry,page)
    data=[]
    dict = {"page_no":page,"entry_no":entry}
    data.append(dict)
    for x in pegina:
        x["_id"]=str(x["_id"])
        data.append(x)
    return jsonify(data)


if __name__ == "__main__":
    app.run(debug=True)

