# init_db.py
from models import auth_engine, auth_Base, UserAuth
from werkzeug.security import generate_password_hash
from sqlalchemy.orm import sessionmaker

def init_auth_db():
    auth_Base.metadata.create_all(bind=auth_engine)
    Session = sessionmaker(bind=auth_engine)
    db = Session()
    if not db.query(UserAuth).filter_by(login='admin').first():
        db.add(UserAuth(
            login='admin',
            password=generate_password_hash('adminpass'),
            permissions='admin'
        ))
        db.commit()
    db.close()
    print("Auth DB initialized with default admin/adminpass")

if __name__ == '__main__':
    init_auth_db()