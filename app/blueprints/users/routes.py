from flask import request, jsonify, Flask
from app.blueprints.users import users_bp
from .schemas import user_schema,login_schema
from marshmallow import ValidationError
from app.models import Users, db, OAuth
from sqlalchemy import select
from app.extensions import limiter
from app.utils.util import encode_token #token_required, token
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token

# Login user
@users_bp.route("/login", methods=['POST'])
def login():
    #verify if the request from the frontend contains a Oauth token

    info = request.get_json()

    google_login = info.get('google_login')

    #Validate the payload and ensure they sent us email and password
    try:
        creds = login_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    query = select(Users).where(Users.email == creds['email'])
    user = db.session.execute(query).scalars().first()

    if google_login:
        google = oauth.create_client('google')
        try:
            token = google.authorize_access_token()
            user_info = google.parse_id_token(token)

            email = user_info['email']
            name = user_info['name']

            user = Users.query.filter_by(email=email).first()

            #if user exist 
            if user:
                access_token = create_access_token(identity=email)
                return jsonify({'access_token': access_token, 'user_info': {'email': email, 'name': name}}), 200
            else:
                new_google_user = Users(email=email, name=name, password=None)
                db.session.add(new_google_user)
                db.session.commit()

                access_token = create_access_token(identity=email)

                return jsonify({
                    'message': "token generated successfully",
                    'access_token': access_token,
                    'user_info': {'email': email, 'name': name}}), 201

        except Exception as e:
            return jsonify({"message": "Invalid Google Token"}), 400


    else:

        if user and check_password_hash(user.password, creds['password']): #If a user exist within the database, with the same email password combination

            token = encode_token(user.id)

            response = {
                "message": "successfully logged in",
                "status": "success",
                "token": token
            }
        
            return jsonify(response), 200
        
        else:
            return jsonify({"message": "Invalid email or password!"}), 400
    






#register/signup new users 
@users_bp.route("/signup", methods=['POST'])
# @limiter.limit("3 per hour")
def create_user():
    #Validate and Deserialize incoming data
    try:
        user_data = user_schema.load(request.json)
    #If data invalid respond with error message
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    query = select(Users).where(Users.email == user_data['email'])
    existing = db.session.execute(query).scalars().first()
    if existing:
        return jsonify({"message": "Account already associated with that email."}), 400
    
    #If data is valid, create new user with that data
    pwhash = generate_password_hash(user_data['password'])
    new_user = Users(name=user_data['name'], email=user_data['email'], phone=user_data['phone'], password=pwhash, dob=user_data['dob']) ## take out and DOB
    db.session.add(new_user) #Add to session
    db.session.commit() #commit session to db

    return user_schema.jsonify(new_user), 201 #return new user object as a response