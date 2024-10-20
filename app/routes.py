from flask import Blueprint, render_template, redirect, url_for, session, current_app, request, jsonify
from .handlers import is_user_authenticated, handle_google_signin, oauth, get_user_info, chat

main = Blueprint('main', __name__)

@main.route('/')
def index():
    if is_user_authenticated():
        return render_template('index.html')
    return redirect(url_for('main.signin'))

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
def get_user_info():
    return jsonify(get_user_info())


@main.route('/chat', methods=['POST'])
def chat_route():
    return jsonify(chat())
