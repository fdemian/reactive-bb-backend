from ariadne import make_executable_schema, upload_scalar, ObjectType
from api.resolvers.mutations.mutations import mutations
from api.resolvers.queries.queries import queries
from api.resolvers.subscriptions.subscriptions import subscriptions
from ariadne import load_schema_from_path
from ariadne import ScalarType

datetime_scalar = ScalarType("Datetime")


@datetime_scalar.serializer
def serialize_datetime(value):
    return value.isoformat()


# Like object
like = ObjectType("Like")
like.set_alias("userId", "user_id")
like.set_alias("postId", "post_id")

# Bookmark object
bookmark = ObjectType("Bookmark")
bookmark.set_alias("userId", "user_id")
bookmark.set_alias("postId", "post_id")

# Post object
post = ObjectType("Post")
post.set_alias("topicId", "topic_id")

# User object
user = ObjectType("User")
user.set_alias("banReason", "ban_reason")
user.set_alias("banExpires", "ban_expires")
user.set_alias("lockoutTime", "lockout_time")

# Flagged post
flagged_post = ObjectType("FlaggedPost")
flagged_post.set_alias("postId", "post_id")
flagged_post.set_alias("userId", "user_id")
flagged_post.set_alias("reasonId", "reason_id")
flagged_post.set_alias("reasonText", "reason_text")

type_defs = load_schema_from_path("./api/schema.graphql")
graphl_schema = make_executable_schema(
    type_defs,
    [
        queries,
        mutations,
        subscriptions,
        upload_scalar,
        like,
        bookmark,
        post,
        user,
        flagged_post,
        datetime_scalar,
    ],
)
