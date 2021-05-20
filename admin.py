from flask import Blueprint, render_template
from flask_login import login_required, current_user
from werkzeug.utils import redirect, secure_filename

from data import db_session
from data.news import News
from forms.delete_confirm import DeleteForm
from forms.news import NewsForm

admin = Blueprint('admin', 'admin')

def admin_protect(func):
    def decoreated_func(*args, **kwargs):
        if current_user.role == 'admin':
            return func(*args, **kwargs)
        else:
            return redirect('/')
    return decoreated_func


@admin.route('/admin/news', endpoint='get_news_list')
@admin_protect
@login_required
def get_news_list():
    db_sess = db_session.create_session()
    data = db_sess.query(News)
    return render_template("admin/news.html", news=data, title="Управление Новостями")

@admin.route('/admin/news_item/new',
             endpoint='new_news_item', methods=['GET', 'POST'])
@admin_protect
@login_required
def new_news_item():
    form = NewsForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        filename = secure_filename(form.image.data.filename)
        form.image.data.save('uploads/'+filename)
        news = News(form.title.data, form.content.data, '/img/'+filename, 1)
        db_sess.add(news)
        db_sess.commit()
        return redirect(f"/admin/news")
    return render_template('admin/news_item.html', title='Новая Новость', form=form)

@admin.route('/admin/news_item/delete/<int:id>',
             endpoint='delete_news_item', methods=['GET', 'POST'])
@admin_protect
@login_required
def delete_news_item(id):
    form = DeleteForm()
    if not form.validate_on_submit():
        form.id.data = id
        return render_template('admin/delete_element.html', title='Удалить Новость', form=form)
    elif form.confirm.data == True:
        del_id = form.id.data
        db_sess = db_session.create_session()
        news = db_sess.query(News).get(id)
        db_sess.delete(news)
        db_sess.commit()
    return redirect('/admin/news')

@admin.route('/admin/products',
             endpoint='get_products_list')
@admin_protect
@login_required
def get_products_list():
    return "products_list_page"

@admin.route('/admin/users',
             endpoint='get_users_list')
@admin_protect
@login_required
def get_users_list():
    return "users_list_page"