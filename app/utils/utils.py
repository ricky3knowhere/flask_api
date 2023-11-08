def format_array(datas):
    array = []
    for i in datas:
        array.append(single_object(i))
    return array


def single_object(datas):
    data = {}
    if hasattr(datas, 'nim'):
        data = {
            "id": datas.id,
            "nim": datas.nim,
            "full_name": datas.full_name,
            "phone": datas.phone,
        }
    else:
        data = {
            "id": datas.id,
            "nidn": datas.nidn,
            "full_name": datas.full_name,
            "phone": datas.phone,
            "address": datas.address,
        }
    return data


# def fetch_post_data(form_data):
#     # get params
#     input_data = {}

#     for key in form_data:
#         input_data[key] = form_data.get(key)

#     return input_data
