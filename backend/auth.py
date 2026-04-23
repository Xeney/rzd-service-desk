from flask_login import LoginManager
from flask import jsonify
from models import User

login_manager = LoginManager()
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


def init_auth(app):
    login_manager.init_app(app)
    
    @login_manager.unauthorized_handler
    def handle_unauthorized():
        return jsonify({'error': 'Требуется авторизация'}), 401