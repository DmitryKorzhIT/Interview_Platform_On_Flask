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
class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(200), unique=True)
    password = db.Column(db.String(200))
    name = db.Column(db.String(200))
    surname = db.Column(db.String(200), nullable=True)
    type = db.Column(db.String(200))

    user_interview_questions = db.relationship('UserInterviewQuestion', backref='user')
    user_interviews = db.relationship('UserInterview', backref='user')

    def __repr__(self):
        return '<User %r>' % self.login


class UserInterviewQuestion(db.Model):
    __tablename__ = 'user_interview_question'

    id = db.Column(db.Integer, primary_key=True)
    user_login = db.Column(db.String(200), db.ForeignKey('user.login'))
    mark = db.Column(db.Integer)
    # interview_question_id =

    def __repr__(self):
        return '<UserInterviewQuestion %r>' % self.id


class UserInterview(db.Model):
    __tablename__ = 'user_interview'

    id = db.Column(db.Integer, primary_key=True)
    user_login = db.Column(db.String(200), db.ForeignKey('user.login'))
    user_comment = db.Column(db.Text)
    # interview_id

    def __repr__(self):
        return '<UserInterview %r>' % self.id


class Interview(db.Model):
    __tablename__ = 'interview'

    id = db.Column(db.Integer, primary_key=True)
    candidate_name = db.Column(db.String(200))
    candidate_surname = db.Column(db.String(200))
    tags = db.Column(db.String(1000))  # Need to convert to JSON array
    date_time = db.Column(db.DateTime)
    link_zoom = db.Column(db.String(1000))
    total_mark = db.Column(db.Integer)  # Need to calculate by yourself

    interview_ids = db.relationship('InterviewQuestion', backref='interview')

    def __repr__(self):
        return 'Interview %r' % self.id


class InterviewQuestion(db.Model):
    __tablename__ = 'interview_question'

    id = db.Column(db.Integer, primary_key=True)
    interview_id = db.Column(db.Integer, db.ForeignKey('interview.id'))
    # question_id

    def __repr__(self):
        return 'InterviewQuestion %r' % self.id


class Question(db.Model):
    __tablename__ = 'question'

    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.Text)
    answear = db.Column(db.Text)
    tags = db.Column(db.String(1000))  # Need to be JSON array

    def __repr__(self):
        return 'Question %r' % self.id


class QuestionSet(db.Model):
    __tablename__ = 'question_set'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(1000))
    tags = db.Column(db.String(1000))  # Need to be JSON array

    def __repr__(self):
        return 'QuestionSet %r' % self.id
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

admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(UserInterviewQuestion, db.session))
admin.add_view(ModelView(UserInterview, db.session))
admin.add_view(ModelView(Interview, db.session))
admin.add_view(ModelView(InterviewQuestion, db.session))
admin.add_view(ModelView(Question, db.session))
admin.add_view(ModelView(QuestionSet, db.session))
# --------------------------------------------------- END ADMIN --------------------------------------------------------

if __name__ == '__main__':
    app.secret_key = 'super secret key'
    app.run(debug=True, host='0.0.0.0')
