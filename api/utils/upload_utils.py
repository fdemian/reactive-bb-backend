from os import path, getcwd
import shutil


def allowed_file(filename, ALLOWED_EXTENSIONS):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def save_spooled_file(upload_path, image, ALLOWED_EXTENSIONS):
    if allowed_file(image.filename, ALLOWED_EXTENSIONS):
        save_path = path.join(getcwd(), upload_path)
        image_url = image.filename
        #
        image.file.seek(0)
        new_file = open(save_path, "wb+")
        shutil.copyfileobj(image.file, new_file)
        return image_url
    else:
        return None
