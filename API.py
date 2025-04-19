import json
from flask import Flask, jsonify
import firebase_admin
from firebase_admin import credentials, firestore
from werkzeug.exceptions import BadRequest
import os
from dotenv import load_dotenv

app = Flask(__name__)

load_dotenv()

firebase_credentials = json.loads(os.environ['FIREBASE_CREDENTIALS'])
cred = credentials.Certificate(firebase_credentials)
firebase_admin.initialize_app(cred)
db = firestore.client()

@app.route('api/pregnancy/english/week/<int:week>', methods=['GET'])
def get_pregnancy_week_english(week):
    if week < 1 or week > 40:
        return jsonify({"error": "Invalid week. Please provide a week between 1 and 40."}), 400

    doc_ref = db.collection('pregnancy_weeks_english').document(f'week_{week}')
    doc = doc_ref.get()

    if doc.exists:
        data = doc.to_dict()
        return jsonify({
            "week": data.get("week"),
            "follow_up": data.get("follow_up"),
            "advice": data.get("advice")
        }), 200
    else:
        return jsonify({"error": "No data found for the specified week."}), 404

@app.errorhandler(404)
def page_not_found(e):
    return jsonify({"error": "Endpoint not found. Please check the URL and try again."}), 404

@app.errorhandler(BadRequest)
def handle_bad_request(e):
    return jsonify({"error": "Invalid input. Please provide a valid integer for the week."}), 400

@app.errorhandler(405)
def method_not_allowed(e):
    return jsonify({"error": "Method not allowed. Please use a GET request."}), 405

@app.errorhandler(500)
def internal_server_error(e):
    return jsonify({"error": "An unexpected error occurred. Please try again later."}), 500

if __name__ == '__main__':
    app.run(debug=True)