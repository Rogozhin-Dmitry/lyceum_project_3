import datetime
import os
import shutil
import json
import string
import random

from flask import Flask, render_template, redirect, request, session, abort
from flask_login import LoginManager
from flask_login import login_user, login_required, logout_user, current_user

from data import db_session
from data.tests import Test
from data.users import User
from data.categories import Category
from data.created_test import CreatedTest
from data.mailing_lists import MailingLists
from data.temporary_third_test_create import TemporaryThirdTestCreate
from data.temporary_third_test import TemporaryThirdTest
from data.temporary_first_test import TemporaryFirstTest
from data.temporary_first_test_create import TemporaryFirstTestCreate
from data.temporary_second_test import TemporarySecondTest
from data.temporary_second_test_create import TemporarySecondTestCreate

from forms.create_tests_form import TestCreateForm
from forms.user import RegisterForm, LoginForm, ChangeForm, SmallLoginForm

from extend_main_index_page import start_app

application = Flask(__name__)
application.config['PERMANENT_SESSION_LIFETIME'] = datetime.timedelta(days=365)
login_manager = LoginManager()
login_manager.init_app(application)
application.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
start_app(application)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


def main():
    db_session.global_init("db/site_data.db")
    db_sess = db_session.create_session()
    db_sess.query(Category).delete()

    first_language = Category(name="English")
    second_language = Category(name="Deutsch")
    db_sess.add(first_language)
    db_sess.add(second_language)
    db_sess.commit()
    application.run(port=5001, host='192.168.1.105')


@application.route('/email', methods=['POST'])
def email():
    if request.method == 'POST':
        db_sess = db_session.create_session()
        new_email = MailingLists()
        new_email.email = request.form['email']
        db_sess.add(new_email)
        db_sess.commit()
    return redirect('/')


@application.route('/index/', methods=['GET', 'POST'])
@application.route('/index/<int:page_id>', methods=['GET', 'POST'])
@application.route('/', methods=['GET', 'POST'])
@application.route('/<int:page_id>', methods=['GET', 'POST'])
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
    tests = db_sess.query(Test).filter(Test.open == 1).all()
    if len(tests) // 12 + 1 < page_id:
        abort(404)
    languages = {}
    for i in db_sess.query(Category).all():
        languages[i.id] = i.name
    for i in tests:
        i.test_language = languages[i.language_id]
    if user.current_filter == 1:
        tests = sorted(tests, key=lambda x: x.title)
    if user.current_filter == 2:
        tests = sorted(tests, key=lambda x: x.made_date, reverse=True)
    if user.current_filter == 3:
        tests = sorted(tests, key=lambda x: x.made_date)
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


@application.route('/my_tests/', methods=['GET', 'POST'])
@application.route('/my_tests/<int:page_id>', methods=['GET', 'POST'])
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
    tests = db_sess.query(Test).filter(Test.id.in_([int(i) for i in json.loads(user.user_tests).keys()])).all()
    if len(tests) // 12 + 1 < page_id:
        abort(404)
    languages = {}
    for i in db_sess.query(Category).all():
        languages[i.id] = i.name
    for i in tests:
        i.test_language = languages[i.language_id]
    if user.current_filter == 1:
        tests = sorted(tests, key=lambda x: x.title)
    if user.current_filter == 2:
        tests = sorted(tests, key=lambda x: x.made_date, reverse=True)
    if user.current_filter == 3:
        tests = sorted(tests, key=lambda x: x.made_date)
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


@application.route('/open_user_tests/', methods=['GET', 'POST'])
@application.route('/open_user_tests/<int:user_id>/', methods=['GET', 'POST'])
@application.route('/open_user_tests/<int:user_id>/<int:page_id>', methods=['GET', 'POST'])
def open_user_tests(user_id=1, page_id=1):
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
    tests = db_sess.query(Test).filter(Test.creator == user_id).filter(Test.open == 1).all()
    if len(tests) // 12 + 1 < page_id:
        abort(404)
    languages = {}
    for i in db_sess.query(Category).all():
        languages[i.id] = i.name
    for i in tests:
        i.test_language = languages[i.language_id]
    if user.current_filter == 1:
        tests = sorted(tests, key=lambda x: x.title)
    if user.current_filter == 2:
        tests = sorted(tests, key=lambda x: x.made_date, reverse=True)
    if user.current_filter == 3:
        tests = sorted(tests, key=lambda x: x.made_date)
    if len(tests) > 12 * page_id:
        next_page_id = page_id + 1
    else:
        next_page_id = 0
    if page_id > 1:
        previous_page_id = page_id - 1
    else:
        previous_page_id = 0
    author = db_sess.query(User).filter(User.id == user_id).first()
    if not author:
        abort(404)
    return render_template('open_user_tests.html', tests=tests[12 * (page_id - 1):12 * page_id],
                           current_filter=user.current_filter, page=[previous_page_id, next_page_id], author=author)


@application.route('/test_site', methods=['GET', 'POST'])
@application.route('/test_site/<int:test_id>', methods=['GET', 'POST'])
def test_site(test_id=1):
    if not current_user.is_authenticated:
        return redirect('/login')
    if request.method == 'POST':
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.id == current_user.get_id()).first()
        user_tests = json.loads(user.user_tests)
        if request.form['subscribe_button'] == 'Отписаться':
            user_tests.pop(str(test_id))
        else:
            user_tests[test_id] = {1: {}, 2: {}, 3: {}, 4: {}}
        user.user_tests = json.dumps(user_tests)
        db_sess.add(user)
        db_sess.commit()
    db_sess = db_session.create_session()
    test = db_sess.query(Test).filter(Test.id == test_id).first()
    if not (test.open or str(test.creator) == str(current_user.get_id())):
        abort(404)
    author = db_sess.query(User).filter(User.id == test.creator).first()
    language = db_sess.query(Category).filter(Category.id == test.language_id).first()
    test.test_language = language.name
    test.author = author
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.id == current_user.get_id()).first()
    subscribe = str(test.id) in json.loads(user.user_tests)
    return render_template('test_site.html', test=test, subscribe=subscribe, current_user=current_user)


@application.route('/second_test', methods=['GET', 'POST'])
@application.route('/second_test/<int:test_id>', methods=['GET', 'POST'])
@application.route('/second_test/<int:test_id>/<int:test_type>', methods=['GET', 'POST'])
def second_test(test_id=1, test_type=1):
    if not current_user.is_authenticated:
        return redirect('/login')
    db_sess = db_session.create_session()
    test_temp = db_sess.query(TemporarySecondTest).filter(TemporarySecondTest.user_id == current_user.get_id()).filter(
        TemporarySecondTest.test_id == test_id).first()
    if not test_temp:
        user = db_sess.query(User).filter(User.id == current_user.get_id()).first()
        test = db_sess.query(Test).filter((Test.id == test_id)).first()
        if not test or str(test.id) not in json.loads(user.user_tests) or not test.type == 'second_tests':
            abort(404)
        test_temp = TemporarySecondTest()
        test_temp.user_id = current_user.get_id()
        test_temp.test_id = test.id
        test_temp.test_type = test_type
        if test_type == 1:
            test_temp.data = test.data
        else:
            test_data = json.loads(test.data)
            test_data_1 = {}
            j = 1
            test_data_keys = list(test_data.keys())
            random.shuffle(test_data_keys)
            for i in test_data_keys:
                test_data_1[j] = test_data[i]
                j += 1
            test_temp.data = json.dumps(test_data_1)
        db_sess.add(test_temp)
        db_sess.commit()
    else:
        if request.method == "POST":
            result_data = json.loads(test_temp.result_data)
            result_data[str(test_temp.selected_page)] = [request.form['answer_1'], request.form['answer_2'],
                                                         request.form['answer_3']]
            test_temp.result_data = json.dumps(result_data)
            test_temp.selected_page += 1
            data = json.loads(test_temp.data)
            if test_temp.selected_page > len(list(data.keys())):
                score = 0
                error_table = []
                for i in data:
                    for j in data[i][:-1]:
                        if j.lower() == result_data[i][data[i][:-1].index(j)].lower():
                            score += 0.3333333
                        else:
                            error_table.append([j.lower(), result_data[i][data[i][:-1].index(j)].lower()])
                user = db_sess.query(User).filter(User.id == current_user.get_id()).first()
                user_data = json.loads(user.user_tests)
                if 'max_count' in user_data[str(test_id)][str(test_temp.test_type)] \
                        and int(user_data[str(test_id)][str(test_temp.test_type)]['max_count']) > score:
                    max_score = int(user_data[str(test_id)][str(test_temp.test_type)]['max_count'])
                else:
                    user_data[str(test_id)][str(test_temp.test_type)]['max_count'] = score
                    user.user_tests = json.dumps(user_data)
                    max_score = round(score, 2)
                db_sess.delete(test_temp)
                db_sess.commit()
                return render_template('test_result.html', score=round(score, 2), test_id=test_id, max_score=max_score,
                                       pages=len(list(data.keys())), error_table=error_table)
            db_sess.commit()
    return render_template('second_test.html', name=json.loads(test_temp.data)[str(test_temp.selected_page)][-1],
                           test=test_temp)


@application.route('/second_test_create', methods=['GET', 'POST'])
def second_test_create():
    if not current_user.is_authenticated:
        return redirect('/login')
    db_sess = db_session.create_session()
    test = db_sess.query(CreatedTest).filter((CreatedTest.creator == current_user.get_id())).first()
    if not test:
        return redirect('/create_test')
    temporary = db_sess.query(TemporarySecondTestCreate).filter((TemporarySecondTestCreate.test_id == test.id)).first()
    if not (test and test.type == 'second_tests'):
        redirect('/create_test')
    if request.method == "POST":
        args = {}
        for i in str(request.form).split("ImmutableMultiDict([('")[-1].split("')])")[0].split("'), ('"):
            args[i.split("', '")[0]] = i.split("', '")[1]
        data = json.loads(temporary.data)
        for i in args:
            if i not in ['append', 'delete', 'create']:
                data[i] = args[i]
        temporary.data = json.dumps(data)
        if 'append' in args:
            if temporary.count_of_tr != 50:
                temporary.count_of_tr += 5
            db_sess.commit()
        elif 'delete' in args:
            if temporary.count_of_tr != 5:
                temporary.count_of_tr -= 5
            db_sess.commit()
        else:
            new_test = Test()
            new_test.title = test.title
            new_test.title_picture = test.title_picture
            new_test.type = 'second_tests'
            new_test.made_date = test.made_date
            new_test.language_id = test.language_id
            new_test.creator = test.creator
            new_test.open = test.open
            new_test.description = test.description
            new_data = {}
            count = 1
            for i in data:
                if data[i] and i.endswith('0') and data[i[:-1] + '1'] and data[i[:-1] + '2'] and data[i[:-1] + '3']:
                    new_data[count] = [data[i], data[i[:-1] + '1'], data[i[:-1] + '2'], data[i[:-1] + '3']]
                    count += 1
            new_test.data = json.dumps(new_data)
            db_sess.add(new_test)
            db_sess.delete(test)
            db_sess.commit()
            db_sess = db_session.create_session()
            user = db_sess.query(User).filter(User.id == current_user.get_id()).first()
            test = db_sess.query(Test).filter((Test.creator == user.id), (Test.title == test.title)).first()
            if not os.path.exists('static/images/test/' + str(test.id)):
                os.mkdir('static/images/test/' + str(test.id))
                os.mkdir('static/images/test/' + str(test.id) + '/title')
                os.mkdir('static/images/test/' + str(test.id) + '/data')
            shutil.move(f"static/{test.title_picture}",
                        f"static/images/test/{test.id}/title/{test.title_picture.split('/')[-1]}")
            test.title_picture = f"images/test/{test.id}/title/{test.title_picture.split('/')[-1]}"
            user_tests = json.loads(user.user_tests)
            user_tests[test.id] = {1: {}, 2: {}, 3: {}, 4: {}}
            user.user_tests = json.dumps(user_tests)
            db_sess.add(user)
            db_sess.delete(temporary)
            db_sess.commit()
            return redirect('/my_tests')
    return render_template('second_test_create.html', count_of_tr=temporary.count_of_tr,
                           column_values=json.loads(temporary.data))


@application.route('/first_test', methods=['GET', 'POST'])
@application.route('/first_test/<int:test_id>', methods=['GET', 'POST'])
@application.route('/first_test/<int:test_id>/<int:test_type>', methods=['GET', 'POST'])
def first_test(test_id=1, test_type=1):
    if not current_user.is_authenticated:
        return redirect('/login')
    db_sess = db_session.create_session()
    test_temp = db_sess.query(TemporaryFirstTest).filter(TemporaryFirstTest.user_id == current_user.get_id()).filter(
        TemporaryFirstTest.test_id == test_id).first()
    if not test_temp:
        user = db_sess.query(User).filter(User.id == current_user.get_id()).first()
        test = db_sess.query(Test).filter((Test.id == test_id)).first()
        if not test or str(test.id) not in json.loads(user.user_tests) or not test.type == 'first_tests':
            abort(404)
        test_temp = TemporaryFirstTest()
        test_temp.user_id = current_user.get_id()
        test_temp.test_id = test.id
        test_temp.test_type = test_type
        if test_type == 1:
            test_temp.data = test.data
        else:
            test_data = json.loads(test.data)
            test_data_1 = {}
            j = 1
            test_data_keys = list(test_data.keys())
            random.shuffle(test_data_keys)
            for i in test_data_keys:
                test_data_1[j] = test_data[i]
                j += 1
            test_temp.data = json.dumps(test_data_1)
        db_sess.add(test_temp)
        db_sess.commit()
    else:
        if request.method == "POST":
            result_data = json.loads(test_temp.result_data)
            result_data[str(test_temp.selected_page)] = request.form['answer']
            test_temp.result_data = json.dumps(result_data)
            test_temp.selected_page += 1
            data = json.loads(test_temp.data)
            if test_temp.selected_page > len(list(data.keys())):
                score = 0
                error_table = []
                for i in data:
                    if data[i][0].lower() == result_data[i].lower():
                        score += 1
                    else:
                        error_table.append([data[i][0].lower(), result_data[i].lower()])
                user = db_sess.query(User).filter(User.id == current_user.get_id()).first()
                user_data = json.loads(user.user_tests)
                if 'max_count' in user_data[str(test_id)][str(test_temp.test_type)] \
                        and int(user_data[str(test_id)][str(test_temp.test_type)]['max_count']) > score:
                    max_score = int(user_data[str(test_id)][str(test_temp.test_type)]['max_count'])
                else:
                    user_data[str(test_id)][str(test_temp.test_type)]['max_count'] = score
                    user.user_tests = json.dumps(user_data)
                    max_score = score
                db_sess.delete(test_temp)
                db_sess.commit()
                return render_template('test_result.html', score=score, test_id=test_id, max_score=max_score,
                                       pages=len(list(data.keys())), error_table=error_table)
            db_sess.commit()
    return render_template('first_test.html', name=json.loads(test_temp.data)[str(test_temp.selected_page)][1],
                           test=test_temp)


@application.route('/first_test_create', methods=['GET', 'POST'])
def first_test_create():
    if not current_user.is_authenticated:
        return redirect('/login')
    db_sess = db_session.create_session()
    test = db_sess.query(CreatedTest).filter((CreatedTest.creator == current_user.get_id())).first()
    if not test:
        return redirect('/create_test')
    temporary = db_sess.query(TemporaryFirstTestCreate).filter((TemporaryFirstTestCreate.test_id == test.id)).first()
    if not (test and test.type == 'first_tests'):
        redirect('/create_test')
    data_temp = json.loads(temporary.data)

    if request.method == 'POST':
        if temporary.load_image:
            if str(request.files) == "ImmutableMultiDict([('image', <FileStorage: '' ('application/octet-stream')>)])":
                args = {}
                for i in str(request.form).split("ImmutableMultiDict([('")[-1].split("')])")[0].split("'), ('"):
                    args[i.split("', '")[0]] = i.split("', '")[1]
                if 'next_page' in args:
                    temporary.load_image = False
                else:
                    name = data_temp.pop(str(list(args.keys())[0][:-2].split('_')[-1]))
                    os.remove(f"static/images/temp/{name}")
            else:
                data = request.files['image']
                if data_temp:
                    num = max([int(i.split('_')[0]) for i in data_temp.keys()]) + 1
                else:
                    num = 0
                name = ''.join(random.choice(string.ascii_lowercase) for _ in range(8))
                data.save(f"static/images/temp/{name}.jpg")
                data_temp[str(num)] = f'{name}.jpg'
            temporary.data = json.dumps(data_temp)
            db_sess.commit()
        else:
            args = {}
            for i in str(request.form).split("ImmutableMultiDict([('")[-1].split("')])")[0].split("'), ('"):
                args[i.split("', '")[0]] = i.split("', '")[1]
            if 'back' in args:
                temporary.load_image = True
            else:
                args.pop('create')
                new_test = Test()
                new_test.title = test.title
                new_test.title_picture = test.title_picture
                new_test.type = 'first_tests'
                new_test.made_date = test.made_date
                new_test.language_id = test.language_id
                new_test.creator = test.creator
                new_test.open = test.open
                new_test.description = test.description
                data = {}
                for i in args:
                    num = i.replace('column_', '')
                    data[num] = [args[i], data_temp[num]]
                count = 1
                data_1 = {}
                for i in data:
                    data_1[count] = data[i]
                    count += 1
                new_test.data = json.dumps(data_1)
                db_sess.add(new_test)
                db_sess.delete(test)
                db_sess.commit()
                db_sess = db_session.create_session()
                user = db_sess.query(User).filter(User.id == current_user.get_id()).first()
                test = db_sess.query(Test).filter((Test.creator == user.id), (Test.title == test.title)).first()
                if not os.path.exists('static/images/test/' + str(test.id)):
                    os.mkdir('static/images/test/' + str(test.id))
                    os.mkdir('static/images/test/' + str(test.id) + '/title')
                    os.mkdir('static/images/test/' + str(test.id) + '/data')
                shutil.move(f"static/{test.title_picture}",
                            f"static/images/test/{test.id}/title/{test.title_picture.split('/')[-1]}")
                test.title_picture = f"images/test/{test.id}/title/{test.title_picture.split('/')[-1]}"
                user_tests = json.loads(user.user_tests)
                user_tests[test.id] = {1: {}, 2: {}}
                user.user_tests = json.dumps(user_tests)
                for i in data_1:
                    shutil.move(f"static/images/temp/{data_1[i][1]}",
                                f"static/images/test/{test.id}/data/{data_1[i][1]}")

                db_sess.add(user)
                db_sess.delete(temporary)
                db_sess.commit()
                return redirect('/my_tests')
            db_sess.commit()
    if temporary.load_image:
        return render_template('first_test_create_image_load.html', data=data_temp, test=test)
    else:
        return render_template('first_test_create.html', data=data_temp, test=test)


@application.route('/third_test', methods=['GET', 'POST'])
@application.route('/third_test/<int:test_id>', methods=['GET', 'POST'])
@application.route('/third_test/<int:test_id>/<int:test_type>', methods=['GET', 'POST'])
def third_test(test_id=1, test_type=1):
    if not current_user.is_authenticated:
        return redirect('/login')
    db_sess = db_session.create_session()
    test_temp = db_sess.query(TemporaryThirdTest).filter(TemporaryThirdTest.user_id == current_user.get_id()).filter(
        TemporaryThirdTest.test_id == test_id).first()
    if not test_temp:
        user = db_sess.query(User).filter(User.id == current_user.get_id()).first()
        test = db_sess.query(Test).filter((Test.id == test_id)).first()
        if not test or str(test.id) not in json.loads(user.user_tests) or not test.type == 'third_tests':
            abort(404)
        test_temp = TemporaryThirdTest()
        test_temp.user_id = current_user.get_id()
        test_temp.test_id = test.id
        test_temp.test_type = test_type
        if test_type == 1:
            test_temp.data = test.data
        elif test_type == 2:
            test_data = json.loads(test.data)
            test_data_1 = {}
            j = 1
            test_data_keys = list(test_data.keys())
            random.shuffle(test_data_keys)
            for i in test_data_keys:
                test_data_1[j] = test_data[i]
                j += 1
            test_temp.data = json.dumps(test_data_1)
        elif test_type == 3:
            test_data = json.loads(test.data)
            test_data_1 = {}
            for i in test_data:
                test_data_1[i] = (test_data[i][1], test_data[i][0])
            test_temp.data = json.dumps(test_data_1)
        else:
            test_data = json.loads(test.data)
            test_data_1 = {}
            j = 1
            test_data_keys = list(test_data.keys())
            random.shuffle(test_data_keys)
            for i in test_data_keys:
                test_data_1[j] = (test_data[i][1], test_data[i][0])
                j += 1
            test_temp.data = json.dumps(test_data_1)
        db_sess.add(test_temp)
        db_sess.commit()
    else:
        if request.method == "POST":
            result_data = json.loads(test_temp.result_data)
            result_data[str(test_temp.selected_page)] = request.form['answer']
            test_temp.result_data = json.dumps(result_data)
            test_temp.selected_page += 1
            data = json.loads(test_temp.data)
            if test_temp.selected_page > len(list(data.keys())):
                score = 0
                error_table = []
                for i in data:
                    if data[i][1].lower() == result_data[i].lower():
                        score += 1
                    else:
                        error_table.append([data[i][0].lower(), result_data[i].lower()])
                user = db_sess.query(User).filter(User.id == current_user.get_id()).first()
                user_data = json.loads(user.user_tests)
                if 'max_count' in user_data[str(test_id)][str(test_temp.test_type)] \
                        and int(user_data[str(test_id)][str(test_temp.test_type)]['max_count']) > score:
                    max_score = int(user_data[str(test_id)][str(test_temp.test_type)]['max_count'])
                else:
                    user_data[str(test_id)][str(test_temp.test_type)]['max_count'] = score
                    user.user_tests = json.dumps(user_data)
                    max_score = score
                db_sess.delete(test_temp)
                db_sess.commit()
                return render_template('test_result.html', score=score, test_id=test_id, max_score=max_score,
                                       pages=len(list(data.keys())), error_table=error_table)
            db_sess.commit()
    return render_template('third_test.html', name=json.loads(test_temp.data)[str(test_temp.selected_page)][0])


@application.route('/third_test_create', methods=['GET', 'POST'])
def third_test_create():
    if not current_user.is_authenticated:
        return redirect('/login')
    db_sess = db_session.create_session()
    test = db_sess.query(CreatedTest).filter((CreatedTest.creator == current_user.get_id())).first()
    if not test:
        return redirect('/create_test')
    temporary = db_sess.query(TemporaryThirdTestCreate).filter((TemporaryThirdTestCreate.test_id == test.id)).first()
    if not (test and test.type == 'third_tests'):
        redirect('/create_test')
    if request.method == "POST":
        args = {}
        for i in str(request.form).split("ImmutableMultiDict([('")[-1].split("')])")[0].split("'), ('"):
            args[i.split("', '")[0]] = i.split("', '")[1]
        data = json.loads(temporary.data)
        for i in args:
            if i not in ['append', 'delete', 'create']:
                data[i] = args[i]
        temporary.data = json.dumps(data)
        if 'append' in args:
            if temporary.count_of_tr != 50:
                temporary.count_of_tr += 5
            db_sess.commit()
        elif 'delete' in args:
            if temporary.count_of_tr != 5:
                temporary.count_of_tr -= 5
            db_sess.commit()
        else:
            new_test = Test()
            new_test.title = test.title
            new_test.title_picture = test.title_picture
            new_test.type = 'third_tests'
            new_test.made_date = test.made_date
            new_test.language_id = test.language_id
            new_test.creator = test.creator
            new_test.open = test.open
            new_test.description = test.description
            new_data = {}
            count = 1
            for i in data:
                if data[i] and i.endswith('0') and data[i[:-1] + '1']:
                    new_data[count] = [data[i], data[i[:-1] + '1']]
                    count += 1
            new_test.data = json.dumps(new_data)
            db_sess.add(new_test)
            db_sess.delete(test)
            db_sess.commit()
            db_sess = db_session.create_session()
            user = db_sess.query(User).filter(User.id == current_user.get_id()).first()
            test = db_sess.query(Test).filter((Test.creator == user.id), (Test.title == test.title)).first()
            if not os.path.exists('static/images/test/' + str(test.id)):
                os.mkdir('static/images/test/' + str(test.id))
                os.mkdir('static/images/test/' + str(test.id) + '/title')
                os.mkdir('static/images/test/' + str(test.id) + '/data')
            shutil.move(f"static/{test.title_picture}",
                        f"static/images/test/{test.id}/title/{test.title_picture.split('/')[-1]}")
            test.title_picture = f"images/test/{test.id}/title/{test.title_picture.split('/')[-1]}"
            user_tests = json.loads(user.user_tests)
            user_tests[test.id] = {1: {}, 2: {}, 3: {}, 4: {}}
            user.user_tests = json.dumps(user_tests)
            db_sess.add(user)
            db_sess.delete(temporary)
            db_sess.commit()
            return redirect('/my_tests')
    return render_template('third_test_create.html', count_of_tr=temporary.count_of_tr,
                           column_values=json.loads(temporary.data))


@application.route('/create_test', methods=['GET', 'POST'])
def test_create():
    if not current_user.is_authenticated:
        return redirect('/login')
    form = TestCreateForm()
    db_sess = db_session.create_session()
    test = db_sess.query(CreatedTest).filter((CreatedTest.creator == current_user.get_id())).first()
    if test:
        if test.type == 'first_tests':
            return redirect('/first_test_create')
        elif test.type == 'second_tests':
            return redirect('/second_test_create')
        else:
            return redirect('/third_test_create')
    if request.method == "POST":
        if form.validate_on_submit():
            args = {}
            for i in str(request.form).split("ImmutableMultiDict([('")[-1].split("')])")[0].split("'), ('"):
                args[i.split("', '")[0]] = i.split("', '")[1]
            new_test = CreatedTest()
            if args['types'] == 'Первый тип':
                new_test.type = 'first_tests'
            elif args['types'] == 'Второй тип':
                new_test.type = 'second_tests'
            else:
                new_test.type = 'third_tests'
            new_test.title = form.title.data
            new_test.language_id = db_sess.query(Category).filter(Category.name == args['language']).first().id
            new_test.creator = current_user.get_id()
            new_test.open = args['open'] != 'Только ваш'
            new_test.description = form.description.data
            db_sess.add(new_test)
            test = db_sess.query(CreatedTest).filter((CreatedTest.title == form.title.data),
                                                     (CreatedTest.creator == current_user.get_id())).first()
            if form.title_picture.data.filename != '' and \
                    form.title_picture.data.filename[form.title_picture.data.filename.index('.') + 1:] \
                    in ["jpg", "bmp", "png", "jpeg", "gif", "cdr", "svg"]:
                name = ''.join(random.choice(string.ascii_lowercase) for _ in range(8))
                form.title_picture.data.save(f'static/images/temp/{name}.jpg')
                test.title_picture = f'images/temp/{name}.jpg'
            else:
                name = ''.join(random.choice(string.ascii_lowercase) for _ in range(8))
                shutil.copyfile("static/images/hero/hero-001-1.jpg",
                                f'static/images/temp/{name}.jpg')
                test.title_picture = f'images/temp/{name}.jpg'

            if test.type == 'first_tests':
                temporary = TemporaryFirstTestCreate()
                temporary.test_id = test.id
                db_sess.add(temporary)
                db_sess.commit()
                return redirect('/first_test_create')
            elif test.type == 'second_tests':
                temporary = TemporarySecondTestCreate()
                temporary.test_id = test.id
                db_sess.add(temporary)
                db_sess.commit()
                return redirect('/second_test_create')
            else:
                temporary = TemporaryThirdTestCreate()
                temporary.test_id = test.id
                db_sess.add(temporary)
                db_sess.commit()
                return redirect('/third_test_create')
    return render_template('test_create.html', form=form, languages=[i.name for i in db_sess.query(Category).all()],
                           types=['Первый тип', 'Второй тип', 'Список слов'])


@application.route("/profile")
def profile():
    if current_user.is_authenticated:
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.id == current_user.get_id()).first()
        return render_template("profile.html", user_data=user)
    else:
        return redirect("/login")


@application.route('/user_edit', methods=['GET', 'POST'])
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


@application.route('/registration', methods=['GET', 'POST'])
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
            return redirect('/profile')
        return redirect('/login')


@application.route('/login', methods=['GET', 'POST'])
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


@application.route('/contacts')
def contacts():
    return render_template('contacts.html')


@application.route('/info')
def info():
    return render_template('info.html')


@application.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@application.errorhandler(404)
def page_not_found(expression):
    if expression:
        expression = 404
    else:
        expression = 403
    return render_template('error_404.html'), expression


if __name__ == '__main__':
    main()
