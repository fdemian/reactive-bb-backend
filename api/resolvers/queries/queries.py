from ariadne import QueryType
from api.resolvers.queries.user import resolve_user
from api.resolvers.queries.topics import (
    resolve_topics,
    resolve_topic,
    resolve_topics_by_user,
    get_pinned_topics,
)
from api.resolvers.queries.posts import (
    resolve_posts,
    resolve_post_link,
    resolve_posts_by_user,
)
from api.resolvers.queries.flagged_posts import resolve_flagged_posts
from api.resolvers.queries.categories import resolve_categories, resolve_category
from api.resolvers.queries.likes import get_likes_by_user
from api.resolvers.queries.bookmarks import (
    resolve_bookmarks_by_user,
    resolve_bookmarks_by_post_list,
)
from api.resolvers.queries.config import resolve_config
from api.resolvers.queries.search import resolve_search
from api.resolvers.queries.mentions import resolve_mention_candidates
from api.resolvers.queries.checkUsername import resolve_user_availability
from api.resolvers.queries.notifications import (
    resolve_notifications,
    resolve_all_notifications,
)
from api.resolvers.queries.chats import resolve_user_chats, resolve_chat
from api.resolvers.queries.post_edits import resolve_post_edits

queries = QueryType()
queries.set_field("getUser", resolve_user)
queries.set_field("topics", resolve_topics)
queries.set_field("topic", resolve_topic)
queries.set_field("topicsByUser", resolve_topics_by_user)
queries.set_field("pinnedTopics", get_pinned_topics)
queries.set_field("posts", resolve_posts)
queries.set_field("flaggedPosts", resolve_flagged_posts)
queries.set_field("postsByUser", resolve_posts_by_user)
queries.set_field("categories", resolve_categories)
queries.set_field("category", resolve_category)
queries.set_field("likesByUser", get_likes_by_user)
queries.set_field("bookmarksByUser", resolve_bookmarks_by_user)
queries.set_field("bookmarksByPostList", resolve_bookmarks_by_post_list)
queries.set_field("config", resolve_config)
queries.set_field("search", resolve_search)
queries.set_field("postLink", resolve_post_link)
queries.set_field("mentionCandidates", resolve_mention_candidates)
queries.set_field("checkUsername", resolve_user_availability)
queries.set_field("notifications", resolve_notifications)
queries.set_field("allNotifications", resolve_all_notifications)
queries.set_field("chatsByUser", resolve_user_chats)
queries.set_field("chat", resolve_chat)
queries.set_field("postEdits", resolve_post_edits)
