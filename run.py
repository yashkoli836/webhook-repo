import os
from app import create_app
from dotenv import load_dotenv

load_dotenv()

app = create_app()

if __name__ == '__main__':
    # Run the Flask app. In a production environment, use a WSGI server like Gunicorn.
    app.run(debug=True, host='0.0.0.0', port=5000)