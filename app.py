# ----------------------------------------------------- IMPORT ---------------------------------------------------------
from flask import Flask, request, redirect
from flask import render_template  # Using for html templates
from flask import url_for

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
# --------------------------------------------------- END IMPORT -------------------------------------------------------


# ---------------------------------------------------- SETTINGS --------------------------------------------------------
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI']='postgresql://postgres:1@localhost/articles'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
# -------------------------------------------------- END SETTINGS ------------------------------------------------------


# ----------------------------------------------------- CLASSES --------------------------------------------------------
class Article(db.Model):
    __tablename__='articles'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    intro = db.Column(db.String(300), nullable=False)
    text = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Article %r>' % self.id


class User(db.Model):
    column_display_pk = True
    user_login = db.Column(db.String(200), primary_key=True)  # Need to do as a primary key
    user_password = db.Column(db.String(200))
    user_name = db.Column(db.String(200))
    user_surname = db.Column(db.String(200), nullable=True)
    user_type = db.Column(db.String(200))

    def __repr__(self):
        return '<User %r>' % self.user_login



# class User_interview(db.Model):
#     pass
#
#
# class Interview(db.Model):
#     pass
#
#
# class Interview_question(db.Model):
#     pass
#
#
# class User_interview_question(db.Model):
#     pass
#
#
# class Question(db.Model):
#     pass
#
#
# class Question_set(db.Model):
#     pass
# --------------------------------------------------- END CLASSES ------------------------------------------------------


# ----------------------------------------------------- VIEWS ----------------------------------------------------------
@app.route('/')  # '@' is a decorator. In brackets path to a specific page on a website.
@app.route('/home')
def index():
    return render_template("index.html")  # Show specific page from 'templates' directory on domain name '.../home'


@app.route('/about')
def about():
    return render_template("about.html")


@app.route('/posts')
def posts():
    articles = Article.query.order_by(Article.date.desc()).all()
    return render_template("posts.html", articles=articles)


@app.route('/posts/<int:id>')
def post_detail(id):
    article = Article.query.get(id)
    return render_template("post_detail.html", article=article)


@app.route('/posts/<int:id>/del')
def post_delete(id):
    article = Article.query.get_or_404(id)

    try:
        db.session.delete(article)
        db.session.commit()
        return redirect('/posts')
    except:
        return "Something went wrong when you tried to delete an Article. Error."


@app.route('/posts/<int:id>/update', methods=['POST', 'GET'])
def post_update(id):
    article = Article.query.get(id)
    if request.method == 'POST':
        article.title = request.form['title']
        article.intro = request.form['intro']
        article.text = request.form['text']

        try:
            db.session.commit()
            return redirect('/posts')
        except:
            return "Something went wrong with editing. Error."

    else:
        return render_template("post_update.html", article=article)


@app.route('/create-article', methods=['POST', 'GET'])
def create_article():
    if request.method == 'POST':
        title = request.form['title']
        intro = request.form['intro']
        text = request.form['text']

        article = Article(title=title, intro=intro, text=text)

        try:
            db.session.add(article)
            db.session.commit()
            return redirect('/posts')
        except:
            return "Something went wrong. Error."

    else:
        return render_template("create-article.html")


# @app.route('/user/<string:name>/<int:id>')  # <string:name> is name of a unique user.
# def user(name, id):
#     return "User page: " + name + " - " + str(id)
# --------------------------------------------------- END VIEWS --------------------------------------------------------


# ----------------------------------------------------- ADMIN ----------------------------------------------------------
app.config['FLASK_ADMIN_SWATCH'] = 'flatly'  # Set style
admin = Admin(app, name='interview platform', template_mode='bootstrap3')

admin.add_view(ModelView(Article, db.session))
admin.add_view(ModelView(User, db.session))
# --------------------------------------------------- END ADMIN --------------------------------------------------------

if __name__ == '__main__':
    app.secret_key = 'super secret key'
    app.run(debug=True)
