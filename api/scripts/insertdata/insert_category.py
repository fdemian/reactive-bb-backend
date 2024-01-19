from api.database.models import Category

category = {"name": "A category", "description": "A description"}


def insert_test_category(session, name, description):
    category = Category()
    category.name = name
    category.description = description
    session.add(category)
    session.commit()
    return category.id
