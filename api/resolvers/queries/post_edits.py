from api.database.models import PostEdits
from sqlalchemy import select, func
from sqlalchemy.orm import Session
from api.engine import get_engine_from_context
from api.resolvers.auth import admin_required


def map_post_edits(p):
    return {
        "user": {"id": p.user.id, "avatar": p.user.avatar, "username": p.user.username},
        "date": p.date,
        "previous": p.previous_text,
        "current": p.current_text,
    }


@admin_required
def resolve_post_edits(_, info, offset, limit):
    # await log_request(info)
    db_engine = get_engine_from_context(info)
    with Session(db_engine) as session:
        post_edits = session.scalars(
            select(PostEdits)
            .order_by(PostEdits.date.desc())
            .limit(limit)
            .offset(offset)
        ).all()

        mapped_post_edits = map(map_post_edits, post_edits)

        post_edits_count = session.scalar(select(func.count(PostEdits.date)))

        return {"postEdits": mapped_post_edits, "editsCount": post_edits_count}
