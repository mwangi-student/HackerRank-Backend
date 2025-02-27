from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from datetime import datetime

metadata = MetaData()
db = SQLAlchemy(metadata=metadata)


class Student(db.Model):
    __tablename__ = "students"  

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(512), nullable=False) 
    cohort = db.Column(db.String(255))
    tm_id = db.Column(db.Integer, db.ForeignKey('tm.id'), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationship
    tm = db.relationship("TM", backref="students", cascade="all, delete", lazy=True)

class TM(db.Model):
    __tablename__ = "tm"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(512), nullable=False) 
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable = True)

class Assessment(db.Model):
    __tablename__ = "assessment"
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    title = db.Column(db.String(255), nullable = False)
    description = db.Column(db.String(255), nullable = False)
    difficulty = db.Column(db.Text, nullable = False)
    category = db.Column(db.String(255), nullable = False)
    constraints = db.Column(db.Text, nullable = False)
    tm_id = db.Column(db.Integer, db.ForeignKey('tm.id'), nullable= False)
    created_at = db.Column(db.DateTime, default= datetime.utcnow, nullable = False)

    tm = db.relationship('TM', backref= db.backref('assessment', lazy = True))

class AssessmentInvite(db.Model):
    __tablename__ = "assessmentinvite"
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    assessment_id = db.Column(db.Integer, db.ForeignKey('assessment.id'), nullable= False)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable= False)
    invited_by = db.Column(db.Integer, db.ForeignKey('tm.id'), nullable= False)
    status = db.Column(db.String(255), nullable = False)

    assessment = db.relationship('Assessment', backref = db.backref('assessmentinvite', lazy = True))
    student = db.relationship('Student', backref=db.backref('assessmentinvite', lazy=True))
    tm = db.relationship('TM', backref= db.backref('assessmentinvite', lazy = True))


class Feedback(db.Model):
    __tablename__ = "feedback"
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    question_id = db.Column(db.Integer, db.ForeignKey('questions.id'), nullable= False)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable= False)
    tm_id = db.Column(db.Integer, db.ForeignKey('tm.id'), nullable= False)
    feedback = db.Column(db.Text, nullable = False)
    created_at = db.Column(db.TIMESTAMP, default= datetime.utcnow, nullable = False)

    student = db.relationship('Student', backref= db.backref('feedback', lazy = True))
    tm = db.relationship('TM', backref= db.backref('feedback', lazy = True))
    question = db.relationship('Questions', backref= db.backref('feedback', lazy = True))


class Submission(db.Model):
    __tablename__ = "submission"
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable= False)
    question_id = db.Column(db.Integer, db.ForeignKey('questions.id'), nullable= False)
    assessment_id = db.Column(db.Integer, db.ForeignKey('assessment.id'), nullable= False)
    answer = db.Column(db.Text, nullable = False)
    status = db.Column(db.String(255), nullable = False)
    score = db.Column(db.Integer, nullable = False)
    created_at = db.Column(db.TIMESTAMP, default= datetime.utcnow, nullable = False)

    student = db.relationship('Student', backref= db.backref('submission', lazy = True))
    assessment = db.relationship('Assessment', backref = db.backref('submission', lazy = True))
    question = db.relationship('Questions', backref= db.backref('submission', lazy = True))

class Questions(db.Model):
    __tablename__ = "questions"
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    assessment_id = db.Column(db.Integer, db.ForeignKey('assessment.id'), nullable= False)
    type = db.Column(db.String(255), nullable = False)
    question_text = db.Column(db.Text, nullable = False)
    options = db.Column(db.JSON)
    correct_answer = db.Column(db.JSON)

    assessment = db.relationship('Assessment', backref = db.backref('questions', lazy = True))

class Discussion(db.Model):
    __tablename__ = "discussions"
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    assessment_id = db.Column(db.Integer, db.ForeignKey('assessment.id'), nullable= False)
    user_type = db.Column(db.String(255), nullable = False)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable= False)
    tm_id = db.Column(db.Integer, db.ForeignKey('tm.id'), nullable= False)
    comment = db.Column(db.Text, nullable = False)
    posted_at = db.Column(db.TIMESTAMP, default= datetime.utcnow, nullable = False)

    assessment = db.relationship('Assessment', backref = db.backref('discussions', lazy = True))
    student = db.relationship('Student', backref= db.backref('discussions', lazy = True))

class Leaderboard(db.Model):
    __tablename__ = "leaderboard"
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable= False)
    assessment_id = db.Column(db.Integer, db.ForeignKey('assessment.id'), nullable= False)
    total_score = db.Column(db.Integer, nullable = False)
    rank = db.Column(db.Integer, nullable = False)
    last_updated = db.Column(db.TIMESTAMP, default= datetime.utcnow, nullable = False)

    assessment = db.relationship('Assessment', backref = db.backref('leaderboard', lazy = True))
    student = db.relationship('Student', backref= db.backref('leaderboard', lazy = True))

class TokenBlocklist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    jti = db.Column(db.String(36), nullable=False, unique=True)
    created_at = db.Column(db.DateTime, nullable=False)

























