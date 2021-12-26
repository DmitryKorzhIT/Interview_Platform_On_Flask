from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from project.config import Config


app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)

from project import routes, models

from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView


# ------------------------------------------------- AUTHENTICATION -----------------------------------------------------
def create_app():

    db.init_app(app)

    # blueprint for auth routes in our app
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    # blueprint for non-auth parts of app
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
# ----------------------------------------------- END AUTHENTICATION ---------------------------------------------------


# ----------------------------------------------------- ADMIN ----------------------------------------------------------
app.config['FLASK_ADMIN_SWATCH'] = 'flatly'  # Set style
admin = Admin(app, name='interview platform', template_mode='bootstrap3')

admin.add_view(ModelView(models.User, db.session))
admin.add_view(ModelView(models.UserInterviewQuestion, db.session))
admin.add_view(ModelView(models.UserInterview, db.session))
admin.add_view(ModelView(models.Interview, db.session))
admin.add_view(ModelView(models.InterviewQuestion, db.session))
admin.add_view(ModelView(models.Question, db.session))
admin.add_view(ModelView(models.QuestionSet, db.session))
# --------------------------------------------------- END ADMIN --------------------------------------------------------
