type Subscription {
    notificationAdded(user: Int!): NotificationResponse
    chatAdded(userA: Int!, userB: Int!): ChatMessage
    chatNotification(user: Int!): ChatNotification
}