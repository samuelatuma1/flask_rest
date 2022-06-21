from functools import wraps
import jwt
from flask import jsonify, request

def check_for_token(func):
    global app
    @wraps(func)
    def wrapped(*args, **kwargs):
        auth = request.headers['authorization']
        if not auth:
            return jsonify({"message" : "Missing token"}), 403
        
        token = auth.split(' ')[1]
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
            setattr(request, 'token', token)
        except:
            return jsonify({"message": "Invalid token"}), 403
        return func(*args, **kwargs)
    return wrapped