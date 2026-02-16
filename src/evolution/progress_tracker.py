import threading

_progress = {
    'current_generation': 0,
    'max_generations': 0,
    'current_agent': 0,
    'max_agents': 0,
    'status': 'idle',
    'best_fitness': 0.0,
    'active_agents': []
}
_lock = threading.Lock()

def update_progress(generation=None, agent=None, max_gen=None, max_agents=None, status=None, fitness=None):
    with _lock:
        if generation is not None:
            _progress['current_generation'] = generation
        if agent is not None:
            _progress['current_agent'] = agent
        if max_gen is not None:
            _progress['max_generations'] = max_gen
        if max_agents is not None:
            _progress['max_agents'] = max_agents
        if status is not None:
            _progress['status'] = status
        if fitness is not None:
            _progress['best_fitness'] = fitness

def add_active_agent(agent_id, fitness, status):
    with _lock:
        _progress['active_agents'].append({
            'id': agent_id,
            'fitness': fitness,
            'status': status
        })
        if len(_progress['active_agents']) > 10:
            _progress['active_agents'] = _progress['active_agents'][-10:]

def get_progress():
    with _lock:
        return _progress.copy()
