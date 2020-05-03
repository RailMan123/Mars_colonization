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
        cap = session.query(User).filter(User.id == 1).first()
        for job in jobs:
            if job.id == id and job.user == current_user or job.id == id and job.user == cap:
                form.team_leader.data = job.team_leader
                form.job.data = job.job
                form.is_finished.data = job.is_finished
                form.work_size.data = job.work_size
                form.collaborators.data = job.collaborators
                break

        else:
            abort(404)
    if form.validate_on_submit():
        session = create_session()
        jobs = session.query(Jobs).all()
        cap = session.query(User).filter(User.id == 1).first()
        for job in jobs:
            if job.id == id and job.user == current_user or job.id == id and job.user == cap:
                job.team_leader = form.team_leader.data
                job.job = form.job.data
                job.is_finished = form.is_finished.data
                job.work_size = form.work_size.data
                job.collaborators = form.collaborators.data
                session.add(job)
                session.commit()
                return redirect('/')
        abort(404)
    return render_template('jobs.html', title='Редактирование работы', form=form)


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