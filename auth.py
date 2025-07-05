from flask import Blueprint, request, redirect, url_for, session, render_template
from models import AuthSessionLocal, UserAuth
from werkzeug.security import check_password_hash, generate_password_hash

auth_bp = Blueprint('auth', __name__)

def get_auth_db():
    """Получить сессию для базы аутентификации"""
    return AuthSessionLocal()

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        login_input = request.form['login']
        password_input = request.form['password']
        db = get_auth_db()
        user = db.query(UserAuth).filter_by(login=login_input).first()
        if user and check_password_hash(user.password, password_input):
            session.clear()
            session.permanent = True
            session['user_id'] = user.id
            session['permissions'] = user.permissions
            return redirect(url_for('index'))
        else:
            return render_template('login.html', error='Неверные логин или пароль')
    return render_template('login.html')

@auth_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))

# Утилита для создания нового пользователя (для скриптов)
def create_user(login, password, permissions='student'):
    db = get_auth_db()
    hashed = generate_password_hash(password)
    new_user = UserAuth(login=login, password=hashed, permissions=permissions)
    db.add(new_user)
    db.commit()
    db.close()
    return new_user
