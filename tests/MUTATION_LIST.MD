
type Mutation {
    banUser(user: Int!, expires: Datetime!, reason: String!): Boolean
    removeUserBan(user: Int!): Boolean
    sendMessage(author: Int!, recipient: Int!, message: JSON!, newchat: Boolean!): Boolean!
    createTopic(name: String!, content:String!, user:Int!, category: Int, tags: String): MutationIdPayload
    closeTopic(topic: Int!): Boolean!
    reopenTopic(topic: Int!): Boolean!
    deleteTopic(topic: Int!): Boolean!
    createPost(user: Int!, topic:Int!, content:JSON!): Post!
    editPost(post: Int!, user: Int!, content: JSON!): EditPostResponse
    deletePost(post: Int! user: Int): MutationIdPayload
    createUser(username: String!, password: String!, email: String!): UserMutationPayload
    validateUser(token: String!): MutationIdPayload
    createCategory(name: String!, description: String!): Category!
    updatePassword(id: Int!, currentPass: String!, newPass: String!): MutationIdPayload
    uploadUserImage(image: Upload!, id: Int!): FileUploadResponse
    removeUserImage(id: Int!): Boolean
    updateEmail(id: Int!, email: String!): Boolean!
    updateProfile(id: Int!, status:String, about:String): MutationIdPayload
    increaseViewCount(topic:Int!): MutationIdPayload
    likePost(user:Int!, originator: Int!, topic: Int!, post: Int!): LikeMutationPayload
    flagPost(post: Int!, user:Int!, reason: Int!, text: String): Boolean
    removeFlag(post: Int!, user:Int!): RemoveFlagResponse
    removeLike(user:Int!, post: Int!): LikeMutationPayload
    bookmarkPost(user:Int!, post: Int!): BookmarkMutationPayload
    removeBookmark(user:Int!, post: Int!): BookmarkMutationPayload
    setMentions(link:String!, user:String!, mentioned:[String!]): Boolean
    markNotificationsRead(notifications: [Int!]): [Int!]
}
