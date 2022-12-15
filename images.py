#import base64
#from pymongo import MongoClient
#client = MongoClient()
#db = ["my_db"]["alert"]


#def insert_image(request):
#    with open(request.GET["image_name"], "rb") as image_file:
#        encoded_string = base64.b64encode(image_file.read())
#    print (encoded_string)
#    abc=db.database_name.insert({"image":encoded_string})
#    return HttpResponse("inserted")


# storing image to the database 

from pymongo import MongoClient
import gridfs
client = MongoClient()
db = client["my_db"]

fs = gridfs.GridFS(db)
file = "video.mp4"

with open(file,"rb") as f:
    contents =f.read()

fs.put(contents, filename=file)

# retrieving image fron the database

name = "video.mp4"
data = db.fs.files.find_one({"filename":name})
my_id = data["_id"]
output_data = fs.get(my_id).read()
output = open("video1.mp4","wb")
output.write(output_data)
output.close()

"""
from pymongo import MongoClient
import gridfs
import cv2

client = MongoClient("localhost", 27017)

db = client['my_db']
#Create an object of GridFs for the above database.
fs = gridfs.GridFS(db)
#Define an image object with the location.
file = "img001.png"

with open(file, 'rb') as f:
    contents = f.read()

#fs.put(contents, filename ="file")




from PIL import Image
import numpy

image = Image.open("img.png")
from numpy import asarray
data = asarray(image)
data
"""