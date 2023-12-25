from requests import get, post

# response = get(url='http://127.0.0.1:5000/posts', json={'name': 'SAeed'}).json()
# print(response)
#


# respone = post(url='http://127.0.0.1:5000/posts', json={'text': 'SAeed'})
# print(respone)
#
# response = post(url='http://127.0.0.1:5000/posts', json={'text': 'SAeed'}).json()
# print(response)

print(post(
    'http://localhost:8080/posts',
    json={'text': 'Текст публикации'}).json())

# print(put(url='http://127.0.0.1:5000/post/1').json())
