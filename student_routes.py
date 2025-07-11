# student_routes.py
from flask import Blueprint, render_template, request, redirect, url_for
from functools import wraps
from models import SchoolSessionLocal, AuthSessionLocal, Class, Student, UserAuth
from werkzeug.security import generate_password_hash
from decorators import login_required


# 👇 Blueprint
student_bp = Blueprint('student_bp', __name__)

@student_bp.route('/add_student', methods=['GET', 'POST'])
@login_required(role='admin')
def add_student():
    school_db = SchoolSessionLocal()
    auth_db = AuthSessionLocal()

    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        username = request.form['username']
        password = request.form['password']
        class_id = request.form['class_id']

        # 1. Добавляем в auth_db
        hashed_password = generate_password_hash(password)
        new_auth = UserAuth(
            login=username,
            password=hashed_password,
            permissions='student'
        )
        auth_db.add(new_auth)
        auth_db.commit()
        auth_db.refresh(new_auth)

        # 2. Добавляем в school_db
        fullname = f"{last_name} {first_name}"
        new_student = Student(
            fullname=fullname,
            class_id=int(class_id),
            auth_id=new_auth.id
        )
        school_db.add(new_student)
        school_db.commit()

        auth_db.close()
        school_db.close()
        return redirect(url_for('index'))

    # GET-запрос — показать форму
    classes = school_db.query(Class).all()
    school_db.close()
    return render_template('add_student.html', classes=classes)
