from server import app
from models import db, User, Class, Subject
from werkzeug.security import generate_password_hash

with app.app_context():
    db.drop_all()
    db.create_all()  # создаст таблицы, если их ещё нет

    cls = Class(name="10-А")
    db.session.add(cls)
    db.session.commit()

    admin = User(
        username='admin',
        password_hash=generate_password_hash('1'),  # пароль: admin123
        role='admin'
    )
    db.session.add(admin)
    
    student = User(
        username="student",
        password_hash=generate_password_hash("1"),
        role="student",
        class_id=cls.id
    )
    db.session.add(student)

    teacher = User(
        username="teacher1",
        password_hash=generate_password_hash("qwerty"),
        role="moderator"
    )
    db.session.add(teacher)

    db.session.commit()
    print("Данные успешно добавлены")
