import os
from flask import Flask, jsonify
from flask_cors import CORS
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv

from models.db import db
from models.user import User
from models.task import Task
from models.habit import Habit
from models.habit_progress import HabitProgress

from routes.auth import auth_bp
from routes.tasks import tasks_bp
from routes.habits import habits_bp
from routes.habit_progress import habit_progress_bp
from routes.nlp import nlp_bp

# Load environment variables
load_dotenv()

# Initialize Flask application
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('JWT_SECRET', 'dev-secret-key')
app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET', 'dev-secret-key')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = int(os.environ.get('JWT_EXPIRE', 2592000))  # 30 days default

# Configure database
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://{}:{}@{}:{}/{}'.format(
    os.environ.get('DB_USER', 'root'),
    os.environ.get('DB_PASSWORD', 'password'),
    os.environ.get('DB_HOST', 'localhost'),
    os.environ.get('DB_PORT', '3306'),
    os.environ.get('DB_NAME', 'prodigyai')
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize extensions
db.init_app(app)
jwt = JWTManager(app)
migrate = Migrate(app, db)
CORS(app)

# Register blueprints
app.register_blueprint(auth_bp, url_prefix='/api/auth')
app.register_blueprint(tasks_bp, url_prefix='/api/tasks')
app.register_blueprint(habits_bp, url_prefix='/api/habits')
app.register_blueprint(habit_progress_bp, url_prefix='/api/habit-progress')
app.register_blueprint(nlp_bp, url_prefix='/api/nlp')

# Health check endpoint
@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({
        'status': 'healthy',
        'name': 'ProdigyAI Flask Backend',
        'version': '1.0.0'
    })

# Error handlers
@app.errorhandler(404)
def not_found(e):
    return jsonify({"error": "Not found"}), 404

@app.errorhandler(500)
def server_error(e):
    return jsonify({"error": "Internal server error"}), 500

# Initialize database tables
@app.before_first_request
def create_tables():
    db.create_all()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=os.environ.get('FLASK_DEBUG', 'True') == 'True') 