from . import app
import os
import json
from flask import jsonify, request, make_response, abort, url_for  # noqa; F401

SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
json_url = os.path.join(SITE_ROOT, "data", "pictures.json")
data: list = json.load(open(json_url))

######################################################################
# RETURN HEALTH OF THE APP
######################################################################


@app.route("/health")
def health():
    return jsonify(dict(status="OK")), 200

######################################################################
# COUNT THE NUMBER OF PICTURES
######################################################################


@app.route("/count")
def count():
    """return length of data"""
    if data:
        return jsonify(length=len(data)), 200

    return {"message": "Internal server error"}, 500


######################################################################
# GET ALL PICTURES
######################################################################
@app.route("/picture", methods=["GET"])
def get_pictures():
    if data:
        return data, 200
    return {"Message": "There is no Data"}, 500

######################################################################
# GET A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["GET"])
def get_picture_by_id(id):
    for i in data:
        if i['id'] == id:
            return i, 200
    
    return {"Message": "No such ID"}, 404


######################################################################
# CREATE A PICTURE
######################################################################
@app.route("/picture", methods=["POST"])
def create_picture():
    pic = request.json
    if not pic: 
        return {"Message": "Invalid input parameters"}, 422 
    for i in data:
        if i['id'] == pic['id']:
            return {"Message": f"picture with id {pic['id']} already present"}, 302
    
    data.append(pic)
    return pic, 201

######################################################################
# UPDATE A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["PUT"])
def update_picture(id):
    new_pic = request.json
    for index, pic in enumerate(data):
        if pic['id'] == id:
            data[index] = new_pic
            return {"Message": "This picture has been updated"}, 302
    return {"Message": "picture not found"}, 404

######################################################################
# DELETE A PICTURE
######################################################################
@app.route("/picture/<int:id>", methods=["DELETE"])
def delete_picture(id):
    for index, pic in enumerate(data):
        if pic['id'] == id:
            data.pop(index)
            return {"Message": "Picture has been deleted"}, 204
    return {"Message": "picture not found"}, 404

