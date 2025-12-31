from flask import Flask
from flask_cors import CORS
import os
from dotenv import load_dotenv
from models import db
from routes.auth import auth_bp
from routes.voter import voter_bp
from routes.api import api_bp

load_dotenv()

app = Flask(__name__)
print("Flask app created")

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')

db.init_app(app)
print("DB initialized")

CORS(app)
print("CORS enabled")

app.register_blueprint(auth_bp)
print("Blueprint registered")

app.register_blueprint(voter_bp)
print('voter blueprint registered')

app.register_blueprint(api_bp)
print('api ready')

with app.app_context():
    db.create_all()
print("Tables created")

@app.route('/')
def index():
    return {'message': 'Hello, World!'}

if __name__ == '__main__':
    print("Starting Flask server...")
    app.run(debug=True, port=8000, host='0.0.0.0')