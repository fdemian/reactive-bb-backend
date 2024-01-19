
type Query {
    getUser(id:Int!): User
    topics(offset: Int!, limit: Int!): TopicsReponse!
    topic(id: Int!): Topic
    posts(topicId: Int!, offset: Int!, limit: Int!): [Post!]
    flaggedPosts(offset: Int!, limit: Int!): [FlaggedPost!]
    search(term: String!, where: [String!], offset: Int!, limit: Int!): SearchResponse
    postLink(post: Int!, itemscount: Int!): PostLinkResponse!
    categories: [Category!]
    category(id: Int!): Category!
    likes: [Like!]
    likesByUser(id: Int!): [Like!]
    topicsByUser(id: Int!): [Topic!]
    postsByUser(id: Int!): [Post!]
    mentionCandidates(search: String!): [User!]
    bookmarksByUser(user: Int!): [Bookmark!]
    bookmarksByPostList(user: Int!, posts: [Int!]): [Bookmark!]
    config: Config!
    checkUsername(username: String!): CheckUsernameResponse!
    notifications(user: Int!): [NotificationResponse!]
    allNotifications(user: Int!, limit: Int!, offset: Int!): [NotificationResponse!]
    chatsByUser(user: Int!): [User!]
    chat(userA: Int!, userB: Int!, offset: Int!, limit: Int!): [ChatMessage!]
}