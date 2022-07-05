from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms import validators
from wtforms.fields.numeric import IntegerField
from wtforms.validators import EqualTo, DataRequired, ValidationError
from webapp.models import Student

class RegisterForm(FlaskForm):

    def validate_Code(self, Code_to_check):
        student = Student.query.filter_by(Code=Code_to_check.data).first()
        if student:
            raise ValidationError('Student with this StudentID already exists')

    Name = StringField(label = 'Name:', validators=[DataRequired()])
    Surname = StringField(label = 'Surname:', validators=[DataRequired()])
    Code = StringField(label = 'User ID:', validators=[DataRequired()])
    Password1 = PasswordField(label = 'Password:', validators=[DataRequired()])
    Password2 = PasswordField(label = 'Confirm Password:', validators=[EqualTo('Password1'), DataRequired()])
    Semester = StringField(label = 'Semester:', validators=[DataRequired()])
    Area = StringField(label = 'Area:', validators=[DataRequired()])
    Submit = SubmitField(label = 'Register New User')

class LoginForm(FlaskForm):
    Code = StringField(label = 'Student ID:', validators=[DataRequired()])
    Password = PasswordField(label = 'Password:', validators=[DataRequired()])
    Submit = SubmitField(label = 'Sign in')