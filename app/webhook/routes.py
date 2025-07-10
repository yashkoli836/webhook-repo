import json
import uuid
from datetime import datetime, timezone
from flask import Blueprint, request, jsonify, render_template, current_app
from ..extensions import mongo 
import hmac 
import hashlib 

webhook_bp = Blueprint('webhook_bp', __name__)

@webhook_bp.route('/')
def index():
    return render_template('index.html')

@webhook_bp.route('/webhook', methods=['POST'])
def github_webhook():
    
    secret = current_app.config.get('GITHUB_WEBHOOK_SECRET')
    
    if secret:
        signature = request.headers.get('X-Hub-Signature-256')
        if not signature:
            current_app.logger.warning("Webhook received without signature. Rejecting.")
            return jsonify({"status": "error", "message": "Signature missing"}), 403

        
        expected_signature = 'sha256=' + hmac.new(
            secret.encode('utf-8'),
            request.data, # Use request.data for the raw payload
            hashlib.sha256
        ).hexdigest()

        if not hmac.compare_digest(expected_signature, signature):
            current_app.logger.warning("Webhook signature mismatch. Rejecting.")
            return jsonify({"status": "error", "message": "Invalid signature"}), 403
        else:
            current_app.logger.info("Webhook signature verified successfully.")

    event_type = request.headers.get('X-GitHub-Event')
    payload = request.json 

    if not payload:
        current_app.logger.warning("Received empty payload.")
        return jsonify({"status": "error", "message": "No payload received"}), 400

    current_app.logger.info(f"Received GitHub event: {event_type}")

    data_to_store = {
        "request_id": str(uuid.uuid4()),
        "timestamp": datetime.now(timezone.utc).isoformat()
    }

    try:
        if event_type == 'push':
            author = payload['pusher']['name']
            to_branch = payload['ref'].split('/')[-1]
            action = "PUSH"
            data_to_store.update({
                "author": author,
                "action": action,
                "from_branch": None,
                "to_branch": to_branch
            })
            current_app.logger.info(f"Push event: {author} pushed to {to_branch}")

        elif event_type == 'pull_request':
            pr_action = payload['action']
            author = payload['pull_request']['user']['login']
            from_branch = payload['pull_request']['head']['ref']
            to_branch = payload['pull_request']['base']['ref']

            if pr_action == 'opened':
                action = "PULL_REQUEST"
                data_to_store.update({
                    "author": author,
                    "action": action,
                    "from_branch": from_branch,
                    "to_branch": to_branch
                })
                current_app.logger.info(f"Pull request opened: {author} from {from_branch} to {to_branch}")

            elif pr_action == 'closed' and payload['pull_request']['merged']:
                action = "MERGE"
                data_to_store.update({
                    "author": author,
                    "action": action,
                    "from_branch": from_branch,
                    "to_branch": to_branch
                })
                current_app.logger.info(f"Merge event: {author} merged {from_branch} to {to_branch}")

            else:
                current_app.logger.info(f"Ignoring pull_request action: {pr_action}")
                return jsonify({"status": "ignored", "message": f"Ignoring pull_request action: {pr_action}"}), 200

        else:
            current_app.logger.info(f"Ignoring unknown event type: {event_type}")
            return jsonify({"status": "ignored", "message": f"Ignoring event type: {event_type}"}), 200

        events_collection = mongo.db[current_app.config['COLLECTION_NAME']]
        events_collection.insert_one(data_to_store)
        current_app.logger.info("Data successfully stored in MongoDB.")
        return jsonify({"status": "success", "message": "Webhook received and processed"}), 200

    except KeyError as e:
        current_app.logger.error(f"Missing key in payload: {e}. Payload: {json.dumps(payload, indent=2)}")
        return jsonify({"status": "error", "message": f"Missing key in payload: {e}"}), 400
    except Exception as e:
        current_app.logger.error(f"An unexpected error occurred: {e}. Payload: {json.dumps(payload, indent=2)}")
        return jsonify({"status": "error", "message": f"An unexpected error occurred: {e}"}), 500

@webhook_bp.route('/events', methods=['GET'])
def get_events():
    """
    Fetches the latest GitHub events from MongoDB and returns them as JSON.
    """
    try:
        events_collection = mongo.db[current_app.config['COLLECTION_NAME']]
        events = list(events_collection.find().sort("timestamp", -1).limit(20))
        
        for event in events:
            event['_id'] = str(event['_id'])
        
        current_app.logger.info(f"Fetched {len(events)} events from MongoDB.")
        return jsonify(events), 200
    except Exception as e:
        current_app.logger.error(f"Error fetching events from MongoDB: {e}")
        return jsonify({"status": "error", "message": f"Error fetching events: {e}"}), 500

