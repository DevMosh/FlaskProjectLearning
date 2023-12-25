
from flask import jsonify, request
# Подключаем родительский класс для создания классов ресурсов.
from flask_restful import Resource

from config import app, api, db
from models import Post


class PostListAPI(Resource):
    def get(self):
        posts = Post.query.all()
        return jsonify(
            {
                'posts': [
                    post.to_dict(only=('text', ))
                    for post in posts
                ]
            }
        )

    def post(self):
        data1 = request.json
        post = Post(text=data1['text'])
        db.session.add(post)
        db.session.commit()
        # Создание ответа с применением сериализатора.
        # return jsonify({'success': 'OK'})
        return jsonify(
            {
                'posts': post.to_dict(only=('text',))
            }
        )


class PostAPI(Resource):
    def get(self, post_id):
        return {'title': f'GET {post_id}'}

    def put(self, post_id):
        return {'title': f'PUT {post_id}'}

    def delete(self, post_id):
        return {'message': f'DELETE {post_id}'}


# Добавление данных о классах и соответствующих им URL в API.
api.add_resource(PostListAPI, '/posts')
api.add_resource(PostAPI, '/posts/<int:post_id>')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(port=8080, host='127.0.0.1', debug=True)



