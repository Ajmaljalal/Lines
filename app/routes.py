from flask import Blueprint, render_template, redirect, url_for, session, current_app, request, jsonify
from functools import wraps
from .handlers import is_user_authenticated, handle_google_signin, oauth, get_user_info_handler, chat

main = Blueprint('main', __name__)

def handle_403_error(e):
    return jsonify(error="Unauthorized access"), 403

def auth_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not is_user_authenticated():
            current_app.logger.warning("Unauthorized access attempt")
            return redirect(url_for('main.signin'))
        return f(*args, **kwargs)
    return decorated_function

@main.route('/')
@auth_required
def index():
    return render_template('index.html')

@main.route('/signin')
def signin():
    return render_template('signin.html')

@main.route('/google-signin')
def google_signin():
    current_app.logger.info(f"Google Sign-In route accessed")
    current_app.logger.info(f"Request args: {request.args}")
    if 'code' not in request.args:
        return handle_google_signin()
    
    try:
        token = oauth.google.authorize_access_token()
        # Extract the ID token from the response
        id_token = token.get('id_token')
        if id_token:
            # Parse the ID token without providing a nonce
            user_info = oauth.google.parse_id_token(token, nonce=None)
            session['user'] = user_info
            return redirect(url_for('main.index'))
        else:
            current_app.logger.error("No ID token found in the response")
            return "Authentication failed: No ID token", 400
    except Exception as e:
        current_app.logger.error(f"Error in Google Sign-In: {str(e)}", exc_info=True)
        return f"An error occurred: {str(e)}", 400

@main.route('/signout')
def signout():
    session.pop('user', None)
    return redirect(url_for('main.signin'))

@main.route('/get-user-info')
@auth_required
def get_user_info():
    return jsonify(get_user_info_handler())

@main.route('/chat', methods=['POST'])
@auth_required
def chat_route():
    return jsonify(chat())
