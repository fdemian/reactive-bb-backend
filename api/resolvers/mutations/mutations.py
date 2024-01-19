from ariadne import MutationType
from api.resolvers.mutations.create_topic import (
    create_topic,
    close_topic,
    delete_topic,
    reopen_topic,
    pin_topic,
    increase_view_count,
)
from api.resolvers.mutations.post import create_post, edit_post, delete_post
from api.resolvers.mutations.create_category import create_category
from api.resolvers.mutations.user_mutations import (
    update_password,
    update_email,
    update_profile,
)
from api.resolvers.mutations.uploads import (
    upload_user_image,
    upload_image,
    remove_image,
)
from api.resolvers.mutations.create_user import create_user
from api.resolvers.mutations.validate_user import validate_user
from api.resolvers.mutations.like_post import like_post, remove_like
from api.resolvers.mutations.flag_post import flag_post, remove_flag
from api.resolvers.mutations.bookmark_post import bookmark_post, remove_bookmark
from api.resolvers.mutations.set_mentions import set_mentions
from api.resolvers.mutations.send_message import send_message
from api.resolvers.mutations.mark_notifications_read import mark_notifications_read
from api.resolvers.mutations.ban_users import ban_user, remove_user_ban
from api.resolvers.mutations.reset_password import (
    reset_password_request,
    reset_password,
)

# Mutation fields.
mutations = MutationType()
mutations.set_field("createTopic", create_topic)
mutations.set_field("closeTopic", close_topic)
mutations.set_field("deleteTopic", delete_topic)
mutations.set_field("reopenTopic", reopen_topic)
mutations.set_field("pinTopic", pin_topic)
mutations.set_field("createPost", create_post)
mutations.set_field("editPost", edit_post)
mutations.set_field("deletePost", delete_post)
mutations.set_field("increaseViewCount", increase_view_count)
mutations.set_field("createCategory", create_category)
mutations.set_field("updatePassword", update_password)
mutations.set_field("uploadUserImage", upload_user_image)
mutations.set_field("uploadImage", upload_image)
mutations.set_field("removeUserImage", remove_image)
mutations.set_field("updateEmail", update_email)
mutations.set_field("updateProfile", update_profile)
mutations.set_field("createUser", create_user)
mutations.set_field("validateUser", validate_user)
mutations.set_field("likePost", like_post)
mutations.set_field("flagPost", flag_post)
mutations.set_field("removeFlag", remove_flag)
mutations.set_field("removeLike", remove_like)
mutations.set_field("bookmarkPost", bookmark_post)
mutations.set_field("removeBookmark", remove_bookmark)
mutations.set_field("setMentions", set_mentions)
mutations.set_field("sendMessage", send_message)
mutations.set_field("markNotificationsRead", mark_notifications_read)
mutations.set_field("banUser", ban_user)
mutations.set_field("removeUserBan", remove_user_ban)
mutations.set_field("resetPasswordRequest", reset_password_request)
mutations.set_field("resetPassword", reset_password)
