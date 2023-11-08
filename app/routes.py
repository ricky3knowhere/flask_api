from app import app, response
from app.controller import DosenController, UserController
from flask import request, jsonify
from flask_jwt_extended import get_jwt_identity, jwt_required


@app.route("/")
def index():
    return "Hello Flask API"


@app.route("/api/dosen/page")
def paginations():
    return DosenController.paginate()


@app.route("/protected", methods=["GET"])
@jwt_required
def protected():
    current_user = get_jwt_identity()
    return response.success(current_user, "Success")


@app.route("/dosen", methods=["GET", "POST"])
def dosen():
    if request.method == "GET":
        return DosenController.index()
    else:
        return DosenController.save()


@app.route("/dosen/<id>", methods=["GET", "PUT", "DELETE"])
def dosens(id):
    if request.method == "GET":
        return DosenController.detail(id)
    elif request.method == "PUT":
        return DosenController.update(id)
    elif request.method == "DELETE":
        return DosenController.delete(id)


@app.route("/file-upload", methods=["POST"])
def uploads():
    return UserController.upload()


@app.route("/create-admin", methods=["POST"])
def admins():
    return UserController.create_admin()


@app.route("/login", methods=["POST"])
def login():
    return UserController.login()
