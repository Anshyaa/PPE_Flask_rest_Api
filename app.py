from flask import Flask
from flask import jsonify
from flask import request

from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required, get_jwt
from flask_jwt_extended import JWTManager
from blocklist import BLOCKLIST

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


from blocklist import BLOCKLIST

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


if __name__ == "__main__":
    app.run()

