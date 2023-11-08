from app.model.user import User
from app.model.picture import Picture
from flask import request
import os
from app import response, app, db, upload_config
import uuid
from werkzeug.utils import secure_filename

from datetime import datetime, timedelta
from flask_jwt_extended import *


def upload():
    try:
        title = request.form.get("title")
        print(title)
        print(request.files)
        if "files" not in request.files:
            return response.bad_request([], "File not found!")

        file = request.files["files"]
        if file.filename == "":
            return response.bad_request([], "Filename not found!")

        if file and upload_config.allowed_file(file.filename):
            uid = uuid.uuid4()
            filename = secure_filename(file.filename)
            rename_file = "Flask-" + str(uid) + filename

            file.save(os.path.join(app.config["UPLOAD_FOLDER"], rename_file))

            uploads = Picture(title=title, pathname=rename_file)
            db.session.add(uploads)
            db.session.commit()

            return response.success(
                {"title": title, "pathname": rename_file},
                "Picture Successfuly Uploaded.",
            )
        else:
            return response.bad_request([], "File not Allowed!")
    except Exception as err:
        print("Error : ", err)


def create_admin():
    try:
        (
            full_name,
            email,
            password,
        ) = request.form.values()
        users = User(full_name=full_name, email=email, level=1)
        users.set_password(password)
        db.session.add(users)
        db.session.commit()

        return response.success("", "Admin Successfuly Added.")
    except Exception as err:
        print("Error : ", err)


def login():
    try:
        email, password = request.form.values()

        user = User.query.filter_by(email=email).first()

        if not user:
            return response.bad_request([], "Email is not registered!")
        if not user.check_password(password):
            return response.bad_request([], "Incorrect Password!")

        data = {
            "id": user.id,
            "name": user.full_name,
            "email": user.email,
            "level": user.level,
        }
        expires = timedelta(days=7)
        expires_refresh = timedelta(days=7)

        access_token = create_access_token(data, fresh=True, expires_delta=expires)
        refresh_token = create_refresh_token(data, expires_delta=expires_refresh)

        return response.success(
            {
                "data": data,
                "access_token": access_token,
                "refresh_token": refresh_token,
            },
            "Login Success.",
        )

    except Exception as err:
        print("Error : ", err)
