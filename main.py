from data import db_session
from flask import Flask, render_template, url_for, redirect, request, abort
from data.users import User
from forms.user import RegisterForm, LoginForm, ChangeForm
from forms.first_tests import FirstTestForm
from flask_login import LoginManager
from flask_login import login_user, login_required, logout_user, current_user
from flask import make_response, jsonify

app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


def main():
    db_session.global_init("db/site_data.db")
    db_sess = db_session.create_session()
    db_sess.query(User).delete()
    random_user = User(name="Eshly", surname="Dark", status="student", email="alpusik2000004@gmail.com")
    random_user.set_password("Pokepark2")
    db_sess.add(random_user)
    db_sess.commit()


@app.route("/")
def index():
    return render_template("index.html")


@app.route('/user_edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_user(id):
    form = ChangeForm()
    if request.method == "GET":
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.id == id).first()
        if user:
            form.name.data = user.name
            form.surname.data = user.surname
        else:
            abort(404)
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.id == id).first()
        if user:
            user.name = form.name.data
            user.surname = form.surname.data
            db_sess.commit()
            return redirect('/')
        else:
            abort(404)
    return render_template('user_edit.html',
                           title='Изменение профиля',
                           form=form
                           )


@app.route('/first_test', methods=['GET', 'POST'])
@login_required
def first_test():
    form = FirstTestForm()
    if form.validate_on_submit():
        return redirect('/')
    return render_template('test_form.html', form=form)


@app.route("/profile/<int:user_id>")
def profile(user_id):
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.id == user_id).first()
    name = user.name
    surname = user.surname
    status = user.status
    email = user.email
    return render_template("profile.html", name=name, surname=surname, status=status, email=email)


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают",
                                   style=url_for('static', filename='css/form_style.css'))
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть",
                                   style=url_for('static', filename='css/form_style.css'))
        user = User(
            name=form.name.data,
            email=form.email.data,
            surname=form.name.data,
            status=form.status.data,
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


if __name__ == '__main__':
    main()
    app.run(port=5001, host='127.0.0.1')
