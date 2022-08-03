from flask_login.utils import login_required
from flask_wtf import form
from webapp import app
from flask import render_template, redirect, url_for, flash, get_flashed_messages, request, send_file
from webapp.models import FileContents, Item, Student, Videos, load_user, student_identifier
from webapp.forms import RegisterForm, LoginForm
from webapp import db
from flask_login import current_user, login_user, logout_user
from io import BytesIO

@app.route('/')
@app.route('/home')
def home_page():
    return render_template('home.html')

@app.route('/about')
def about_page():
    return '<h1>About page<h1>'

@app.route('/profile/<username>')
def profile_page(username):
    return f'<h1>Profile of {username}<h1>'

@app.route('/courses')
def courses_page():

    courses_list = Item.query.all()

    return render_template('courses.html', semester='21Z', items=courses_list)


@app.route('/admin', methods=['GET', 'POST'])
def admin_page():
    if(current_user.is_authenticated):
        if(current_user.Code == 'ADMIN'):
            form = RegisterForm()
            if form.validate_on_submit():
                student_to_create = Student(Name=form.Name.data, Surname=form.Surname.data, Code=form.Code.data,
                                            password_hash=form.Password1.data,Semester=form.Semester.data ,Area=form.Area.data, )
                db.session.add(student_to_create)
                db.session.commit()
                return redirect(url_for('courses_page'))
            if form.errors != {}:
                for err_msg in form.errors.values():
                    flash(f'There was an error with creating a user: {err_msg}', category='danger')
            return render_template('register.html', form=form)
        else:
            return 'You are not the administrator'
    else:
        return 'Login into administrator account to access admin panel'


@app.route('/login', methods=['GET', 'POST'])
def login_page():
    form=LoginForm()
    if form.validate_on_submit():
        attempted_student = Student.query.filter_by(Code=form.Code.data).first()
        if attempted_student and attempted_student.check_password_correction(attempted_password=form.Password.data):
            login_user(attempted_student)
            flash(f'User logged in: {attempted_student.Name} {attempted_student.Surname}', category='success')
            return redirect(url_for('courses_page'))
        else:
            flash('Wrong Code or Password', category='danger')    
    return render_template('login.html', form=form)

@app.route('/logout')
def logout_page():
    logout_user()
    flash('You have been logged out', category='info')
    return redirect(url_for('home_page'))

@app.route('/user/<Code>')
@login_required
def user(Code):
    user = Student.query.filter_by(Code=Code).first
    courses_list = Student.query.filter_by(Code=Code).first().Courses
    return render_template('user.html', user=user, items=courses_list)

@app.route('/upload')
def upload_page():

    return render_template('upload.html')

@app.route('/uploading', methods=['POST'])
def uploading_page():
    file = request.files['inputFile']

    newFile = Videos(code="ENUME", name=file.filename, data=file.read())
    db.session.add(newFile)
    db.session.commit()

    return 'Saved ' + file.filename + ' to database'

@app.route('/cours/<Code>')
@login_required
def cours_page(Code):
    cours = Item.query.filter_by(Code=Code).first
    video_list = Videos.query.filter_by(code=Code)
    return render_template('cours.html', cours=cours, items=video_list)


@app.route('/download/<Id>')
@login_required
def download(Id):

    file_data = Videos.query.filter_by(id=Id).first()

    return send_file(BytesIO(file_data.data), attachment_filename=file_data.name, as_attachment=False)