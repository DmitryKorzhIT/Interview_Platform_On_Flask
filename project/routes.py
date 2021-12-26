from project import app, db

from flask import Flask, request, redirect
from flask import render_template  # Using for html templates


# ----------------------------------------------------- VIEWS ----------------------------------------------------------
@app.route('/')  # '@' is a decorator. In brackets path to a specific page on a website.
@app.route('/home')
def index():
    user = {'username': 'Miguel'}
    posts = [
        {'author': {'username': 'Jerry'},
         'body': 'Beeing a good author is a job 24/7.'},
        {'author': {'username': 'Susan'},
         'body': 'The weather is always good.'},
        {'author': {'username': 'Oakla'},
         'body': 'Listen the music.'},
        {'author': {'username': 'Pronx'},
         'body': 'Or watch the galery.'}
    ]
    return render_template("index.html", user=user, posts=posts)


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

