from wsgi import app
from endpoints import blueprint
from flask import request, jsonify
from simplepam import authenticate
from datetime import datetime, timedelta
import jwt


@blueprint.route('/api/auth', methods=['POST'])
def authentication_endpoint():
    user_data = request.get_json()
    if 'username' not in user_data or 'password' not in user_data:
        return jsonify({'detail': 'please provide "username" and "password" attributes to authenticate.'}), 400

    authentication_valid = authenticate(user_data['username'], user_data['password'])
    if authentication_valid is not True:
        return jsonify({'detail': 'credentials invalid.'}), 401

    now = datetime.utcnow()
    exp = now + timedelta(minutes=20)
    payload = {
        'username': user_data['username'],
        'iat': now,
        'exp': exp
    }
    access_token = jwt.encode(payload, app.config['SECRET_KEY'], 'HS256')

    return jsonify({'access_token': access_token.decode('utf8')})
