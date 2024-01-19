from os import path
import uuid

current_dir = path.dirname(path.realpath(__file__))

image_file_name = "sample.png"
sample_image_file_path = path.join(current_dir, image_file_name)

text_file_name = "sample.txt"
text_file_path = path.join(current_dir, image_file_name)


def get_sample_file_contents():
    f = open(sample_image_file_path, "rb+")
    return {"content": f, "name": image_file_name}


def get_sample_txt_contents():
    f = open(text_file_path, "rb+")
    return {"content": f, "name": text_file_name}


def get_fr_data_headers(token):
    boundary = "boundary=------{}".format(uuid.uuid4())
    multipart_header = "multipart/form-data; " + boundary
    return {
        "content-type": multipart_header,
        "accept": "application/json",
        "access_token": token,
    }
