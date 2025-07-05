# init_school_db.py
from models import school_engine, school_Base

def init_school_db():
    school_Base.metadata.create_all(bind=school_engine)
    print("School DB initialized with tables: classes, subjects, students, teachers, tasks, submissions")

if __name__ == '__main__':
    init_school_db()