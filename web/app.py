from flask import Flask, render_template, jsonify, request
from flask_socketio import SocketIO, emit
import subprocess
import json
import pandas as pd
from pathlib import Path
from src.evolution.progress_tracker import get_progress
import threading
import time
import sys
import io

app = Flask(__name__)
app.config['SECRET_KEY'] = 'alpha-mining-secret'
socketio = SocketIO(app, cors_allowed_origins="*")

# Global state
current_run = {
    "running": False,
    "process": None,
    "config": {}
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/status')
def status():
    """Get current system status"""
    results_path = Path('/app/data/results/factor_results.csv')
    progress = get_progress()
    
    status_data = {
        "running": current_run["running"],
        "config": current_run.get("config", {}),
        "has_results": results_path.exists(),
        "total_factors": 0,
        "good_factors": 0,
        "best_ic": 0.0
        ,"current_generation": progress.get("current_generation", 0),
        "max_generations": progress.get("max_generations", 10)
    }
    
    if results_path.exists():
        try:
            df = pd.read_csv(results_path)
            if not df.empty:
                status_data["total_factors"] = len(df)
                status_data["good_factors"] = len(df[df['ic'] > 0.05])
                status_data["best_ic"] = float(df['ic'].max())
        except Exception as e:
            print(f"Error reading results: {e}", file=sys.stderr)
    
    return jsonify(status_data)

@app.route('/api/system')
def system_stats():
    """Get CPU/RAM/GPU stats"""
    try:
        from src.system_monitor import get_system_stats
        stats = get_system_stats()
        return jsonify(stats)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/results')
def results():
    """Get factor results"""
    results_path = Path('/app/data/results/factor_results.csv')
    
    if not results_path.exists():
        return jsonify({"error": "No results yet", "factors": []}), 200
    
    try:
        df = pd.read_csv(results_path)
        if df.empty:
            return jsonify({"total": 0, "good": 0, "factors": []}), 200
            
        df = df.sort_values('ic', ascending=False)
        
        # Convert to dict with None handling
        factors_list = []
        for _, row in df.head(20).iterrows():
            factor_dict = {
                "dsl": row.get('dsl', 'N/A'),
                "hypothesis": row.get('hypothesis', ''),
                "ic": float(row.get('ic', 0)) if pd.notna(row.get('ic')) else 0.0,
                "sharpe": float(row.get('sharpe', 0)) if pd.notna(row.get('sharpe')) else 0.0,
                "arr": float(row.get('arr', 0)) if pd.notna(row.get('arr')) else 0.0,
                "mdd": float(row.get('mdd', 0)) if pd.notna(row.get('mdd')) else 0.0
            }
            factors_list.append(factor_dict)
        
        results_data = {
            "total": len(df),
            "good": len(df[df['ic'] > 0.05]),
            "factors": factors_list
        }
        
        return jsonify(results_data)
    except Exception as e:
        print(f"Error in /api/results: {e}", file=sys.stderr)
        return jsonify({"error": str(e), "factors": []}), 500

@app.route('/api/start', methods=['POST'])
def start_evolution():
    """Start evolution run"""
    if current_run["running"]:
        return jsonify({"error": "Already running"}), 400
    
    config = request.json or {}
    generations = config.get('generations', 5)
    agents = config.get('agents', 3)
    symbols = config.get('symbols', 'AAPL,MSFT,GOOGL,AMZN,NVDA,TSLA,META')
    
    current_run["config"] = config
    current_run["running"] = True
    
    socketio.emit('status_change', {'running': True})
    socketio.emit('log', {'message': f'🚀 Starting evolution: {generations} generations × {agents} agents', 'type': 'success'})
    socketio.emit('log', {'message': f'📊 Analyzing {len(symbols.split(","))} stocks', 'type': 'info'})
    
    # Run in background thread with stdout capture
    def run_evolution():
        import os
        os.environ['MAX_GENERATIONS'] = str(generations)
        os.environ['AGENTS_PER_GENERATION'] = str(agents)
        os.environ['UNIVERSE_SYMBOLS'] = symbols
        
        # Capture stdout to send to web UI
        old_stdout = sys.stdout
        
        class LogCapture(io.TextIOBase):
            def write(self, text):
                if text.strip():
                    # Determine log type from emoji
                    log_type = 'info'
                    if '✅' in text or '🌟' in text or '🏆' in text or '🎉' in text:
                        log_type = 'success'
                    elif '❌' in text:
                        log_type = 'error'
                    elif '⚠️' in text:
                        log_type = 'warning'
                    elif '🔄' in text or '🤖' in text:
                        log_type = 'progress'
                    
                    socketio.emit('log', {'message': text.strip(), 'type': log_type})
                old_stdout.write(text)
                return len(text)
        
        sys.stdout = LogCapture()
        
        try:
            from src.evolution import run_evolution
            run_evolution()
        except Exception as e:
            socketio.emit('log', {'message': f'❌ FATAL ERROR: {str(e)}', 'type': 'error'})
            print(f"Evolution error: {e}", file=sys.stderr)
        finally:
            sys.stdout = old_stdout
            current_run["running"] = False
            socketio.emit('status_change', {'running': False})
    
    thread = threading.Thread(target=run_evolution)
    thread.daemon = True
    thread.start()
    
    return jsonify({"message": "Evolution started"})

@app.route('/api/stop', methods=['POST'])
def stop_evolution():
    """Stop evolution run"""
    current_run["running"] = False
    socketio.emit('log', {'message': '⏸️ Stopping (may take a moment)...', 'type': 'warning'})
    return jsonify({"message": "Stopping (may take a moment)"})

if __name__ == '__main__':
    print("🚀 Starting Alpha Mining Dashboard on http://0.0.0.0:8050")
    socketio.run(app, host='0.0.0.0', port=8050, allow_unsafe_werkzeug=True)
