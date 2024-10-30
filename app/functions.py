import os.path
import secrets
from PIL import Image

from flask import current_app


def save_picture(picture):
    random_hex = secrets.token_hex(16)
    _, f_ext = os.path.splitext(picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.config['UPLOAD_PATH_FULL'], picture_fn)
    print(picture_path)
    output_size = (128, 128)
    i = Image.open(picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    return picture_fn