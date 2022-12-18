from functools import wraps
from flask import request, jsonify
from flask import current_app as app
import jwt


def is_authenticated(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        token = None
        if 'authorization' in request.headers:
            token = request.headers['authorization']

        if not token:
            return jsonify({'detail': 'access token not found in request headers[authorization].'}), 401

        try:
            jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
        except:
            return jsonify({'detail': 'access token is invalid.'}), 401

        return f(*args, **kwargs)

    return decorator


# def is_authenticated_with_user(f):
#     @wraps(f)
#     def decorator(*args, **kwargs):
#         token = None
#         if 'authorization' in request.headers:
#             token = request.headers['authorization']
#
#         if not token:
#             return jsonify({'message': 'access token not found in request headers[authorization].'})
#
#         try:
#             user = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
#         except:
#             return jsonify({'message': 'access token is invalid.'})
#
#         return f(user, *args, **kwargs)
#
#     return decorator
