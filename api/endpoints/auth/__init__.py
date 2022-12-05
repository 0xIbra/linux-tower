from wsgi import app
from endpoints import blueprint
from flask import request, jsonify
from simplepam import authenticate
import jwt


@blueprint.route('/api/auth', methods=['POST'])
def authentication_endpoint():
    user_data = request.get_json()
    if 'username' not in user_data or 'password' not in user_data:
        return jsonify({'detail': 'please provide "username" and "password" attributes to authenticate.'}), 400

    authentication_valid = authenticate(user_data['username'], user_data['password'])
    if authentication_valid is not True:
        return jsonify({'detail': 'credentials invalid.'}), 401

    access_token = jwt.encode({'username': user_data['username']}, app.config['SECRET_KEY'], 'HS256')

    return jsonify({'access_token': access_token.decode('utf8')})
