
# from api.scripts.insert_test_data import user
# from api.scripts.insert_test_data import user


# @pytest.mark.asyncio
# async def test_notification_query(setup_test_database):
#      client = TestClient(app)
#
#      # Log in to the application
#      login_data = json.dumps({'username': user['username'], 'password': user['password']})
#      login_resp = client.post("/api/login", data=login_data)
#      access_token = login_resp.cookies['access_token']
#
#      notification_query = """
#      subscription NotificationAdded($user: Int!) {
#        notificationAdded(user: $user) {
#          link
#          type
#          read
#          originator {
#            id
#            avatar
#            username
#          }
#          user {
#            id
#            avatar
#            username
#          }
#        }
#      }
#      """
#
#      with client.websocket_connect("/api/subscriptions", ["graphqlws"]) as ws:
#          ws.send_json({"type": GraphQLTransportWSHandler.GQL_CONNECTION_INIT})
#          ws.send_json({
#              "type": GraphQLTransportWSHandler.GQL_SUBSCRIBE,
#              "payload": {
#                  "query": notification_query,
#                  "variables": {
#                      "user": 1
#                  }
#              }
#          })
#          response = ws.receive_json()
#          assert response["type"] == GraphQLTransportWSHandler.GQL_CONNECTION_ACK
#
#          # Like post
#          query_mut = """mutation LikePost($user: Int!, $originator: Int!, $topic: Int!, $post: Int!) {
#                 likePost(user: $user, originator: $originator, topic: $topic, post: $post) {
#                   id
#                   ok
#                   postId
#                   likes
#                 }
#               }
#             """
#          data_mut = {
#              "operationName": "LikePost",
#              "query": query_mut.replace('\n', '').strip(),
#              "variables": {
#                  "user": 1,
#                  "originator": 1,
#                  "topic": 1,
#                  "post": 1
#              }
#          }
#          headers_mut = {
#              'content-type': 'application/json',
#              'access_token': access_token
#          }
#          response_mut = client.post("/api/graphql", headers=headers_mut, data=json.dumps(data_mut))
#          assert response_mut.status_code == 200
#
#          response = ws.receive_json()
#          assert response["type"] == GraphQLTransportWSHandler.GQL_NEXT
#          print(response)
#
#          assert True is False
