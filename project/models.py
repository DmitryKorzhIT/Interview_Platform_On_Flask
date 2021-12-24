from project import db


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
    interview_question_id = db.Column(db.Integer, db.ForeignKey('interview_question.id'))
    user_login = db.Column(db.String(200), db.ForeignKey('user.login'))
    mark = db.Column(db.Integer)

    def __repr__(self):
        return '<UserInterviewQuestion %r>' % self.id


class UserInterview(db.Model):
    __tablename__ = 'user_interview'

    id = db.Column(db.Integer, primary_key=True)
    user_login = db.Column(db.String(200), db.ForeignKey('user.login'))
    interview_id = db.Column(db.Integer, db.ForeignKey('interview.id'))
    user_comment = db.Column(db.Text)

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
    total_mark = db.Column(db.Float)  # Need to calculate by yourself

    interview_ids = db.relationship('InterviewQuestion', backref='interview')
    interview_ids_1 = db.relationship('UserInterview', backref='interview')

    def __repr__(self):
        return 'Interview %r' % self.id


class InterviewQuestion(db.Model):
    __tablename__ = 'interview_question'

    id = db.Column(db.Integer, primary_key=True)
    interview_id = db.Column(db.Integer, db.ForeignKey('interview.id'))
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'))

    interview_question_ids = db.relationship('UserInterviewQuestion', backref='interview_question')

    def __repr__(self):
        return 'InterviewQuestion %r' % self.id


class Question(db.Model):
    __tablename__ = 'question'

    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.Text)
    answear = db.Column(db.Text)
    tags = db.Column(db.String(1000))  # Need to be JSON array

    question_ids = db.relationship('InterviewQuestion', backref='question')

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

