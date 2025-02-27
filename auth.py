from functools import wraps
from flask import request, jsonify
import jwt
import os
from models import User
from app import app

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        
        if not token:
            return {'message': 'Token is missing'}, 401
        
        try:
            if token.startswith('Bearer '):
                token = token.split(' ')[1]
            data = jwt.decode(token, app.secret_key, algorithms=["HS256"])
            current_user = User.query.get(data['user_id'])
        except:
            return {'message': 'Token is invalid'}, 401
        
        return f(current_user, *args, **kwargs)
    
    return decorated
