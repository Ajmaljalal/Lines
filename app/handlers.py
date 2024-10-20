from cmath import e
import logging
from flask import jsonify, session, url_for, request
from authlib.integrations.flask_client import OAuth
import secrets

from app.agents.newsletter_agent import run_newsletter_creator

oauth = OAuth()

def init_oauth(app):
    oauth.init_app(app)
    oauth.register(
        name='google',
        client_id=app.config['GOOGLE_CLIENT_ID'],
        client_secret=app.config['GOOGLE_CLIENT_SECRET'],
        server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
        client_kwargs={'scope': 'openid email profile'},
    )
    app.logger.info(f"OAuth initialized with client_id: {app.config['GOOGLE_CLIENT_ID'][:10]}...")

def is_user_authenticated():
    return 'user' in session

def handle_google_signin():
    redirect_uri = url_for('main.google_signin', _external=True)
    nonce = secrets.token_urlsafe(16)
    session['oauth_nonce'] = nonce
    return oauth.google.authorize_redirect(redirect_uri, nonce=nonce)

def get_user_info():
    return session.get('user', {})

def chat():
    data = request.json
    user_input = data.get('user_input')
    thread_id = "default_thread_id"

    if not user_input:
        return {"error": "User input is required"}, 400

    try:
        result = run_newsletter_creator(user_input, thread_id)
        if not result:
            logging.warning("No messages returned from newsletter_creator_agent.")
            ai_response = "No response generated."
        else:
            ai_response = result[-1].content if hasattr(result[-1], 'content') else "No response generated."
        
        return {"response": [ai_response]}
    except Exception as e:
        return {"error": str(e)}, 500
