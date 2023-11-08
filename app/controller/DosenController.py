from app.model.dosen import Dosen
from app.model.mahasiswa import Mahasiswa
from app.utils.utils import format_array, single_object

from app import response, app, db
from flask import request, jsonify, abort
import math


def index():
    try:
        dosen = Dosen.query.all()
        data = format_array(dosen)
        return response.success(data, "success")
    except Exception as err:
        print("Error =>>> ", err)


def single_detail_mahasiswa(dosen, mahasiswa):
    data = {
        "id": dosen.id,
        "nidn": dosen.nidn,
        "full_name": dosen.full_name,
        "phone": dosen.phone,
        "mahasiswa": mahasiswa,
    }

    return data


def detail(id):
    try:
        dosen = Dosen.query.filter_by(id=id).first()
        print(dosen)
        mahasiswa = Mahasiswa.query.filter(
            (Mahasiswa.first_dosen == id) | (Mahasiswa.second_dosen == id)
        )

        if not dosen:
            return response.bad_request([], "Dosen not found!")
        data_mahasiswa = format_array(mahasiswa)
        data = single_detail_mahasiswa(dosen, data_mahasiswa)
        return response.success(data, "success")

    except Exception as err:
        print("Error : ", err)


def save():
    try:
        nidn, full_name, phone, address = request.form.values()
        dosens = Dosen(nidn=nidn, full_name=full_name, phone=phone, address=address)

        db.session.add(dosens)
        db.session.commit()

        return response.success([request.form], "Data Successfuly Added.")
    except Exception as err:
        print("Error : ", err)


def update(id):
    try:
        dosen = Dosen.query.filter_by(id=id).first()
        # get_attr = [i for i in dosen.__dict__.keys() if i[:1] != "_"]
        # print(get_attr)
        for key in request.form.keys():
            setattr(dosen, key, request.form.get(key))

        db.session.commit()

        return response.success([request.form], "Data Successfuly Update.")
    except Exception as err:
        print("Error : ", err)


def delete(id):
    try:
        dosen = Dosen.query.filter_by(id=id).first()
        if not dosen:
            return response.bad_request([], "Data not found!")

        print(dosen)
        db.session.delete(dosen)
        db.session.commit()

        return response.success("", "Data Successfuly Deleted.")
    except Exception as err:
        print("Error : ", err)


def get_paginated_list(clss, url, start, limit):
    results = clss.query.all()
    data = format_array(results)
    count = len(data)
    print("limit =>", limit)
    if start == 0 or limit == 0:
        start = 1
        limit = 5

    obj = {}

    if count < start:
        obj["success"] = False
        obj["message"] = "You choose page(start) that out of total data!"
        return obj
    else:
        # make response
        obj["success"] = True
        obj["start_page"] = start
        obj["per_page"] = limit
        obj["total_data"] = count
        # ceil agar bilangan menjadi bulat ke atas
        obj["total_page"] = math.ceil(count / limit)
        # make URLs
        # make previous url
        if start == 1:
            obj["previous"] = ""
        else:
            start_copy = max(1, start - limit)
            limit_copy = start - 1
            obj["previous"] = url + "?start=%d&limit=%d" % (start_copy, limit_copy)
        # make next url
        if start + limit > count:
            obj["next"] = ""
        else:
            start_copy = start + limit
            obj["next"] = url + "?start=%d&limit=%d" % (start_copy, limit)
        obj["results"] = data[(start - 1) : (start - 1 + limit)]
        return obj


def paginate():
    start = request.args.get("start")
    limit = request.args.get("limit")

    try:
        # default display first page
        if start == None or limit == None:
            return jsonify(
                get_paginated_list(
                    Dosen,
                    "http://127.0.0.1:5000/api/dosen/page",
                    start=request.args.get("start", 1),
                    limit=request.args.get("limit", 5),
                )
            )
            # custom parameters
        else:
            return jsonify(
                get_paginated_list(
                    Dosen,
                    "http://127.0.0.1:5000/api/dosen/page",
                    start=int(start),
                    limit=int(limit),
                )
            )

    except Exception as err:
        print("Error : ", err)
