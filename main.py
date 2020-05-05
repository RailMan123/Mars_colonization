from flask import Flask, render_template, request
from flask_login import login_user, LoginManager, login_manager, login_required, logout_user,\
    current_user
from flask_restful import abort
from flask_wtf import FlaskForm
from werkzeug.utils import redirect
from wtforms import PasswordField, StringField, TextAreaField, SubmitField, BooleanField, IntegerField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired

from data.db_session import create_session, global_init
from data.departments import Department
from data.jobs import Jobs
from data.users import User, News


app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)
@login_manager.user_loader
def load_user(user_id):
    session = create_session()
    return session.query(User).get(user_id)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


class NewsForm(FlaskForm):
    title = StringField('Заголовок', validators=[DataRequired()])
    content = TextAreaField("Содержание")
    is_private = BooleanField("Личное")
    submit = SubmitField('Применить')


class RegisterForm(FlaskForm):
    email = EmailField('Login / email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    password_again = PasswordField('Repeat password', validators=[DataRequired()])
    surname = StringField('Surname', validators=[DataRequired()])
    name = StringField('Name', validators=[DataRequired()])
    age = IntegerField('Age', validators=[DataRequired()])
    position = StringField('Position', validators=[DataRequired()])
    speciality = StringField('Speciality', validators=[DataRequired()])
    address = StringField('Address', validators=[DataRequired()])
    submit = SubmitField('Submit')

@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        session = create_session()
        if session.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            email=form.email.data,
            surname=form.surname.data,
            name=form.name.data,
            age=form.age.data,
            position=form.position.data,
            speciality=form.speciality.data,
            address=form.address.data,

        )
        user.set_password(form.password.data)
        session.add(user)
        session.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)

class LoginForm(FlaskForm):
    email = EmailField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')

class JobsForm(FlaskForm):
    team_leader = IntegerField('Team Leader', validators=[DataRequired()])
    job = StringField("Job")
    work_size = IntegerField('Work size', validators=[DataRequired()])
    collaborators = StringField("Collaborators")
    is_finished = BooleanField("Is finished?")
    submit = SubmitField('DO IT!')

class DepartmentForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    chef = IntegerField('Team Leader', validators=[DataRequired()])
    members = StringField("Members", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired()])
    submit = SubmitField('DO IT!')

@app.route('/departments',  methods=['GET', 'POST'])
@login_required
def departments_show():
    session = create_session()
    jobs = session.query(Department).all()
    return render_template("departments_table.html", jobs=jobs)

@app.route('/add_department',  methods=['GET', 'POST'])
@login_required
def add_department():
    form = DepartmentForm()
    if form.validate_on_submit():
        session = create_session()
        Dep = Department()
        Dep.chef = form.chef.data
        Dep.title = form.title.data
        Dep.members = form.members.data
        Dep.email = form.email.data
        session.add(Dep)
        session.commit()
        return redirect('/departments')
    return render_template('department.html', title='Добавление департамента',
                           form=form)

@app.route('/department/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_department(id):
    form = DepartmentForm()
    if request.method == "GET":
        session = create_session()
        deps = session.query(Department).all()
        a = False
        for i in range(len(deps)):
            if deps[i].id == id and deps[i].user == current_user or deps[i].id == id and current_user.id == 1:
                form.title.data = deps[i].title
                form.chef.data = deps[i].chef
                form.members.data = deps[i].members
                form.email.data = deps[i].email
                a = True
                break
        if not a:
            abort(404)
    if form.validate_on_submit():
        session = create_session()
        deps = session.query(Department).all()
        for i in range(len(deps)):
            if deps[i].id == id and deps[i].user == current_user or deps[i].id == id and current_user.id == 1:
                deps[i].title = form.title.data
                deps[i].chef = form.chef.data
                deps[i].members = form.members.data
                deps[i].email = form.email.data
                session.add(deps[i])
                session.commit()
                return redirect('/departments')
            if i == len(deps) - 1:
                abort(404)
    return render_template('department.html', title='Редактирование департамента', form=form)

@app.route('/department_delete/<int:id>', methods=['GET', 'POST'])
@login_required
def department_delete(id):
    session = create_session()
    deps = session.query(Department).all()
    for i in range(len(deps)):
        if deps[i].id == id and deps[i].user == current_user or deps[i].id == id and current_user.id == 1:
            session.delete(deps[i])
            session.commit()
            return redirect('/departments')
        if i == len(deps) - 1:
            abort(404)

@app.route('/add_job',  methods=['GET', 'POST'])
@login_required
def add_job():
    form = JobsForm()
    if form.validate_on_submit():
        session = create_session()
        job = Jobs()
        job.team_leader = form.team_leader.data
        job.job = form.job.data
        job.is_finished = form.is_finished.data
        job.work_size = form.work_size.data
        job.collaborators = form.collaborators.data
        session.add(job)
        session.commit()
        return redirect('/')
    return render_template('jobs.html', title='Добавление работы',
                           form=form)

@app.route('/job/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_job(id):
    form = JobsForm()
    if request.method == "GET":
        session = create_session()
        jobs = session.query(Jobs).all()
        a = False
        for i in range(len(jobs)):
            if jobs[i].id == id and jobs[i].user == current_user or jobs[i].id == id and current_user.id == 1:
                form.team_leader.data = jobs[i].team_leader
                form.job.data = jobs[i].job
                form.is_finished.data = jobs[i].is_finished
                form.work_size.data = jobs[i].work_size
                form.collaborators.data = jobs[i].collaborators
                a = True
                break
        if not a:
            abort(404)
    if form.validate_on_submit():
        session = create_session()
        jobs = session.query(Jobs).all()
        for i in range(len(jobs)):
            if jobs[i].id == id and jobs[i].user == current_user or jobs[i].id == id and current_user.id == 1:
                jobs[i].team_leader = form.team_leader.data
                jobs[i].job = form.job.data
                jobs[i].is_finished = form.is_finished.data
                jobs[i].work_size = form.work_size.data
                jobs[i].collaborators = form.collaborators.data
                session.add(jobs[i])
                session.commit()
                return redirect('/')
            if i == len(jobs) - 1:
                abort(404)
    return render_template('jobs.html', title='Редактирование работы', form=form)

@app.route('/job_delete/<int:id>', methods=['GET', 'POST'])
@login_required
def job_delete(id):
    session = create_session()
    jobs = session.query(Jobs).all()
    for i in range(len(jobs)):
        if jobs[i].id == id and jobs[i].user == current_user or jobs[i].id == id and current_user.id == 1:
            session.delete(jobs[i])
            session.commit()
            return redirect('/')
        if i == len(jobs) - 1:
            abort(404)

@app.route('/news',  methods=['GET', 'POST'])
@login_required
def add_news():
    form = NewsForm()
    if form.validate_on_submit():
        session = create_session()
        news = News()
        news.title = form.title.data
        news.content = form.content.data
        news.is_private = form.is_private.data
        current_user.news.append(news)
        session.merge(current_user)
        session.commit()
        return redirect('/')
    return render_template('news.html', title='Добавление новости',
                           form=form)

@app.route('/news/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_news(id):
    form = NewsForm()
    if request.method == "GET":
        session = create_session()
        news = session.query(News).filter(News.id == id,
                                          News.user == current_user).first()
        if news:
            form.title.data = news.title
            form.content.data = news.content
            form.is_private.data = news.is_private
        else:
            abort(404)
    if form.validate_on_submit():
        session = create_session()
        news = session.query(News).filter(News.id == id,
                                          News.user == current_user).first()
        if news:
            news.title = form.title.data
            news.content = form.content.data
            news.is_private = form.is_private.data
            session.commit()
            return redirect('/')
        else:
            abort(404)
    return render_template('news.html', title='Редактирование новости', form=form)

@app.route('/news_delete/<int:id>', methods=['GET', 'POST'])
@login_required
def news_delete(id):
    session = create_session()
    news = session.query(News).filter(News.id == id,
                                      News.user == current_user).first()
    if news:
        session.delete(news)
        session.commit()
    else:
        abort(404)
    return redirect('/')



@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        session = create_session()
        user = session.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)



@app.route('/')
def index():
    session = create_session()
    jobs = session.query(Jobs).all()
    return render_template("job_table.html", jobs=jobs)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


def main():
    global_init("db/blogs.sqlite")
    app.run()


if __name__ == '__main__':
    main()