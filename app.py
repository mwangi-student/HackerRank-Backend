from flask import Flask, jsonify
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_cors import CORS

from models import db, TokenBlocklist
from views.student import student_bp
from views.tm import tm_bp
from views.leaderboard import leaderboard_bp
from views.discussions import discussion_bp
from views.auth import auth_bp
from views.assessment_invite import assessment_invite_bp
from views.codeChallenge import code_challenge_bp
from views.assessment import assessment_bp
from views.questions import questions_bp
from views.AssessmenySubmission import submission_bp
from views.feedback import feedback_bp
from views.scores import score_bp

mail = Mail()
jwt = JWTManager()

def create_app():
    app = Flask(__name__)

    # Enable CORS for frontend connection
    CORS(app, supports_credentials=True, origins=["http://localhost:5173"], allow_headers=["Authorization", "Content-Type"])

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hackerrank.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    app.config["JWT_SECRET_KEY"] = "htgdfcenkudbgdtevdjugsmkkksjugst"
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)

    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 465
    app.config['MAIL_USE_TLS'] = False
    app.config['MAIL_USE_SSL'] = True
    app.config['MAIL_USERNAME'] = 'mwangi.brian@student.moringaschool.com'
    app.config['MAIL_PASSWORD'] = 'kqsq xrws pkwz dpyb'
    app.config['MAIL_DEFAULT_SENDER'] = 'mwangi.brian@student.moringaschool.com'

    # Initialize extensions
    db.init_app(app)
    migrate = Migrate(app, db)
    jwt.init_app(app)
    mail.init_app(app)

    # Register blueprints
    blueprints = [
        student_bp, tm_bp, leaderboard_bp, discussion_bp, auth_bp, score_bp,
        assessment_invite_bp, assessment_bp, questions_bp, submission_bp, feedback_bp, code_challenge_bp
    ]
    for bp in blueprints:
        app.register_blueprint(bp)

    # Define a simple route
    @app.route("/", methods=["GET"])
    def get_data():
        return jsonify({"message": "Flask is working!"})

    # Blocklist JWT check
    @jwt.token_in_blocklist_loader
    def check_if_token_revoked(jwt_header, jwt_payload: dict) -> bool:
        jti = jwt_payload["jti"]
        token_exists = db.session.query(TokenBlocklist.id).filter_by(jti=jti).scalar()
        return token_exists is not None

    return app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
