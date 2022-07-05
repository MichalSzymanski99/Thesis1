from sqlalchemy.orm import backref
from webapp import db, login_manager
from webapp import bcrypt
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return Student.query.get(int(user_id))

student_identifier = db.Table('student_identifier',
    db.Column('Student_id', db.Integer, db.ForeignKey('student.id')),
    db.Column('Curses_id', db.Integer, db.ForeignKey('item.id'))
)

class Student(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key = True)
    Name = db.Column(db.String(length = 30), nullable = False, unique = False)
    Surname = db.Column(db.String(length = 30), nullable = False, unique = False)
    Code = db.Column(db.String(length = 6), nullable = False, unique = True)
    Password = db.Column(db.String(length = 60), nullable = False, unique = False)
    Semester = db.Column(db.String(length = 3), nullable = False, unique = False)
    Area = db.Column(db.String(length = 30), nullable = False, unique = False)
   # Courses = db.relationship('Item', backref = 'owned_user', lazy = True)

    @property
    def password_hash(self):
        return self.password_hash

    @password_hash.setter
    def password_hash(self, plain_text_password):
        self.Password = bcrypt.generate_password_hash(plain_text_password).decode('utf-8')

    def check_password_correction(self, attempted_password):
        return bcrypt.check_password_hash(self.Password, attempted_password)

class Item(db.Model):
    id = db.Column(db.Integer(), primary_key = True)
    Name = db.Column(db.String(length = 30), nullable = False, unique = True)
    Code = db.Column(db.String(length = 5), nullable = False, unique = True)
    Lecturer = db.Column(db.String(length = 30), nullable = False, unique = False)
    Description = db.Column(db.String(length = 1000), nullable = False, unique = True)
    Children = db.relationship("Student", secondary=student_identifier, backref=db.backref('Courses', lazy = 'dynamic'))

    def __repr__(self):
        return f'Course {self.Name}'


class FileContents(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(length = 5), unique = False)
    name = db.Column(db.String(200))
    data = db.Column(db.LargeBinary)

class FileContents2(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(length = 5), unique = False)
    name = db.Column(db.String(200))
    data = db.Column(db.LargeBinary)

class Videos(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(length = 5), unique = False)
    name = db.Column(db.String(200))
    data = db.Column(db.LargeBinary)