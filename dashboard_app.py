from flask import Flask, render_template, jsonify, send_from_directory, send_file
import os
import json
from datetime import datetime

app = Flask(__name__)
DATA_DIR = os.path.join(os.path.dirname(__file__), 'dashboard_data')

def ensure_data_dir():
    """Ensure dashboard data directory exists"""
    os.makedirs(DATA_DIR, exist_ok=True)

def get_file_timestamp(filepath):
    """Get the last modified timestamp of a file"""
    try:
        return os.path.getmtime(filepath)
    except:
        return 0

@app.route('/')
def dashboard():
    ensure_data_dir()
    return render_template('dashboard.html')

@app.route('/api/summary')
def api_summary():
    try:
        filepath = os.path.join(DATA_DIR, 'summary.json')
        with open(filepath) as f:
            data = json.load(f)
        data['last_updated'] = datetime.fromtimestamp(get_file_timestamp(filepath)).strftime('%Y-%m-%d %H:%M:%S')
        return jsonify(data)
    except FileNotFoundError:
        return jsonify({
            'total_speed_violations': 0,
            'total_helmet_violations': 0,
            'speed_violations_per_lane': {},
            'helmet_violations_per_lane': {},
            'last_updated': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        })

@app.route('/api/speed_violations')
def api_speed_violations():
    try:
        filepath = os.path.join(DATA_DIR, 'speed_violations.json')
        with open(filepath) as f:
            data = json.load(f)
        return jsonify(data)
    except FileNotFoundError:
        return jsonify([])

@app.route('/api/helmet_violations')
def api_helmet_violations():
    try:
        filepath = os.path.join(DATA_DIR, 'helmet_violations.json')
        with open(filepath) as f:
            data = json.load(f)
        return jsonify(data)
    except FileNotFoundError:
        return jsonify([])

@app.route('/violations_graph.png')
def graph_image():
    try:
        path = os.path.join(os.path.dirname(__file__), 'dashboard_data', 'violations_graph.png')
        if not os.path.exists(path):
            return "Graph not available", 404
        return send_file(path, mimetype='image/png', cache_timeout=0)
    except Exception as e:
        print(f"Error serving graph: {e}")
        return "Graph not available", 500

@app.route('/safety')
def safety():
    try:
        with open(os.path.join(os.path.dirname(__file__), 'safety', 'safety', 'police.json'), 'r') as f:
            police_stations = json.load(f)
    except FileNotFoundError:
        police_stations = []
    return render_template('safety.html', police_stations=police_stations)

if __name__ == '__main__':
    ensure_data_dir()
    app.run(debug=True, port=5000) 