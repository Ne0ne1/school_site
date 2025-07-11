# models.py
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

# --------------------
# Configuration: adjust these URLs to point to your databases.
AUTH_DATABASE_URL = "sqlite:///auth_db.sqlite"
SCHOOL_DATABASE_URL = "sqlite:///school_db.sqlite"

# For PostgreSQL later:
# AUTH_DATABASE_URL = "postgresql://user:pass@host:port/auth_db"
# SCHOOL_DATABASE_URL = "postgresql://user:pass@host:port/school_db"
# --------------------

# Engines
auth_engine = create_engine(AUTH_DATABASE_URL, echo=True)
school_engine = create_engine(SCHOOL_DATABASE_URL, echo=True)

# Bases
auth_Base = declarative_base()
school_Base = declarative_base()

# Session makers
AuthSessionLocal = sessionmaker(bind=auth_engine)
SchoolSessionLocal = sessionmaker(bind=school_engine)

# --------------------
# Models for auth_db
class UserAuth(auth_Base):
    __tablename__ = 'user_auth'
    id = Column(Integer, primary_key=True, index=True)
    login = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    permissions = Column(String, nullable=False)  # 'student', 'teacher', 'admin'

# --------------------
# Models for school_db
class Class(school_Base):
    __tablename__ = 'classes'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, unique=True, nullable=False)
    students = relationship("Student", back_populates="class_")
    tasks = relationship("Task", back_populates="class_")

class Subject(school_Base):
    __tablename__ = 'subjects'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, unique=True, nullable=False)
    tasks = relationship("Task", back_populates="subject")

class Student(school_Base):
    __tablename__ = 'students'
    id = Column(Integer, primary_key=True, index=True)
    fullname = Column(String, nullable=False)
    class_id = Column(Integer, ForeignKey('classes.id'), nullable=False)
    auth_id = Column(Integer, nullable=False)  # no FK to auth_db

    class_ = relationship("Class", back_populates="students")
    submissions = relationship("Submission", back_populates="student")

class Teacher(school_Base):
    __tablename__ = 'teachers'
    id = Column(Integer, primary_key=True, index=True)
    fullname = Column(String, nullable=False)
    auth_id = Column(Integer, nullable=False)  # no FK

class Task(school_Base):
    __tablename__ = 'tasks'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    pdf_link = Column(String)
    date_time = Column(DateTime)
    class_id = Column(Integer, ForeignKey('classes.id'), nullable=False)
    subject_id = Column(Integer, ForeignKey('subjects.id'), nullable=False)

    class_ = relationship("Class", back_populates="tasks")
    subject = relationship("Subject", back_populates="tasks")
    submissions = relationship("Submission", back_populates="task")

class Submission(school_Base):
    __tablename__ = 'submissions'
    id = Column(Integer, primary_key=True, index=True)
    assignment_id = Column(Integer, ForeignKey('tasks.id'), nullable=False)
    student_id = Column(Integer, ForeignKey('students.id'), nullable=False)
    pdf_file = Column(String)
    grade = Column(String)
    comment = Column(Text)

    task = relationship("Task", back_populates="submissions")
    student = relationship("Student", back_populates="submissions")

# --------------------
# Init functions
def init_auth_db():
    auth_Base.metadata.create_all(bind=auth_engine)

def init_school_db():
    school_Base.metadata.create_all(bind=school_engine)

if __name__ == "__main__":
    # choose one or both
    init_auth_db()
    init_school_db()