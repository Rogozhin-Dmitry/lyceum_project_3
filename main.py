import datetime
import os
import shutil

from flask import Flask, render_template, redirect, request, session
from flask_login import LoginManager
from flask_login import login_user, login_required, logout_user, current_user

from data import db_session
from data.categories import Category
from data.tests import Test, FirstTest, SecondTest
from data.tests_pages import FirstTestPage, SecondTestPage
from data.users import User
from extend_main_index_page import start_app
from forms.create_tests_form import PictureSlot, WordSlot, SecondTestCreateForm, TestCreateForm, \
    NewTestForm
from forms.list_of_tests import TestForm
from forms.tests_forms import FirstTestForm, SecondTestForm
from forms.user import RegisterForm, LoginForm, ChangeForm, SmallLoginForm

app = Flask(__name__)
app.config['PERMANENT_SESSION_LIFETIME'] = datetime.timedelta(
    days=365
)
login_manager = LoginManager()
login_manager.init_app(app)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
TEST_TYPES = ['first_tests', 'second_tests']
start_app(app)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


def main():
    db_session.global_init("db/site_data.db")
    db_sess = db_session.create_session()
    # db_sess.query(User).delete()
    # db_sess.query(Category).delete()
    # db_sess.query(Test).delete()
    # db_sess.query(FirstTest).delete()
    # db_sess.query(SecondTest).delete()
    # db_sess.query(FirstTestPage).delete()
    # random_user = User(name="Eshly", surname="Dark", status="student", email="alpusik2000004@gmail.com")
    # first_language = Category(name="English")
    # second_language = Category(name="Japanese")
    # random_user.set_password("Pokepark2")
    # some_page = FirstTestPage()
    # some_page.image_list = \
    #     '/static/img/first_test/1/test1.jpg, /static/img/first_test/1/test2.jpg, /static/img/first_test/1/test3.jpg'
    # some_page.right_image_number = 1
    # some_page.question = "Какая фапута лучше?"
    # second_page = FirstTestPage()
    # some_page.image_list = \
    #     '/static/img/first_test/1/test4.jpg, /static/img/first_test/1/test5.jpg, /static/img/first_test/1/test6.jpg'
    # some_page.right_image_number = 2
    # some_page.question = "Какая картинка лучше?"
    # third_page = FirstTestPage()
    # some_page.image_list = \
    #     '/static/img/first_test/1/test7.png, /static/img/first_test/1/test8.png, /static/img/first_test/1/test9.png'
    # some_page.right_image_number = 1
    # some_page.question = "Какой каштан лучше?"
    # first_test_1 = FirstTest()
    # first_test_1.title = "something"
    # first_test_1.language_id = 1
    # first_test_1.creator = 1
    # first_test_1.type = 'first_tests'
    # first_test_1.title_picture = '/static/img/first_test/1/title.jpg'
    # second_test_1 = FirstTest()
    # second_test_1.title = "something2"
    # second_test_1.language_id = 2
    # second_test_1.creator = 1
    # second_test_1.type = 'first_tests'
    # second_page1 = SecondTestPage()
    # second_page1.words_list = 'no, yes, is'
    # second_page1.first_sentence = 'My name'
    # second_page1.second_sentence = 'Lucas'
    # second_page1.right_word_number = 2
    # second_page2 = SecondTestPage()
    # second_page2.words_list = 'no, yes, is'
    # second_page2.first_sentence = 'My name'
    # second_page2.second_sentence = 'Lucas'
    # second_page2.right_word_number = 2
    # third_test = SecondTest()
    # third_test.title = "something3"
    # third_test.language_id = 2
    # third_test.creator = 1
    # third_test.type = 'second_tests'
    # second_page3 = SecondTestPage
    # second_page3.words_list = 'no, yes, is'
    # second_page3.first_sentence = 'My name'
    # second_page3.second_sentence = 'Lucas'
    # second_page3.right_word_number = 2
    # first_test_1.pages.append(some_page)
    # first_test_1.pages.append(second_page)
    # first_test_1.pages.append(third_page)
    # third_test.pages.append(second_page1)
    # third_test.pages.append(second_page2)
    # third_test.pages.append(second_page3)
    # db_sess.add(random_user)
    # db_sess.add(first_test_1)
    # db_sess.add(first_language)
    # db_sess.add(second_language)
    # db_sess.add(third_test)
    # db_sess.add(second_test_1)
    # db_sess.commit()
    app.run(port=5001, host='127.0.0.1')


class Tests:
    def __init__(self, name, language, description):
        self.name = name
        self.language = language
        self.description = description
        db_sess = db_session.create_session()
        self.author = db_sess.query(User).filter(User.id == 1).first()


@app.route('/index/', methods=['GET', 'POST'])
@app.route('/index/<int:page_id>', methods=['GET', 'POST'])
@app.route('/', methods=['GET', 'POST'])
@app.route('/<int:page_id>', methods=['GET', 'POST'])
def index(page_id=1):
    session['current_second_test_length'] = 2
    session['current_first_test_length'] = 2
    session['current_images_stack'] = []
    if not current_user.is_authenticated:
        return render_template('index.html')
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.id == current_user.get_id()).first()
    if request.method == 'POST':
        block_filter = {'По популярности': 0, 'По названию': 1, 'По дате (сначала старые)': 2,
                        'По дате (сначала новые)': 3}
        user.current_filter = block_filter[str(request.form).split('block_filter')[-1].split("'")[2]]
        db_sess.add(user)
        db_sess.commit()
    tests = [Tests('Имя теста 2', 'Немецкий', 'Не особо большое описание этого теста')]
    import random
    for i in range(32):
        tests.append(Tests(f'Имя теста {random.randint(0, 1000)}', 'Немецкий', 'Не особо большое описание этого теста'))
    if user.current_filter == 1:
        tests = sorted(tests, key=lambda x: int(x.name.split()[-1]))
    if len(tests) > 12 * page_id:
        next_page_id = page_id + 1
    else:
        next_page_id = 0
    if page_id > 1:
        previous_page_id = page_id - 1
    else:
        previous_page_id = 0
    return render_template('index_for_log_users.html', tests=tests[12 * (page_id - 1):12 * page_id],
                           current_filter=user.current_filter, page=[previous_page_id, next_page_id])


@app.route('/my_tests/', methods=['GET', 'POST'])
@app.route('/my_tests/<int:page_id>', methods=['GET', 'POST'])
def my_tests(page_id=1):
    if not current_user.is_authenticated:
        return redirect('/login')
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.id == current_user.get_id()).first()
    if request.method == 'POST':
        block_filter = {'По популярности': 0, 'По названию': 1, 'По дате (сначала старые)': 2,
                        'По дате (сначала новые)': 3}
        user.current_filter = block_filter[str(request.form).split('block_filter')[-1].split("'")[2]]
        db_sess.add(user)
        db_sess.commit()
    tests = [Tests('Имя теста 2', 'Немецкий', 'Не особо большое описание этого теста')]
    import random
    for i in range(132):
        tests.append(Tests(f'Имя теста {random.randint(0, 1000)}', 'Немецкий', 'Не особо большое описание этого теста'))
    if user.current_filter == 1:
        tests = sorted(tests, key=lambda x: int(x.name.split()[-1]))
    if len(tests) > 12 * page_id:
        next_page_id = page_id + 1
    else:
        next_page_id = 0
    if page_id > 1:
        previous_page_id = page_id - 1
    else:
        previous_page_id = 0
    return render_template('my_tests.html', tests=tests[12 * (page_id - 1):12 * page_id],
                           current_filter=user.current_filter, page=[previous_page_id, next_page_id])


@app.route('/test_page')
def test():
    return render_template('test_page.html')


@app.route('/email', methods=['POST'])
def email():
    if request.method == 'POST':
        print(request.form['email'])
    return redirect('/')


@app.route('/test_site')
def test_site():
    test_data = Tests('Имя теста 2', 'Немецкий', 'Не особо большое описание этого теста')
    return render_template('test_site.html', test=test_data)


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


@app.route('/first_tests/<int:id>/<int:page_number>', methods=['GET', 'POST'])
def first_test(user_id, page_number):
    db_sess = db_session.create_session()
    test = db_sess.query(FirstTest).filter(FirstTest.id == user_id).first()
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
            return redirect('/test_succeed/' + str(user_id))
        else:
            if current_page.image_list.split(', ').index(form.images.data) == current_page.right_image_number:
                score = session.get('total_score', 0)
                session['total_score'] = score + 10
            return redirect('/first_tests/' + str(user_id) + '/' + str(page_number + 1))
    return render_template('first_test.html', form=form, question=question)


@app.route('/second_tests/<int:id>/<int:page_number>', methods=['GET', 'POST'])
def second_test(user_id, page_number):
    db_sess = db_session.create_session()
    test = db_sess.query(SecondTest).filter(SecondTest.id == user_id).first()
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
            return redirect('/test_succeed/' + str(user_id))
        else:
            if current_page.words_list.split(', ').index(form.words.data) == current_page.right_word_number:
                score = session.get('total_score', 0)
                session['total_score'] = score + 10
            return redirect('/second_tests/' + str(user_id) + '/' + str(page_number + 1))
    return render_template('second_test.html', form=form, first_sentence=first_sentence,
                           second_sentence=second_sentence)


@app.route('/test_title/<int:id>')
def test_title(user_id):
    db_sess = db_session.create_session()
    test = db_sess.query(Test).filter(Test.id == user_id).first()
    return render_template('test_title.html', test=test)


@app.route('/test_succeed/<int:id>')
def test_succeed(user_id):
    score = session.get('total_score', 0)
    session['total_score'] = 0
    db_sess = db_session.create_session()
    test = db_sess.query(FirstTest).filter(FirstTest.id == user_id).first()
    return render_template('test_succeed.html', test=test, score=score)


@app.route('/first_test_create/<int:test_id>/<int:page_id>', methods=['GET', 'POST'])
@app.route('/first_test_create/<int:test_id>', methods=['GET', 'POST'])
def first_test_create(test_id, page_id=None):
    if not os.path.exists('static/img/users/' + str(current_user.id) + '/first_test_create_stack'):
        os.mkdir('static/img/users/' + str(current_user.id) + '/first_test_create_stack')
    form = NewTestForm()
    current_length = session.get('current_first_test_length', 2)
    current_images = session.get('current_images_stack', [])
    new_choices = [str(i + 1) for i in range(current_length)]
    form.right_image_choosing.choices = new_choices
    if request.method == "GET":
        if page_id is not None:
            db_sess = db_session.create_session()
            current_page = db_sess.query(FirstTestPage).filter(FirstTestPage.id == page_id).first()
            session['current_first_test_length'] = len(current_page.image_list.split(', '))
            while len(form.images.entries) != len(current_page.image_list.split(', ')):
                form.images.append_entry(PictureSlot())
            session['current_images_stack'] = current_page.image_list.split(', ')
            current_images = session.get('current_images_stack', [])
            form.question.data = current_page.question
            new_choices = [str(i + 1) for i in range(len(current_page.image_list.split(', ')))]
            form.right_image_choosing.choices = new_choices
            form.right_image_choosing.data = str(current_page.right_image_number)
    if request.method == "POST":
        session['current_som_test_length'] = session.get('current_som_test_length', 3) + 1
        if 'over' in request.form:
            images_list = session.get('current_images_stack', [])
            if '' in images_list or len(images_list) == 0:
                return render_template('test.html', form=form, images=images_list, message='не все картинки заполнены')
            if form.right_image_choosing.data is None:
                return render_template('test.html', form=form, images=images_list, message='Не выбрана верная картинка')
            db_sess = db_session.create_session()
            current_test = db_sess.query(FirstTest).filter(FirstTest.id == test_id).first()
            session['current_images_stack'] = []
            for i in range(len(images_list)):
                if images_list[i][1:] != 'static/img/first_test/' + str(test_id) + '/' + images_list[i][
                                                                                         images_list[i].rfind(
                                                                                             '/') + 1:]:
                    shutil.copy(images_list[i][1:],
                                'static/img/first_test/' + str(test_id) + '/' + images_list[i][
                                                                                images_list[i].rfind('/') + 1:])
                images_list[i] = '/static/img/first_test/' + str(test_id) + '/' + images_list[i][
                                                                                  images_list[i].rfind('/') + 1:]
            pages_now_images = os.listdir('static/img/first_test/' + str(test_id))
            for image in pages_now_images:
                if '/static/img/first_test/' + str(test_id) + '/' + image not in images_list:
                    os.remove('static/img/first_test/' + str(test_id) + '/' + image)
            images_list = ', '.join(images_list)
            if page_id is None:
                new_page = FirstTestPage()
                new_page.question = form.question.data
                new_page.right_image_number = int(form.right_image_choosing.data)
                new_page.image_list = images_list
                current_test.pages.append(new_page)
                db_sess.add(new_page)
            else:
                new_page = db_sess.query(FirstTestPage).filter(FirstTestPage.id == page_id).first()
                new_page.question = form.question.data
                new_page.right_image_number = int(form.right_image_choosing.data)
                new_page.image_list = images_list
            db_sess.commit()
            shutil.rmtree('static/img/users/' + str(current_user.id) + '/first_test_create_stack')
            return redirect('/test_page_creation/' + str(test_id))
        elif 'right' in request.form:
            print('yeah')
            current_length = session.get('current_first_test_length', 2)
            if current_length < 5:
                session['current_first_test_length'] = current_length + 1
                current_length = session.get('current_first_test_length', 2)
                form.images.append_entry(PictureSlot())
            form.right_image_choosing.choices = [str(i + 1) for i in range(current_length)]
        elif 'left' in request.form:
            current_length = session.get('current_first_test_length', 2)
            if current_length > 2:
                session['current_first_test_length'] = current_length - 1
                current_length = session.get('current_first_test_length', 2)
                del form.images.entries[-1]
                del session['current_images_stack'][-1]
            form.right_image_choosing.choices = [str(i + 1) for i in range(current_length)]
        else:
            images_list = []
            for image in form.images.entries:
                if image.slot.data.filename != '':
                    if image.slot.data.filename[image.slot.data.filename.index('.') + 1:] not in ["jpg", "bmp", "png",
                                                                                                  "jpeg",
                                                                                                  "gif",
                                                                                                  "cdr", "svg"]:
                        return render_template('test.html', form=form, message='Непподдерживаемый формат файла')
                    image.slot.data.save('static/img/users/' + str(current_user.id) + '/first_test_create_stack/' +
                                         image.slot.data.filename)
                    images_list.append('/static/img/users/' + str(
                        current_user.id) + '/first_test_create_stack/' + image.slot.data.filename)
                else:
                    images_list.append('')
            for i in range(len(images_list)):
                current_images = session.get('current_images_stack', [])
                if i == len(current_images):
                    session['current_images_stack'].append('')
                if images_list[i] != '':
                    session['current_images_stack'][i] = images_list[i]
            current_images = session.get('current_images_stack', [])
        return render_template('test.html', form=form, images=current_images)
    return render_template('test.html', form=form, images=current_images)


@app.route('/second_test_create/<int:test_id>/<int:page_id>', methods=['GET', 'POST'])
@app.route('/second_test_create/<int:test_id>', methods=['GET', 'POST'])
def second_test_create(test_id, page_id=None):
    form = SecondTestCreateForm()
    if request.method == "GET":
        if page_id is not None:
            db_sess = db_session.create_session()
            current_page = db_sess.query(SecondTestPage).filter(SecondTestPage.id == page_id).first()
            session['current_second_test_length'] = len(current_page.words_list.split(', '))
            while len(form.words.entries) != len(current_page.words_list.split(', ')):
                form.words.append_entry(WordSlot())
            count = 0
            for word in form.words.entries:
                word.slot.data = current_page.words_list.split(', ')[count]
                count = count + 1
            form.first_sentence.data = current_page.first_sentence
            form.second_sentence.data = current_page.second_sentence
            new_choices = [str(i + 1) for i in range(len(current_page.words_list.split(', ')))]
            form.right_word_choosing.choices = new_choices
            form.right_word_choosing.data = str(current_page.right_word_number)
        else:
            current_length = session.get('current_second_test_length', 2)
            new_choices = [str(i + 1) for i in range(current_length)]
            form.right_word_choosing.choices = new_choices
    if request.method == "POST":
        if 'right' in request.form:
            current_length = session.get('current_second_test_length', 2)
            if current_length < 5:
                session['current_second_test_length'] = current_length + 1
                current_length = session.get('current_second_test_length', 2)
                print(current_length, 'from_right')
                form.words.append_entry(WordSlot())
            form.right_word_choosing.choices = [str(i + 1) for i in range(current_length)]
        if 'left' in request.form:
            current_length = session.get('current_second_test_length', 2)
            if current_length > 2:
                session['current_second_test_length'] = current_length - 1
                current_length = session.get('current_second_test_length', 2)
                del form.words.entries[-1]
            form.right_word_choosing.choices = [str(i + 1) for i in range(current_length)]
        elif 'submit' in request.form:
            current_length = session.get('current_second_test_length', 2)
            new_choices = [str(i + 1) for i in range(current_length)]
            form.right_word_choosing.choices = new_choices
            if form.right_word_choosing.data is None:
                return render_template('second_test_create.html', form=form, message='Не выбрано верное слово')
            db_sess = db_session.create_session()
            current_test = db_sess.query(SecondTest).filter(SecondTest.id == test_id).first()
            words_list = []
            for word in form.words.entries:
                words_list.append(word.slot.data)
            words_list = ', '.join(words_list)
            if page_id is None:
                new_page = SecondTestPage()
                new_page.first_sentence = form.first_sentence.data
                new_page.second_sentence = form.second_sentence.data
                new_page.words_list = words_list
                new_page.right_word_number = int(form.right_word_choosing.data)
                current_test.pages.append(new_page)
                db_sess.add(new_page)
            else:
                new_page = db_sess.query(SecondTestPage).filter(SecondTestPage.id == page_id).first()
                new_page.first_sentence = form.first_sentence.data
                new_page.second_sentence = form.second_sentence.data
                new_page.words_list = words_list
                new_page.right_word_number = int(form.right_word_choosing.data)
            db_sess.commit()
            return redirect('/test_page_creation/' + str(test_id))
    return render_template('second_test_create.html', form=form)


@app.route('/create_test', methods=['GET', 'POST'])
def test_create():
    form = TestCreateForm()
    db_sess = db_session.create_session()
    categories = db_sess.query(Category).all()
    used = []
    for category in categories:
        if category.name not in used:
            used.append(category.name)
    form.language.choices = used
    form.type.choices = TEST_TYPES
    if form.validate_on_submit():
        language_id = db_sess.query(Category).filter(Category.name == form.language.data).first().id
        if form.type.data == 'first_tests':
            new_test = FirstTest()
            new_test.title = form.title.data
            new_test.language_id = language_id
            new_test.creator = current_user.id
            new_test.type = 'first_tests'
            db_sess.add(new_test)
        elif form.type.data == 'second_tests':
            new_test = SecondTest()
            new_test.title = form.title.data
            new_test.language_id = language_id
            new_test.creator = current_user.id
            new_test.type = 'second_tests'
            db_sess.add(new_test)
        test_id = str(db_sess.query(Test).filter((Test.title == form.title.data),
                                                 (Test.user == current_user)).first().id)
        test_type = str(db_sess.query(Test).filter((Test.title == form.title.data),
                                                   (Test.user == current_user)).first().type)
        test = db_sess.query(Test).filter((Test.title == form.title.data),
                                          (Test.user == current_user)).first()
        if test_type == "first_tests":
            if not os.path.exists('static/img/first_test/' + str(test_id)):
                os.mkdir('static/img/first_test/' + str(test_id))
                os.mkdir('static/img/first_test/' + str(test_id) + '/title')
        elif test_type == "second_tests":
            if not os.path.exists('static/img/second_test/' + str(test_id)):
                os.mkdir('static/img/second_test/' + str(test_id))
                os.mkdir('static/img/second_test/' + str(test_id) + '/title')
        if form.title_picture.data.filename != '':
            print('yeah')
            if form.title_picture.data.filename[form.title_picture.data.filename.index('.') + 1:] not in ["jpg", "bmp",
                                                                                                          "png",
                                                                                                          "jpeg",
                                                                                                          "gif",
                                                                                                          "cdr", "svg"]:
                return render_template('test_create.html', form=form)
            if form.type.data == 'first_tests':
                form.title_picture.data.save(
                    'static/img/first_test/' + str(test_id) + '/title/' + form.title_picture.data.filename)
                test.title_picture = '/' + 'static/img/first_test/' + str(
                    test_id) + '/title/' + form.title_picture.data.filename
            elif form.type.data == 'second_tests':
                form.title_picture.data.save(
                    'static/img/second_test/' + str(test_id) + '/title/' + form.title_picture.data.filename)
                test.title_picture = '/' + 'static/img/second_test/' + str(
                    test_id) + '/title/' + form.title_picture.data.filename
        db_sess.commit()
        return redirect('/test_page_creation/' + test_id)
    return render_template('test_create.html', form=form)


@app.route('/created_test_page', methods=['GET', 'POST'])
def created_test_page():
    if current_user.is_authenticated:
        db_sess = db_session.create_session()
        tests = db_sess.query(Test).filter(Test.creator == current_user.get_id())
        return render_template('created_test_page.html', tests=tests)
    else:
        return redirect("/login")


@app.route('/delete_page/<int:test_id>/<int:page_id>', methods=['GET', 'POST'])
def delete_page(test_id, page_id):
    db_sess = db_session.create_session()
    current_test = db_sess.query(Test).filter(Test.id == test_id).first()
    if current_test.type == 'second_tests':
        current_page = db_sess.query(SecondTestPage).filter(SecondTestPage.id == page_id).first()
    elif current_test.type == 'first_tests':
        current_page = db_sess.query(FirstTestPage).filter(FirstTestPage.id == page_id).first()
    else:
        current_page = db_sess.query(FirstTestPage).filter(FirstTestPage.id == page_id).first()
    current_test.pages.remove(current_page)
    db_sess.delete(current_page)
    db_sess.commit()
    return redirect('/test_page_creation/' + str(test_id))


@app.route('/delete_test/<int:test_id>', methods=['GET', 'POST'])
def delete_test(test_id):
    db_sess = db_session.create_session()
    current_test = db_sess.query(Test).filter(Test.id == test_id).first()
    for page in current_test.pages:
        current_test.pages.remove(page)
        db_sess.delete(page)
    db_sess.delete(current_test)
    db_sess.commit()
    return redirect('/created_test_page/' + str(current_user.id))


@app.route('/test_page_creation')
def test_page_creation():
    if current_user.is_authenticated:
        db_sess = db_session.create_session()
        current_test = db_sess.query(Test).filter(Test.id == current_user.get_id()).first()
        pages_list = current_test.pages
        return render_template('test_page_creation.html', pages=pages_list, test=current_test)
    else:
        return redirect("/login")


@app.route("/profile")
def profile():
    if current_user.is_authenticated:
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.id == current_user.get_id()).first()
        return render_template("profile.html", user_data=user)
    else:
        return redirect("/login")


@app.route('/user_edit', methods=['GET', 'POST'])
def edit_user():
    if current_user.is_authenticated:
        if request.method == "GET":
            form = SmallLoginForm()
            return render_template('user_edit.html', form=form, user_is_login=False)
        elif request.method == "POST":
            if request.form.get('main_button') == "d56b699830e77ba53855679cb1d252da":
                if current_user.is_authenticated:
                    db_sess = db_session.create_session()
                    user = db_sess.query(User).filter(User.id == current_user.get_id()).first()
                    if user and user.check_password(request.form.get('password')):
                        form = ChangeForm()
                        form.name.data = user.name
                        form.surname.data = user.surname
                        form.email.data = user.email
                        return render_template('user_edit.html', form=form, user_is_login=True)
                    elif user:
                        form = SmallLoginForm()
                        return render_template('user_edit.html', form=form, user_is_login=False,
                                               message='Неверный пароль')
            elif request.form.get('main_button') == "save":
                form = ChangeForm()
                if form.validate_on_submit():
                    if current_user.is_authenticated:
                        db_sess = db_session.create_session()
                        user = db_sess.query(User).filter(User.id == current_user.get_id()).first()
                        if user:
                            user.name = form.name.data
                            user.surname = form.surname.data
                            user.email = form.email.data
                            db_sess.commit()
                            return redirect('/profile')
    return redirect("/login")


@app.route('/registration', methods=['GET', 'POST'])
def registration():
    if request.method == "GET":
        if not current_user.is_authenticated:
            form = RegisterForm()
            return render_template('registration.html', title='Регистрация', form=form)
        return redirect('/profile')
    elif request.method == "POST":
        form = RegisterForm()
        if form.validate_on_submit():
            if form.password.data != form.password_again.data:
                return render_template('registration.html', form=form, message="Пароли не совпадают")
            db_sess = db_session.create_session()
            if db_sess.query(User).filter(User.email == form.email.data).first():
                return render_template('registration.html', form=form, message="Такой пользователь уже есть")
            user = User()
            user.name = form.name.data
            user.email = form.email.data
            user.surname = form.surname.data
            user.set_password(form.password.data)
            db_sess.add(user)
            db_sess.commit()
            login_user(user)
            if not os.path.exists('static/img/users/' +
                                  str(db_sess.query(User).filter(User.email == form.email.data).first().id)):
                os.mkdir('static/img/users/'
                         + str(db_sess.query(User).filter(User.email == form.email.data).first().id))
            return redirect('/profile')
        return redirect('/login')


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
    return render_template('login.html', form=form)


@app.route('/contacts')
def contacts():
    return render_template('contacts.html')


@app.route('/info')
def info():
    return render_template('info.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.errorhandler(404)
def page_not_found(expression):
    if expression:
        expression = 404
    else:
        expression = 403
    return render_template('error_404.html'), expression


if __name__ == '__main__':
    main()
