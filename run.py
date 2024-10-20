from dotenv import load_dotenv
from app import create_app

load_dotenv()  # This loads the environment variables from .env

try:
    app = create_app()
except Exception as e:
    print(f"Error creating app: {e}")
    raise

if __name__ == '__main__':
    app.run(debug=True)
