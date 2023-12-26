from flask import Blueprint

analytics_blueprint = Blueprint(
    'analytics',
    __name__,
    template_folder='templates'
)


@analytics_blueprint.route('/analytics')
def get_analytics():
    return 'аналитика по нашему сервису'