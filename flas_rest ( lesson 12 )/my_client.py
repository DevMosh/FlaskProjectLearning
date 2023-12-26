from requests import get, post, put

# response = get(url='http://127.0.0.1:5000/posts', json={'name': 'SAeed'}).json()
# print(response)
#


# respone = post(url='http://127.0.0.1:5000/posts', json={'text': 'SAeed'})
# print(respone)
#
# response = post(url='http://127.0.0.1:5000/posts', json={'text': 'SAeed'}).json()
# print(response)

print(get('http://localhost:8080/posts/3').json())
# print(post('http://localhost:8080/posts',
#     json={
#         'title': 'Текст публикации',
#         'text': 'Текст публикации',
#         'author_id': 3
#           }).json())

print(put('http://localhost:8080/posts/5',
          json={
              'title': 'Текст публикацииииdsиии',
              'text': 'Текст публикациddsи',
              'author_id': 5
          }).json())
