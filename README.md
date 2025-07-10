# 🔗 GitHub Webhook Receiver with Flask & MongoDB

This project is a **Flask-based GitHub webhook receiver** that listens to `push` and `pull_request` events from a GitHub repository, stores them in **MongoDB**, and displays them on a web UI.

---

## 📁 Project Structure

.
├── run.py # Entry point of the Flask application
├── app/
│ ├── init.py # Flask app setup & blueprint registration
│ ├── extensions.py # MongoDB connection initialization
│ ├── webhook/
│ │ ├── init.py # Makes 'webhook' a package
│ │ └── routes.py # Webhook & event display routes
│ └── templates/ # Frontend templates
│ ├── index.html
│ ├── style.css
│ └── script.js
├── .env # Environment variables (Mongo URI, secrets, etc.)
├── .gitignore # Files/folders to ignore in Git
├── README.md # You're here!
└── requirements.txt # Python dependencies

Copy
Edit

---

## ⚙️ Setup Instructions

### 1. Clone and Set Up Environment

```bash
git clone https://github.com/your-username/webhook-receiver.git
cd webhook-receiver
2. Create & Activate a Virtual Environment
bash
Copy
Edit
pip install virtualenv
virtualenv venv
source venv/bin/activate
3. Install Requirements
bash
Copy
Edit
pip install -r requirements.txt
4. Configure Environment Variables
Create a .env file in the root directory and add the following:

env
Copy
Edit
MONGO_URI="YOUR_MONGODB_CONNECTION_STRING"
DB_NAME="github_webhook_db"
COLLECTION_NAME="github_events"
GITHUB_WEBHOOK_SECRET="YOUR_GENERATED_SECRET_KEY"
🔐 You can generate a secret key using Python:

python
Copy
Edit
import secrets; secrets.token_hex(32)
🚀 Running the Application
bash
Copy
Edit
python run.py
App runs at: http://127.0.0.1:5000

Webhook endpoint: POST /webhook/receiver

✅ For production, use Gunicorn

🌍 Expose Flask to Internet (for GitHub Webhooks)
GitHub needs a public endpoint, use ngrok:

Install from https://ngrok.com/download

Start tunnel:

bash
Copy
Edit
ngrok http 5000
Copy the HTTPS URL generated (e.g., https://xxxx.ngrok-free.app)

🔧 GitHub Webhook Configuration
In your GitHub repo (action-repo):

Go to Settings > Webhooks > Add webhook

Payload URL: https://xxxx.ngrok-free.app/webhook/receiver

Content type: application/json

Secret: (match your .env key)

Events: Select:

✅ Pushes

✅ Pull requests

🧪 Testing
Push: Commit & push code to the repo.

Pull Request: Create/open/merge PR.

Events will:

Be logged in terminal

Stored in MongoDB

Shown on the UI (auto-refresh every 15s)

🛠️ Technologies Used
🐍 Python 3.8+

🌐 Flask

🍃 MongoDB (with pymongo)

📡 GitHub Webhooks

🧪 ngrok

🖥️ HTML + CSS + JavaScript

📌 Notes
Secure your webhook with a secret to avoid spoofed requests.

MongoDB Atlas users: whitelist your IP address and ensure user has readWrite access.

🤝 Contributions
Feel free to fork this repo, raise issues, or submit PRs to improve functionality or add support for more event types!

