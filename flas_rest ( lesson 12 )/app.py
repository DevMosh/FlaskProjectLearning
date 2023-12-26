

from config import app, api, db
from post_resources import PostListAPI, PostAPI
import analytics

# Добавление данных о классах и соответствующих им URL в API.
api.add_resource(PostListAPI, '/posts')
api.add_resource(PostAPI, '/posts/<int:post_id>')
app.register_blueprint(analytics.analytics_blueprint)


# @app.errorhandler(404)
# def page_not_found(error):
#     return "Not found", 404

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(port=8080, host='127.0.0.1', debug=True)



