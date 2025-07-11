import re
from flask import Blueprint, request, render_template, redirect, url_for
from sqlalchemy.exc import IntegrityError, OperationalError
from models import SchoolSessionLocal, Class
from decorators import login_required

class_bp = Blueprint('class_bp', __name__)

# Шаблон: 1–9 или 10–11, затем одна буква 
CLASS_PATTERN = re.compile(r'^(?:[1-9]|1[0-1])[А-ЯЁ]$')  # Только русские буквы


@class_bp.route('/add_class', methods=['GET', 'POST'])
@login_required(role='admin')
def add_class():
    error = None
    db = SchoolSessionLocal()
    if request.method == 'POST':
        name = request.form.get('class_name', '').strip().upper()
        
        db.query(Class).filter(Class.title == name).exists()
        db.rollback()
        error = f'Класс «{name}» уже существует в базе.'
    try:
                db.add(Class(title=name))
                db.commit()
                return redirect(url_for('index'))
    except IntegrityError:
                db.rollback()
                error = f'Класс «{name}» уже существует в базе.'
    except OperationalError:
                db.rollback()
                error = 'Ошибка БД: таблицы не найдены. Запустите init_school_db.py.'
    except Exception as ex:
                db.rollback()
                error = f'Непредвиденная ошибка: {ex}'
    finally:
                db.close()

    # При GET или при наличии ошибки показываем форму с сообщением
    return render_template('add_class.html', error=error)
