from flask import render_template, request, redirect, url_for, session, flash
from app import app
from app.models import Diary
from app.models import diaryItem

@app.route('/api/v1/entries/<int:entry_id>', methods=['GET', 'POST'])
def diaryitems(entry_id):
    """
    Route to show and create diary items.
    :param entry_id: 
    :return: 
    """
    if request.method == 'POST':
        if request.form['name']:
            if Diary.create_item(
                    diaryItem(application.generate_random_key(), request.form['name'], request.form['description'],
                               request.form['deadline'])):
                flash("You have successfully added an Item to the diary")
                return redirect(url_for('diaryitems', entry_id=entry_id))
        error = "Item cannot be created"
    return render_template('mydiaryitem.html', error=error, diary=diary, user=user)


@app.route('/api/v1/entries/<int:entry_id>', methods=['GET', 'POST'])
def edititem(entry_id):
    """
    Route to edit an item specified by the Id
    :param entry_id: 
    :param entry_id: 
    :return: 
    """

    item = Diary.get_item(entry_id)
    if not item:
        return redirect(url_for('mydiary'))

    if request.method == 'POST':
        if request.form['name'] and request.form['description'] and request.form['deadline']:
            if Diary.update_item(entry_id, request.form['name'], request.form['description'],
                                  request.form['deadline']):
                flash("You have successfully updated your Item in the diary")
                return redirect(url_for('diaryitems', entry_id=entry_id))
    return render_template('modifyitem.html', diary=diary, item=item)


@app.route('/api/v1/entries/<int:entry_id>', methods=['GET', 'POST'])
def deleteitem(entry_id):
    """
    Route to delete an item from a diary specified by the Id.
    :param entry_id: 
    :param entry_id: 
    :return: 
    """
    item = Diary.get_item(entry_id)
    if not item:
        return redirect(url_for('mydiary'))

    if request.method == 'POST':
        if Diary.delete_item(entry_id):
            flash('You have successfully deleted an Item from the diary')
            return redirect(url_for('diaryitems', entry_id=entry_id))
    return render_template('deleteitem.html', diary=diary, item=item)


@app.errorhandler(404)
def page_not_found(e):
    """
    The page to return in case a route is not defined.
    :param e: 
    :return: 
    """
    return render_template('404.html'), 404
