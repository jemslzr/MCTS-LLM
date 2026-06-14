import json
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS

app = Flask(__name__, static_folder='.')
CORS(app)

# Load pre‑computed results
with open('results_cache.json', 'r', encoding='utf-8') as f:
    CACHE = json.load(f)
CACHE_MAP = {item['seed_id']: item for item in CACHE}

@app.route('/')
def index():
    return send_from_directory('.', 'spade.html')

@app.route('/<path:path>')
def static_files(path):
    return send_from_directory('.', path)

@app.route('/seeds')
def list_seeds():
    # Return only fields needed for the conversation list
    return jsonify([{
        "seed_id": item["seed_id"],
        "turn_1_context": item["turn_1_context"],
        "weight": item["weight"]
    } for item in CACHE])

@app.route('/evaluate', methods=['POST'])
def evaluate():
    data = request.get_json()
    seed_id = data.get('seed_id')
    cached = CACHE_MAP.get(seed_id)
    if not cached:
        return jsonify({'error': 'Seed not found'}), 404
    return jsonify({
        'success': cached['success'],
        'agent_response': cached['agent_response'],
        'seed_id': seed_id
    })

if __name__ == '__main__':
    app.run(port=5000, debug=False)