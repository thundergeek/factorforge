import json
from pathlib import Path
from typing import Dict, Any

PROGRESS_FILE = Path('/app/data/evolution_progress.json')

def update_progress(current_gen: int, max_gen: int, current_agent: int, max_agent: int):
    """Update progress file for web UI"""
    data = {
        'current_generation': current_gen,
        'max_generations': max_gen,
        'current_agent': current_agent,
        'max_agents': max_agent
    }
    PROGRESS_FILE.parent.mkdir(parents=True, exist_ok=True)
    with PROGRESS_FILE.open('w') as f:
        json.dump(data, f)

def get_progress() -> Dict[str, Any]:
    """Read current progress"""
    if not PROGRESS_FILE.exists():
        return {'current_generation': 0, 'max_generations': 0, 'current_agent': 0, 'max_agents': 0}
    try:
        with PROGRESS_FILE.open('r') as f:
            return json.load(f)
    except:
        return {'current_generation': 0, 'max_generations': 0, 'current_agent': 0, 'max_agents': 0}

def clear_progress():
    """Clear progress file"""
    if PROGRESS_FILE.exists():
        PROGRESS_FILE.unlink()
