from data import db_session
from flask import Flask, render_template, url_for, redirect, request, abort, make_response, session
from data.users import User
from data.categories import Category
from data.tests_pages import FirstTestPage, SecondTestPage
from forms.user import RegisterForm, LoginForm, ChangeForm
from forms.tests_forms import FirstTestForm, SecondTestForm
from forms.list_of_tests import TestForm
from data.tests import Test, FirstTest, SecondTest
from flask_login import LoginManager
from flask_login import login_user, login_required, logout_user

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
    db_sess.query(Category).delete()
    db_sess.query(Test).delete()
    db_sess.query(FirstTest).delete()
    db_sess.query(SecondTest).delete()
    db_sess.query(FirstTestPage).delete()
    random_user = User(name="Eshly", surname="Dark", status="student", email="alpusik2000004@gmail.com")
    first_language = Category(name="English")
    second_language = Category(name="Japanese")
    random_user.set_password("Pokepark2")
    some_page = FirstTestPage(
        image_list='/static/img/first_test/1/test1.jpg, /static/img/first_test/1/test2.jpg, /static/img/first_test/1/test3.jpg',
        right_image_number=1, question="Какая фапута лучше?")
    second_page = FirstTestPage(
        image_list='/static/img/first_test/1/test4.jpg, /static/img/first_test/1/test5.jpg, /static/img/first_test/1/test6.jpg',
        right_image_number=2, question="Какая картинка лучше?")
    third_page = FirstTestPage(
        image_list='/static/img/first_test/1/test7.png, /static/img/first_test/1/test8.png, /static/img/first_test/1/test9.png',
        right_image_number=1, question="Какой каштан лучше?")
    first_test = FirstTest(title="something", language_id=1, creator=1, type='first_tests',
                           title_picture='/static/img/first_test/1/title.jpg')
    second_test = FirstTest(title="something2", language_id=2, creator=1, type='first_tests')
    second_page1 = SecondTestPage(words_list='no, yes, is', first_sentence='My name', second_sentence='Lucas',
                                  right_word_number=2)
    second_page2 = SecondTestPage(words_list='no, yes, is', first_sentence='My name', second_sentence='Lucas',
                                  right_word_number=2)
    third_test = SecondTest(title="something3", language_id=2, creator=1, type='second_tests')
    second_page3 = SecondTestPage(words_list='no, yes, is', first_sentence='My name', second_sentence='Lucas',
                                  right_word_number=2)
    first_test.pages.append(some_page)
    first_test.pages.append(second_page)
    first_test.pages.append(third_page)
    third_test.pages.append(second_page1)
    third_test.pages.append(second_page2)
    third_test.pages.append(second_page3)
    db_sess.add(random_user)
    db_sess.add(first_test)
    db_sess.add(first_language)
    db_sess.add(second_language)
    db_sess.add(third_test)
    db_sess.add(second_test)
    db_sess.commit()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/tests_list", methods=['GET', 'POST'])
def test_list():
    form = TestForm()
    db_sess = db_session.create_session()
    categories = db_sess.query(Category).all()
    used = ['all']
    for category in categories:
        if category.name not in used:
            used.append(category.name)
    form.languages.choices = used
    if request.method == "GET":
        tests = db_sess.query(Test).all()
        return render_template("tests_list.html", form=form, tests=tests)
    if form.validate_on_submit():
        now_language = form.languages.data
        if now_language == "all":
            tests = db_sess.query(Test).all()
        else:
            tests = db_sess.query(Test).filter(Test.language_id == used.index(now_language))
        return render_template("tests_list.html", form=form, tests=tests)


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


@app.route('/first_tests/<int:id>/<int:page_number>', methods=['GET', 'POST'])
def first_test(id, page_number):
    db_sess = db_session.create_session()
    test = db_sess.query(FirstTest).filter(FirstTest.id == id).first()
    form = FirstTestForm()
    current_page = test.pages[page_number - 1]
    question = current_page.question
    images_list = []
    for image in current_page.image_list.split(', '):
        images_list.append(image)
    form.images.choices = images_list
    if page_number == 1:
        session['total_score'] = 0
    if form.validate_on_submit():
        if page_number == len(test.pages):
            score = session.get('total_score', 0)
            if current_page.image_list.split(', ').index(form.images.data) == current_page.right_image_number:
                session['total_score'] = score + 10
            return redirect('/test_succeed/' + str(id))
        else:
            if current_page.image_list.split(', ').index(form.images.data) == current_page.right_image_number:
                score = session.get('total_score', 0)
                session['total_score'] = score + 10
            return redirect('/first_tests/' + str(id) + '/' + str(page_number + 1))
    return render_template('first_test.html', form=form, question=question)


@app.route('/second_tests/<int:id>/<int:page_number>', methods=['GET', 'POST'])
def second_test(id, page_number):
    db_sess = db_session.create_session()
    test = db_sess.query(SecondTest).filter(SecondTest.id == id).first()
    form = SecondTestForm()
    current_page = test.pages[page_number - 1]
    first_sentence, second_sentence = current_page.first_sentence, current_page.second_sentence
    words_list = current_page.words_list.split(', ')
    form.words.choices = words_list
    if page_number == 1:
        session['total_score'] = 0
    if form.validate_on_submit():
        if page_number == len(test.pages):
            score = session.get('total_score', 0)
            if current_page.words_list.split(', ').index(form.words.data) == current_page.right_word_number:
                session['total_score'] = score + 10
            return redirect('/test_succeed/' + str(id))
        else:
            if current_page.words_list.split(', ').index(form.words.data) == current_page.right_word_number:
                score = session.get('total_score', 0)
                session['total_score'] = score + 10
            return redirect('/second_tests/' + str(id) + '/' + str(page_number + 1))
    return render_template('second_test.html', form=form, first_sentence=first_sentence,
                           second_sentence=second_sentence)


@app.route('/test_title/<int:id>')
def test_title(id):
    db_sess = db_session.create_session()
    test = db_sess.query(Test).filter(Test.id == id).first()
    return render_template('test_title.html', test=test)


@app.route('/test_succeed/<int:id>')
def test_succeed(id):
    score = session.get('total_score', 0)
    session['total_score'] = 0
    db_sess = db_session.create_session()
    test = db_sess.query(FirstTest).filter(FirstTest.id == id).first()
    return render_template('test_succeed.html', test=test, score=score)


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
