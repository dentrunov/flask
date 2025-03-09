from app import app
from flask_login import current_user, login_user
import sqlalchemy as sa
from flask import render_template, flash, redirect, url_for, request
from flask_login import logout_user, login_required

from app import db
from app.models import User, Student, Classes
from app.forms import RegistrationForm, LoginForm, AddStudentsForm, EditInformationForm


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Home')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if request.method == 'POST':
        user = db.session.scalar(
            sa.select(User).where(User.username == form.username.data))
        if user is None or not user.check_password(form.password.data):
          flash('Неправильный логин или пароль')
          return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data, status=4)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/user')
def user():
    user = db.first_or_404(sa.select(User).where(User.username == current_user.username))
    return render_template('second.html', title='Home', user=user)

@app.route("/add_students", methods=['GET', 'POST'])
def add_students():
    form = AddStudentsForm()
    if form.validate_on_submit():
        name = form.name.data
        surname = form.surname.data
        paral = form.par.data
        class_ = form.class_.data
        class_id = db.session.scalar(sa.select(Classes).filter(Classes.class_name==str(paral) + class_))
        print(class_id)
        student = Student(name=name, surname=surname, paral=paral, class_id=class_id.id)
        db.session.add(student)
        db.session.commit()
        return redirect(url_for('user'))
    return render_template('add_students.html', title='Добавить студентов', form=form)

@app.route('/class/<int:num>',methods=['GET'])
def classes(num):   
    students = db.session.scalars(sa.select(Student).filter(Student.paral==num))
    classes = db.session.scalars(sa.select(Classes).filter(Classes.class_parral==num))
    sts = {}
    for student in students:
        sts.setdefault(student.class_id, []).append(student)

    print(sts)
    return render_template('classes.html', title=str(num) + 'классы', students=sts, classes=classes)

@app.route('/edit data')
def edit_data():
    form = EditInformationForm()
    u_id = current_user.id
    if form.validate_on_submit():
        name = form.name.data
        surname = form.surname.data
        new_data = {}
        if name:
            new_data.update({"name": name})
        if surname:
            new_data.update({"surname": surname})
        usr = User.query.filter_by(user_id = u_id).update(new_data)
        db.session.commit()
        return redirect(url_for('user'))
    return render_template('edit_data.html', title='Редактировать информацию пользователей', form=form)

@app.route("/dashboard")
@login_required
def dashboard():
    return render_template('dashboard.html', title='Dashboard')