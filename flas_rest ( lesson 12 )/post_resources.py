from flask import jsonify, request
from flask_restful import Resource, reqparse, abort
from config import db
from models import Post


parser = reqparse.RequestParser()
parser.add_argument('title', required=True)
parser.add_argument('text', required=True)
parser.add_argument('author_id', required=True, type=int)


def abort_if_post_doesnt_exist(post_id):
    post = Post.query.get(post_id)
    if not post:
        abort(http_status_code=404,
              message=f"Post id={post_id} doesn't")


class PostListAPI(Resource):
    def get(self):
        posts = Post.query.all()
        return jsonify(
            {
                'posts': [
                    post.to_dict(only=('title', ))
                    for post in posts
                ]
            }
        )

    def post(self):
        args = parser.parse_args()
        post = Post(
            title=args['title'],
            text=args['text'],
            author_id=args['author_id']
        )

        db.session.add(post)
        db.session.commit()
        # Создание ответа с применением сериализатора.
        # return jsonify({'success': 'OK'})
        return jsonify(
            {
                # 'posts': post.to_dict(only=('text',))
                'success': 'ok'
            }
        )


class PostAPI(Resource):
    def get(self, post_id):
        abort_if_post_doesnt_exist(post_id)
        posts = Post.query.get_or_404(post_id)
        print(posts)
        return jsonify(
            {
                'posts': [
                    post.to_dict(only=('title',))
                    for post in posts
                ]
            }
        )

    def put(self, post_id):
        args = parser.parse_args()

        post_update = Post.query.get_or_404(post_id)
        post_update.title = args['title']
        post_update.text = args['text']
        post_update.text = args['author_id']

        db.session.commit()

        # Создание ответа с применением сериализатора.
        # return jsonify({'success': 'OK'})
        return jsonify(
            {
                'posts': post_update.to_dict(only=('title', 'text', 'author_id'))
            }
        )

    def delete(self, post_id):
        post = Post.query.get_or_404(post_id)
        db.session.delete(post)
        db.session.commit()
        return jsonify({
            'success': 'ok'
        })