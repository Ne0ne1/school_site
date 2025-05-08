from flask import Flask, request, jsonify, render_template, redirect, url_for, session
from datetime import timedelta, datetime
from data_base import classes, students, subjects_data, student_subjects

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # В продакшене используйте сложный ключ!

# Настройки сессии
app.config.update(
    PERMANENT_SESSION_LIFETIME=timedelta(days=14),  # Срок жизни куки - 14 дней
    SESSION_COOKIE_SECURE=True,      # Только для HTTPS в production
    SESSION_COOKIE_HTTPONLY=True,    # Защита от XSS
    SESSION_COOKIE_SAMESITE='Lax',   # Защита от CSRF
    SESSION_REFRESH_EACH_REQUEST=True  # Обновлять срок при каждом запросе
)

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

@app.route('/')
@login_required()
def index():
    search_query = request.args.get('search', '').strip().lower()
    
    if search_query:
        filtered_students = [
            s for s in students 
            if (search_query in s['first_name'].lower() or 
                search_query in s['last_name'].lower())
        ]
    else:
        filtered_students = students
    
    last_students = students[-5:][::-1]
    
    return render_template(
        'admin_panel.html',
        classes=classes,
        students=students,
        filtered_students=filtered_students,
        last_students=last_students
    )

@app.route('/api/students', methods=['GET'])
def get_students():
    query = request.args.get('query', '').strip().lower()
    
    if not query:
        return jsonify([
            {
                'id': s['id'],
                'first_name': s['first_name'],
                'last_name': s['last_name'],
                'class': s['class']
            }
            for s in students
        ])
    
    result = [
        {
            'id': s['id'],
            'first_name': s['first_name'],
            'last_name': s['last_name'],
            'class': s['class']
        }
        for s in students 
        if (query in s['first_name'].lower() or 
            query in s['last_name'].lower())
    ]
    
    return jsonify(result)

@app.route('/add_student', methods=['GET', 'POST'])
@login_required(role='admin')
def add_student():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        class_name = request.form['class']
        new_student = {
            'id': len(students) + 1,
            'first_name': first_name,
            'last_name': last_name,
            'class': class_name
        }
        students.append(new_student)
        return redirect(url_for('index'))
    return render_template('add_student.html')

@app.route('/add_teacher', methods=['GET', 'POST'])
@login_required(role='admin')
def add_teacher():
    if request.method == 'POST':
        return redirect(url_for('index'))
    return render_template('add_teacher.html')

@app.route('/add_class', methods=['GET', 'POST'])
@login_required(role='admin')
def add_class():
    if request.method == 'POST':
        class_name = request.form['class_name']
        new_class = {'name': class_name, 'students': 0}
        classes.append(new_class)
        return redirect(url_for('index'))
    return render_template('add_class.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if not username or not password:
            return render_template('login.html', error='Заполните все поля')
            
        if username == 'admin' and password == 'admin':
            session.permanent = True  # Включаем постоянную сессию (14 дней)
            session['user'] = {
                'username': username,
                'role': 'admin',
                'login_time': datetime.now().isoformat()
            }
            return redirect(url_for('admin_panel'))
        elif username == 'student' and password == 'student':
            session.permanent = True
            session['user'] = {
                'username': username,
                'role': 'student',
                'login_time': datetime.now().isoformat()
            }
            return redirect(url_for('student_panel'))
        else:
            return render_template('login.html', error='Неверные учетные данные')
    
    return render_template('login.html')

@app.route('/admin')
@login_required(role='admin')
def admin_panel():
    return render_template('admin_panel.html')

@app.route('/student')
@login_required(role='student')
def student_panel():
    return render_template('student_panel.html', subjects=student_subjects)

@app.route('/logout')
def logout():
    session.clear()  # Полная очистка сессии
    return redirect(url_for('login'))

@app.route('/subject/<subject_name>')
@login_required(role='student')
def subject_detail(subject_name):
    subject_info = subjects_data.get(subject_name, [])
    return render_template('subject_detail.html', 
                         subject_name=subject_name, 
                         exams=subject_info)

if __name__ == '__main__':
    app.run(debug=True)