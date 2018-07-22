from flask import render_template, request, redirect, url_for, session, flash
from app import app
from app.application import Application
from app.models import User
from app.models import Diary
from app.models import diaryItem

application = Application()


@app.route('/')
@app.route('/home')
def index():
    """
    This method returns the home page of the application
    :return: 
    """
    return render_template('index.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    """
    This method shows the user the sign up page. It also signs up a user
    if all the required attributes are present and then redirects the
    user to their diary list
    :return: 
    """
    error = None
    if request.method == 'POST':
        if request.form['name'] and request.form['username'] and request.form['password'] \
                and request.form['password-confirmation']:

            if request.form['password'] == request.form['password-confirmation']:
                user = User(request.form['username'], request.form['password'], request.form['name'])
                if application.register_user(user):
                    flash("You have successfully signed up. Please Login")
                    return redirect(url_for('login'))
                return render_template('register.html', error="You are already signed up, please login")
            error = 'The passwords do not match'

    return render_template('register.html', error=error)


@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    This method logins in an already existing user if their username and password
    match those already stored.
    It also shows errors to the user if their password is wrong or they do not 
    already have an account.
    :return: 
    """
    error = None
    if request.method == 'POST':
        if request.form['username'] and request.form['password']:
            if application.does_user_exist(request.form['username']):
                if application.login_user(request.form['username'], request.form['password']):
                    session['username'] = request.form['username']
                    return redirect(url_for('mydiary'))
                return render_template('login.html', error="Incorrect password")
            return render_template('login.html', error="No account found, please sign up first")
        error = "Invalid credentials, try again"
    return render_template('login.html', error=error)


@app.route('/diary/list', methods=['GET', 'POST'])
def mydiary():
    """
    This method shows the user entries.
    When its a Post request a diary is created
    and attached to the user. Then redirected back 
    :return: 
    """
    error = None
    user = application.get_user(session['username'])
    if not user:
        return redirect(url_for('login'))
    if request.method == 'POST':
        name = request.form['name']
        if user.create_diary(Diary(application.generate_random_key(), name)):
            flash("You have successfully added a diary")
            return redirect(url_for('mydiary'))
        error = "Could not create the diary, it already exists"
    return render_template('mydiary.html', error=error, entries=user.get_entries(), user=user)


@app.route('/edit/diary/<entry_id>', methods=['GET', 'POST'])
def editdiary(entry_id):
    """
    This route enables a user to edit their entries
    :param entry_id: 
    :return: 
    """
    error = None
    user = application.get_user(session['username'])
    if not user:
        return redirect(url_for('login'))
    diary = user.get_diary(entry_id)
    if not diary:
        return redirect(url_for('mydiary'))
    if request.method == 'POST':
        if request.form['name']:
            if user.update_diary(entry_id, request.form['name']):
                flash("You have successfully updated your diary")
                return redirect(url_for('mydiary'))
        error = "Please provide the diary name"
    return render_template('modify.html', error=error, diary=diary, user=user)


@app.route('/delete/diary/<entry_id>', methods=['GET', 'POST'])
def deletediary(entry_id):
    """
    This route enables a user to delete a diary
    :param entry_id: 
    :return: 
    """
    error = None
    user = application.get_user(session['username'])
    if not user:
        return redirect(url_for('login'))
    diary = user.get_diary(entry_id)
    if not diary:
        return redirect(url_for('mydiary'))

    if request.method == 'POST':
        if user.delete_diary(entry_id):
            flash("You have successfully Deleted a diary")
            return redirect(url_for('mydiary'))
        error = "Could not delete the diary"
    return render_template('delete.html', error=error, diary=diary, user=user)


@app.route('/diary/items/<entry_id>', methods=['GET', 'POST'])
def diaryitems(entry_id):
    """
    Route to show and create diary items.
    :param entry_id: 
    :return: 
    """
    error = None
    user = application.get_user(session['username'])
    if not user:
        return redirect(url_for('login'))
    diary = user.get_diary(entry_id)
    if not diary:
        return redirect(url_for('mydiary'))

    if request.method == 'POST':
        if request.form['name']:
            if diary.create_item(
                    diaryItem(application.generate_random_key(), request.form['name'], request.form['description'],
                               request.form['deadline'])):
                flash("You have successfully added an Item to the diary")
                return redirect(url_for('diaryitems', entry_id=diary.id))
        error = "Item cannot be created"
    return render_template('mydiaryitem.html', error=error, diary=diary, user=user)


@app.route('/diary/item/<entry_id>/<item_id>', methods=['GET', 'POST'])
def edititem(entry_id, item_id):
    """
    Route to edit an item specified by the Id
    :param entry_id: 
    :param item_id: 
    :return: 
    """
    user = application.get_user(session['username'])
    if not user:
        return redirect(url_for('login'))
    diary = user.get_diary(entry_id)
    item = diary.get_item(item_id)
    if not diary and not item:
        return redirect(url_for('mydiary'))

    if request.method == 'POST':
        if request.form['name'] and request.form['description'] and request.form['deadline']:
            if diary.update_item(item_id, request.form['name'], request.form['description'],
                                  request.form['deadline']):
                flash("You have successfully updated your Item in the diary")
                return redirect(url_for('diaryitems', entry_id=diary.id))
    return render_template('modifyitem.html', diary=diary, item=item, user=user)


@app.route('/diary/item/delete/<entry_id>/<item_id>', methods=['GET', 'POST'])
def deleteitem(entry_id, item_id):
    """
    Route to delete an item from a diary specified by the Id.
    :param entry_id: 
    :param item_id: 
    :return: 
    """
    user = application.get_user(session['username'])
    if not user:
        return redirect(url_for('login'))
    diary = user.get_diary(entry_id)
    item = diary.get_item(item_id)
    if not diary and not item:
        return redirect(url_for('mydiary'))

    if request.method == 'POST':
        if diary.delete_item(item_id):
            flash('You have successfully deleted an Item from the diary')
            return redirect(url_for('diaryitems', entry_id=diary.id))
    return render_template('deleteitem.html', user=user, diary=diary, item=item)


@app.route('/logout')
def logout():
    """
    This methods clears the user session and logs the user out
    :return: 
    """
    session.pop('username', None)
    return redirect(url_for('login'))


@app.errorhandler(404)
def page_not_found(e):
    """
    The page to return in case a route is not defined.
    :param e: 
    :return: 
    """
    return render_template('404.html'), 404
