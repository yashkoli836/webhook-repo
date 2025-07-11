# 🔗 GitHub Webhook Receiver with Flask & MongoDB

This project is a **Flask-based GitHub webhook receiver** that listens to `push` and `pull_request` events from a GitHub repository, stores them in **MongoDB**, and displays them on a web UI.

---

## 🎥 Video Demo

📺 [Click to Watch Demo](https://drive.google.com/file/d/1rl3IAEm-cBr30y5aQ1jnfrU42fAMRsz6/view?usp=sharing)

---

## 📁 Project Structure

```
.
├── run.py                  # Entry point of the Flask application
├── app/
│   ├── __init__.py         # Flask app setup & blueprint registration
│   ├── extensions.py       # MongoDB connection initialization
│   ├── webhook/
│   │   ├── __init__.py     # Makes 'webhook' a package
│   │   └── routes.py       # Webhook & event display routes
│   └── templates/          # Frontend templates
│       └── index.html
├── .env                    # Environment variables (Mongo URI, secrets, etc.)
├── .gitignore              # Files/folders to ignore in Git
├── Dockerfile              # Builds the Flask app image
├── docker-compose.yml      # Defines Flask + MongoDB services
├── requirements.txt        # Python dependencies
└── README.md               # You're here!
```

---

## ⚙️ Environment Setup

Create a `.env` file in the root directory:

```env
MONGO_URI=mongodb://mongo:27017/
DB_NAME=github_webhook_db
COLLECTION_NAME=github_events
GITHUB_WEBHOOK_SECRET=your_secret_key_here
```

> 🔐 This file is ignored by Git and not copied into the Docker image.

Generate a secret key using Python:
```python
import secrets; secrets.token_hex(32)
```

---

## 🚀 Run with Docker (One Command)

```bash
docker-compose up --build
```

- App will be live at: [http://localhost:5000](http://localhost:5000)
- Webhook endpoint: `POST /webhook`
- MongoDB is available internally at `mongo:27017`

To stop the app:
```bash
docker-compose down
```

---

## 🔧 GitHub Webhook Configuration

In your GitHub repo:

- Go to **Settings > Webhooks > Add webhook**
- **Payload URL**: `http://<your-public-url>/webhook`
- **Content type**: `application/json`
- **Secret**: same as `GITHUB_WEBHOOK_SECRET`
- **Events**: Enable:
  - ✅ Push
  - ✅ Pull Requests

If you're testing locally, use **ngrok** to expose your port:

```bash
ngrok http 5000
```

Then update the Payload URL to `https://<ngrok-domain>.ngrok-free.app/webhook`.

---

## 🧪 Testing

- Push commits or open PRs in the connected repo
- Events are:
  - Stored in MongoDB
  - Printed in terminal logs
  - Shown in the UI (auto-refreshes every 15s)

---

## 🛠️ Technologies Used

- 🐍 Python 3.8+
- 🌐 Flask
- 🍃 MongoDB (with `pymongo`)
- 📡 GitHub Webhooks
- 🧪 ngrok
- 🖥️ HTML + CSS + JavaScript
- 🐳 Docker + Docker Compose

---

## 📌 Notes

- Webhook secrets ensure GitHub authenticity
- MongoDB Atlas users must whitelist IP & enable `readWrite` access
- Use `Gunicorn` + `nginx` in production

---

## 🤝 Contributions

Feel free to fork this repo, raise issues, or submit PRs to improve functionality or extend webhook support!

---

## 📝 License

MIT License © [Yash Mahor](https://github.com/yashkoli836)
