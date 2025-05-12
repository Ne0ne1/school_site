from flask import Flask, request, jsonify, render_template, redirect, url_for, session
from datetime import timedelta, datetime
from models import db, User, Class, Subject
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # ЗАМЕНИТЬ НА НАСТОЯЩИЙ КЛЮЧ В ПРОДАКШЕНЕ

# Настройки сессии
app.config.update(
    PERMANENT_SESSION_LIFETIME=timedelta(days=14),
    SESSION_COOKIE_SECURE=True,
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE='Lax',
    SESSION_REFRESH_EACH_REQUEST=True
)

# Настройки БД
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///school.db'  # или PostgreSQL URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# --- Аутентификация и роли ---

def is_authenticated(required_role=None):
    user = session.get('user')
    if not user:
        return False
    if required_role and user.get('role') != required_role:
        return False
    return True

def login_required(role=None):
    def decorator(func):
        def wrapper(*args, **kwargs):
            if not is_authenticated(role):
                return redirect(url_for('login'))
            return func(*args, **kwargs)
        wrapper.__name__ = func.__name__
        return wrapper
    return decorator

# --- Маршруты ---

@app.route('/')
@login_required()
def index():
    students = User.query.filter_by(role='student').all()
    classes = Class.query.all()
    return render_template(
        'admin_panel.html',
        students=students,
        classes=classes,
        filtered_students=students,
        last_students=students[-5:]
    )

@app.route('/add_student', methods=['GET', 'POST'])
@login_required(role='admin')
def add_student():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        username = request.form['username']
        password = request.form['password']
        class_id = request.form['class_id']

        password_hash = generate_password_hash(password)

        new_user = User(
            username=username,
            password_hash=password_hash,
            role='student',
            class_id=class_id
        )
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('index'))

    classes = Class.query.all()
    return render_template('add_student.html', classes=classes)

@app.route('/add_class', methods=['GET', 'POST'])
@login_required(role='admin')
def add_class():
    if request.method == 'POST':
        class_name = request.form['class_name']
        new_class = Class(name=class_name)
        db.session.add(new_class)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('add_class.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password_hash, password):
            session.permanent = True
            session['user'] = {
                'username': user.username,
                'role': user.role,
                'user_id': user.id,
                'login_time': datetime.now().isoformat()
            }
            if user.role == 'admin':
                return redirect(url_for('admin_panel'))
            elif user.role == 'student':
                return redirect(url_for('student_panel'))
            elif user.role == 'moderator':
                return redirect(url_for('moderator_panel'))  # реализация позже
        else:
            return render_template('login.html', error='Неверные данные')
    return render_template('login.html')

@app.route('/admin')
@login_required(role='admin')
def admin_panel():
    students = User.query.filter_by(role='student').all()
    classes = Class.query.all()
    return render_template('admin_panel.html', students=students, classes=classes)

@app.route('/student')
@login_required(role='student')
def student_panel():
    user_id = session['user']['user_id']
    user = User.query.get(user_id)
    subjects = Subject.query.filter_by(class_id=user.class_id).all()
    return render_template('student_panel.html', subjects=subjects)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))


@app.route('/add_teacher', methods=['GET', 'POST'])
@login_required(role='admin')
def add_teacher():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        from werkzeug.security import generate_password_hash

        new_teacher = User(
            username=username,
            password_hash=generate_password_hash(password),
            role='moderator'
        )
        db.session.add(new_teacher)
        db.session.commit()
        return redirect(url_for('admin_panel'))

    return render_template('add_teacher.html')



# Запуск
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
