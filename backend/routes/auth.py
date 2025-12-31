from flask import Blueprint, request
from models import db, User, SccCodes
from werkzeug.security import generate_password_hash, check_password_hash

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    if request.method == 'POST':
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        full_name = data.get('full_name')
        dob = data.get('dob')
        scc = data.get('scc')

        #validate all inputs
        if not email or not password or not full_name or not dob or not scc:
            return {"message": "Missing required fields"}, 400

        scc_record = SccCodes.query.filter_by(scc=scc).first() #get scc from db

        #validate scc code
        if scc_record is None:
            return {"message": "Invalid scc code"} , 400
        if scc_record.usage is True:
            return {"message": "SCC code has already been used"} , 400

        #validate email
        existing_email = User.query.filter_by(email=email).first()
        if existing_email is not None:
            return {"message": "Email already registered"} , 400

        password_hash = generate_password_hash(password)

        #create the user
        user = User(email=email, password=password_hash, full_name=full_name, dob=dob,scc=scc)
        scc_record.usage = True
        scc_record.user_id = user.id
        db.session.add(user)
        db.session.commit()

        return {"message": "User registered"} , 201

    return None

@auth_bp.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')

        #check inputs exist
        if not email or not password:
            return {"message": "Missing required fields"}, 400

        #find the user
        find_user = User.query.filter_by(email=email).first()
        if find_user is None:
            return {"message": "Invalid email or password"}, 400

        #verify password and email
        if check_password_hash(find_user.password, password):
            return {"message": "Login successful"} , 200
        else:
            return {"message": "Invalid email or password"}, 400


    return None




























