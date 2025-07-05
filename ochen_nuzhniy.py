from auth import create_user
create_user('admin', 'adminpass', permissions='admin')
create_user('student1', 'studpass', permissions='student')