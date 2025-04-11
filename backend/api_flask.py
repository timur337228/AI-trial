import os
from flask import (
    Blueprint, request, jsonify, Response, send_from_directory,
    make_response, current_app, stream_with_context
)
from werkzeug.utils import secure_filename
from flask_login import current_user, login_required
import secrets
from functools import wraps
from models import User  # Предполагается, что у вас есть модель User с SQLAlchemy

# Инициализация Blueprints
ai_bp = Blueprint('ai', __name__, url_prefix='/ai')
auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

# Конфигурация
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'static')
ALLOWED_EXTENSIONS = {'pdf'}


# Вспомогательные функции
def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# Аутентификация и авторизация
def get_current_user():
    # Ваша реализация получения пользователя из кук/сессии
    pass


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            return jsonify({"error": "Unauthorized"}), 401
        return f(*args, **kwargs)

    return decorated_function


# AI Routes
@ai_bp.route('/upload/', methods=['POST'])
@login_required
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if file and allowed_file(file.filename):
        filename = secure_filename(f"{current_user.email}.pdf")
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(file_path)

        text = pdf_to_text(filename)

        def generate():
            for chunk in get_completion_stream(message=text):
                yield chunk

        return Response(stream_with_context(generate()), mimetype='text/plain')

    return jsonify({"error": "Invalid file type"}), 400


# Auth Routes
@auth_bp.route('/register/', methods=['POST'])
def register_auth_user_jwt():
    # Реализация регистрации пользователя
    return jsonify({"message": "Good reg, confirm email"})


@auth_bp.route('/login/', methods=['POST'])
def auth_user_jwt():
    # Реализация аутентификации
    response = make_response(jsonify({"status": "success"}))
    response.set_cookie(
        key='session_id',
        value=secrets.token_urlsafe(),
        secure=True,
        httponly=True,
        samesite='Strict'
    )
    return response


@auth_bp.route('/user/me/')
@login_required
def auth_user_check_self_info():
    return jsonify({
        "first_name": current_user.first_name,
        "last_name": current_user.last_name,
        "email": current_user.email
    })


@auth_bp.route('/confirm-email/')
def confirm_email():
    token = request.args.get('token')
    user = confirm_email_confirmation_token(token)
    # Установка кук и логика подтверждения
    return jsonify({'message': 'Good confirm Email'})


@auth_bp.route('/logout/')
@login_required
def logout():
    # Логика выхода
    response = make_response(jsonify({"message": "Logout successful"}))
    response.delete_cookie('session_id')
    return response