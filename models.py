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

    tm = db.relationship("TM", backref="students", cascade="all, delete", lazy=True)


class TM(db.Model):
    __tablename__ = "tm"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(512), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=True)


class Assessment(db.Model):
    __tablename__ = "assessment"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    difficulty = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(255), nullable=False)
    assessment_type = db.Column(db.String(500), nullable=False)
    publish = db.Column(db.String(500), nullable=False)
    constraints = db.Column(db.Text, nullable=False)
    time_limit = db.Column(db.Integer, nullable=False)
    tm_id = db.Column(db.Integer, db.ForeignKey('tm.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    tm = db.relationship('TM', backref=db.backref('assessments', lazy=True))
    questions = db.relationship('Questions', backref='assessment', lazy=True)
    code_challenge = db.relationship('CodeChallenge', backref='assessment', uselist=False)
    invites = db.relationship('AssessmentInvite', backref='assessment', lazy=True)
    scores = db.relationship('Scores', backref='assessment', lazy=True)


class Questions(db.Model):
    __tablename__ = "questions"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    assessment_id = db.Column(db.Integer, db.ForeignKey('assessment.id'), nullable=False)
    question_text = db.Column(db.Text, nullable=False)
    choice_a = db.Column(db.String(255), nullable=False)
    choice_b = db.Column(db.String(255), nullable=False)
    choice_c = db.Column(db.String(255), nullable=False)
    choice_d = db.Column(db.String(255), nullable=False)
    correct_answer = db.Column(db.String(1), nullable=False)


class CodeChallenge(db.Model):
    __tablename__ = "code_challenge"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    assessment_id = db.Column(db.Integer, db.ForeignKey('assessment.id'), nullable=False)
    task = db.Column(db.Text, nullable=False)
    example = db.Column(db.Text, nullable=False)
    input_format = db.Column(db.String(255), nullable=False)
    output_format = db.Column(db.String(255), nullable=False)
    constraints = db.Column(db.Text, nullable=False)
    sample_input_1 = db.Column(db.String(255), nullable=False)
    sample_input_2 = db.Column(db.String(255), nullable=False)
    sample_input_3 = db.Column(db.String(255), nullable=False)
    sample_input_4 = db.Column(db.String(255), nullable=False)
    sample_output_1 = db.Column(db.String(255), nullable=False)
    sample_output_2 = db.Column(db.String(255), nullable=False)
    sample_output_3 = db.Column(db.String(255), nullable=False)
    sample_output_4 = db.Column(db.String(255), nullable=False)


class AssessmentInvite(db.Model):
    __tablename__ = "assessment_invite"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    assessment_id = db.Column(db.Integer, db.ForeignKey('assessment.id'), nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
    tm_id = db.Column(db.Integer, db.ForeignKey('tm.id'), nullable=False)
    status = db.Column(db.String(255), nullable=False)  # pending, accepted, declined
    created_at = db.Column(db.TIMESTAMP, default=datetime.utcnow, nullable=False)
    completed_at = db.Column(db.DateTime, nullable=True)

    student = db.relationship('Student', backref=db.backref('assessment_invites', lazy=True))
    tm = db.relationship('TM', backref=db.backref('assessment_invites', lazy=True))


class AssessmentSubmission(db.Model):
    __tablename__ = "assessment_submission"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
    assessment_id = db.Column(db.Integer, db.ForeignKey('assessment.id'), nullable=False)
    submitted_at = db.Column(db.TIMESTAMP, default=datetime.utcnow, nullable=False)

    # Relationships
    student = db.relationship('Student', backref='submissions')  # Relationship with Student
    assessment = db.relationship('Assessment', backref='submissions')  # Relationship with Assessment
    mcq_answers = db.relationship('MCQSubmission', backref='assessment_submission', lazy=True)  # Relationship with MCQSubmission
    code_submission = db.relationship('CodeSubmission', backref='assessment_submission', uselist=False)  # Relationship with CodeSubmission

class MCQSubmission(db.Model):
    __tablename__ = "mcq_submission"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    assessment_submission_id = db.Column(db.Integer, db.ForeignKey('assessment_submission.id'), nullable=False)
    selected_answer = db.Column(db.String(1), nullable=False)
    question_id = db.Column(db.Integer, nullable=False)
    selected_answer = db.Column(db.String(255), nullable=False)

class CodeSubmission(db.Model):
    __tablename__ = "code_submission"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    assessment_submission_id = db.Column(db.Integer, db.ForeignKey('assessment_submission.id'), nullable=False)
    codechallenge_id = db.Column(db.Integer, db.ForeignKey('code_challenge.id'), nullable=False)
    selected_answer = db.Column(db.String(500), nullable=False)

class Scores(db.Model):
    __tablename__ = "scores"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
    assessment_id = db.Column(db.Integer, db.ForeignKey('assessment.id'), nullable=False)
    score = db.Column(db.Integer, nullable=False)

    student = db.relationship('Student', backref=db.backref('scores', lazy=True))



class Feedback(db.Model):
    __tablename__ = "feedback"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    assessment_id = db.Column(db.Integer, db.ForeignKey('assessment.id'), nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
    tm_id = db.Column(db.Integer, db.ForeignKey('tm.id'), nullable=False)
    feedback = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.TIMESTAMP, default=datetime.utcnow, nullable=False)


class Discussion(db.Model):
    __tablename__ = "discussions"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    assessment_id = db.Column(db.Integer, db.ForeignKey('assessment.id'), nullable=False)
    user_type = db.Column(db.String(255), nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=True)
    tm_id = db.Column(db.Integer, db.ForeignKey('tm.id'), nullable=True)
    comment = db.Column(db.Text, nullable=False)
    posted_at = db.Column(db.TIMESTAMP, default=datetime.utcnow, nullable=False)


class Leaderboard(db.Model):
    __tablename__ = "leaderboard"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
    assessment_id = db.Column(db.Integer, db.ForeignKey('assessment.id'), nullable=False)
    total_score = db.Column(db.Integer, nullable=False)
    rank = db.Column(db.Integer, nullable=False)
    last_updated = db.Column(db.TIMESTAMP, default=datetime.utcnow, nullable=False)

class TokenBlocklist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    jti = db.Column(db.String(36), nullable=False, index=True)
    created_at = db.Column(db.DateTime, nullable=False)