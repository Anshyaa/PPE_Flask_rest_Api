import mongo

from flask import request, Flask

app = Flask(__name__)

@app.route("/camera/id", methods=["POST"])
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


@app.route("/alert/msg_id", methods=["POST"])
def getalert():
    msg_id = request.json
    if msg_id is None:
        return {"message":"No msg_id found"}
    mongo.get_alert(msg_id)
    return {"messager": "msg_id successfully added"}
    

@app.route("/camera", methods=["POST"])
def getcamera():
    cam_id = request.json
    if cam_id is None:
        return {"message":"No cam_id found"}
    mongo.get_alert(cam_id)
    return {"messager": "cam_id successfully added"}


@app.route("/cameras",methods=["GET"])
def cameras():
    return mongo.client["my_db"]["camera"]
    
 
@app.route("/camera/id",methods=["GET"])
def camera_id():
    #geting cam_id
    camid=request.json.get("cam_id",None)
    return mongo.get_camera(camid)


@app.route("/alerts",methods=["GET"])
def alerts():
    mongo.all_alert()   
    
@app.route("/alert/msg_id",methods=["GET"])
def alert_msg():
    al=request.json.get("msg_id",None)
    mongo.get_alert(al)

if __name__ == "__main__":
    app.run()


