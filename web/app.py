from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO
import threading

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/system_stats')
def system_stats():
    from src.system_monitor import get_system_stats
    return jsonify(get_system_stats())

@app.route('/api/start_evolution', methods=['POST'])
def start_evolution():
    data = request.json
    symbols = data.get('symbols', [])
    num_generations = data.get('generations', 10)
    population_size = data.get('population', 20)
    
    def run():
        from src.evolution import run_evolution
        run_evolution(symbols, num_generations, population_size)
    
    thread = threading.Thread(target=run, daemon=True)
    thread.start()
    
    return jsonify({'status': 'started'})

@app.route('/api/progress')
def progress():
    from src.evolution.progress_tracker import get_progress
    return jsonify(get_progress())

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=8050, debug=True, allow_unsafe_werkzeug=True)
