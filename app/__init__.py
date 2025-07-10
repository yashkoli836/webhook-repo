import os
from flask import Flask
from .extensions import mongo

def create_app():
    """
    Creates and configures the Flask application.
    """
    app = Flask(__name__)

    # MongoDB Configuration
    app.config["MONGO_URI"] = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
    app.config["DB_NAME"] = os.getenv("DB_NAME", "github_webhook_db")
    app.config["COLLECTION_NAME"] = os.getenv("COLLECTION_NAME", "github_events")
    
    # GitHub Webhook Secret
    app.config["GITHUB_WEBHOOK_SECRET"] = os.getenv("GITHUB_WEBHOOK_SECRET")

    mongo.init_app(app)

    from .webhook.routes import webhook_bp
    app.register_blueprint(webhook_bp)

    print(f"Flask app created. Connected to MongoDB: {app.config['MONGO_URI']}, Database: {app.config['DB_NAME']}, Collection: {app.config['COLLECTION_NAME']}")
    if app.config["GITHUB_WEBHOOK_SECRET"]:
        print("GitHub Webhook Secret is configured.")
    else:
        print("WARNING: GitHub Webhook Secret is NOT configured. Webhooks will not be verified.")

    return app

