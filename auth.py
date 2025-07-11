from flask import Blueprint, request, redirect, url_for, session, render_template
from models import AuthSessionLocal, UserAuth
from werkzeug.security import check_password_hash, generate_password_hash

auth_bp = Blueprint('auth', __name__)

def get_auth_db():
    return AuthSessionLocal()

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        login_input = request.form['login']
        password_input = request.form['password']
        db = get_auth_db()
        user = db.query(UserAuth).filter_by(login=login_input).first()
        db.close()

        if user and check_password_hash(user.password, password_input):
            session.clear()
            session.permanent = True
            session['user_id'] = user.id
            session['permissions'] = user.permissions

            # Перенаправление в зависимости от роли
            if user.permissions == 'admin':
                return redirect(url_for('index'))  # index есть в app.py
            elif user.permissions == 'student':
                return redirect(url_for('student_panel'))  # есть в app.py
            elif user.permissions == 'teacher':
                return redirect(url_for('teacher_panel'))  # есть в app.py
            else:
                return redirect(url_for('student_panel'))  # fallback

        return render_template('login.html', error='Неверные логин или пароль')
    
    return render_template('login.html')

@auth_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))

# Утилита для создания пользователя с проверкой permissions
def create_user(login, password, permissions='student'):
    valid_permissions = {'admin', 'student', 'teacher'}
    if permissions not in valid_permissions:
        permissions = 'student'  # fallback
    db = get_auth_db()
    hashed = generate_password_hash(password)
    new_user = UserAuth(login=login, password=hashed, permissions=permissions)
    db.add(new_user)
    db.commit()
    db.close()
    return new_user
