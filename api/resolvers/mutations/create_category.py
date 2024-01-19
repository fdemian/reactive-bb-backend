from api.database.models import Category
from api.resolvers.auth import login_required
from sqlalchemy.orm import Session
from api.engine import get_engine_from_context


@login_required
def create_category(_, info, name, description):
    db_engine = get_engine_from_context(info)
    with Session(db_engine) as session:
        # Create new post.
        category = Category(name=name, description=description)
        session.add(category)
        session.commit()

        return {
            "id": category.id,
            "name": category.name,
            "description": category.description,
        }
