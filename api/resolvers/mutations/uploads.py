from api.database.models import User
from os import path, remove
from api.resolvers.auth import login_required
from api.utils.upload_utils import save_spooled_file
from sqlalchemy.orm import Session
from api.engine import get_engine_from_context
from sqlalchemy import select

# UPLOAD CONFIG
# TODO: move this to the configuration folder.
UPLOAD_AVATAR_FOLDER = "static/avatars"
UPLOAD_IMAGE_FOLDER = "static/uploads"
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}


@login_required
def remove_image(_, info, id):
    db_engine = get_engine_from_context(info)
    with Session(db_engine) as session:
        user = session.query(User).filter_by(id=id).one()
        avatar = user.avatar
        user.avatar = None
        session.add(user)
        session.commit()
        remove(path.join(UPLOAD_AVATAR_FOLDER, avatar))
        return True


@login_required
def upload_user_image(_, info, image, id):
    upload_path = path.join(UPLOAD_AVATAR_FOLDER, image.filename)
    image_url = save_spooled_file(upload_path, image, ALLOWED_EXTENSIONS)
    db_engine = get_engine_from_context(info)
    if image_url is not None:
        with Session(db_engine) as session:
            # Save user.
            user = session.scalars(select(User).filter_by(id=id)).one()
            user.avatar = image.filename
            session.add(user)
            session.commit()

            return {"id": user.id, "url": image_url, "ok": True}
    else:
        return {"id": 0, "url": "", "ok": False}


@login_required
def upload_image(_, info, image):
    upload_path = path.join(UPLOAD_IMAGE_FOLDER, image.filename)
    image_url = save_spooled_file(upload_path, image, ALLOWED_EXTENSIONS)
    return {"src": image_url}
