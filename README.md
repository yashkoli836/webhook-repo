Dev Assessment - Webhook Receiver
Please use this repository for constructing the Flask webhook receiver.

Setup
Create a new virtual environment

pip install virtualenv

Create the virtual env

virtualenv venv

Install requirements

pip install -r requirements.txt

Run the flask application (In production, please use Gunicorn)

python run.py

The endpoint is at:

POST [http://127.0.0.1:5000/webhook/receiver](http://127.0.0.1:5000/webhook/receiver)

You need to use this as the base and setup the flask app. Integrate this with MongoDB (commented at app/extensions.py)

Project Structure
.
├── run.py                  # Main entry point for the Flask application (formerly app.py)
├── app/
│   ├── __init__.py         # Initializes the Flask app and registers blueprints
│   ├── extensions.py       # Handles MongoDB client initialization
│   ├── webhook/            # Contains webhook-related routes and logic
│   │   ├── __init__.py     # Makes 'webhook' a Python package
│   │   └── routes.py       # Defines the webhook and event display routes
│   └── templates/          # All frontend files (HTML, CSS, JS) are here
│       ├── index.html      # Main HTML content
│       ├── style.css       # Stylesheet for the frontend
│       └── script.js       # JavaScript for frontend logic and API calls
├── .env                    # Environment variables (e.g., MongoDB URI, Webhook Secret)
├── .gitignore              # Specifies intentionally untracked files to ignore
├── README.md               # This file
└── requirements.txt        # Python dependencies

Configuration and Usage (for your reference)
This section provides additional details for setting up your .env and configuring GitHub webhooks, which are essential for the application to function.

Configure Environment Variables
Create a file named .env in the root directory of your webhook-repo and add the following content. Make sure to replace the placeholder values with your actual details.

MONGO_URI="YOUR_MONGODB_CONNECTION_STRING"
DB_NAME="github_webhook_db"
COLLECTION_NAME="github_events"
GITHUB_WEBHOOK_SECRET="YOUR_GENERATED_SECRET_KEY" # Optional but Recommended for security

MONGO_URI: Replace "YOUR_MONGODB_CONNECTION_STRING" with the connection string for your MongoDB database (e.g., from MongoDB Atlas). Ensure your MongoDB user has readWrite access and your IP address is whitelisted in MongoDB Atlas.

DB_NAME: The name of the database where events will be stored (default is github_webhook_db).

COLLECTION_NAME: The name of the collection within the database (default is github_events).

GITHUB_WEBHOOK_SECRET:

Optional but highly recommended for security.

Generate a strong, random string (e.g., using secrets.token_hex(32) in Python).

If you choose not to use a secret, you can leave this line empty (GITHUB_WEBHOOK_SECRET="") or remove it. However, this means your webhook endpoint will be accessible to anyone.

Expose Your Local Server to the Internet (for GitHub Webhooks)
GitHub needs to send webhooks to a publicly accessible URL. For local development, ngrok is a convenient tool for this.

Install ngrok: If you haven't already, download and install ngrok from ngrok.com/download.

Run ngrok: In a new terminal window (while your Flask app is still running), execute:

ngrok http 5000
```ngrok` will provide you with a public HTTPS forwarding URL (e.g., `https://xxxx-xxxx-xxxx-xxxx.ngrok-free.app`). **Copy this URL.** Note that `ngrok-free` tunnels often generate a new URL each time they start.


GitHub Webhook Configuration (action-repo)
Configure the webhook in your GitHub repository (action-repo) to send events to your running Flask application.

Go to your action-repo on GitHub.

Navigate to Settings > Webhooks.

Click the Add webhook button (or edit your existing one).

Payload URL: Paste the ngrok HTTPS forwarding URL you copied, followed by /webhook/receiver.

Example: https://xxxx-xxxx-xxxx-xxxx.ngrok-free.app/webhook/receiver

Content type: Select application/json.

Secret:

If you set GITHUB_WEBHOOK_SECRET in your .env file, paste the exact same secret key here.

If you chose not to use a secret, leave this field empty.

Which events would you like to trigger this webhook?:

Select "Let me select individual events."

Check the boxes for Pushes and Pull requests. (The "Merge" action is covered by the pull_request event when it's closed and merged).

Ensure Active is checked.

Click Add webhook (or Update webhook).

Testing and Usage
Once both the Flask application and the GitHub webhook are configured and running:

Push Action: Make a commit and push to any branch in your action-repo.

Pull Request Action: Create and open a pull request in your action-repo.

Merge Action: Merge a pull request in your action-repo.

You will observe the following:

Events will be logged in your Flask application's terminal.

The data will be stored in your MongoDB database.

The events will automatically appear on your web UI (http://127.0.0.1:5000/) within 15 seconds (due to the polling mechanism).