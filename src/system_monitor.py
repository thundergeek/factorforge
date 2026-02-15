import psutil
import subprocess
import json

def get_system_stats():
    """Get CPU, RAM, and GPU stats"""
    
    # CPU stats
    cpu_percent = psutil.cpu_percent(interval=0.5)
    cpu_count = psutil.cpu_count()
    cpu_freq = psutil.cpu_freq()
    
    # RAM stats
    ram = psutil.virtual_memory()
    
    # GPU stats - call host script
    gpu_stats = []
    
    try:
        result = subprocess.run(
            ['/app/get_gpu_stats.sh'],
            capture_output=True,
            text=True,
            timeout=3
        )
        
        if result.returncode == 0 and result.stdout.strip():
            gpu_data = json.loads(result.stdout.strip())
            for gpu in gpu_data:
                gpu['memory_percent'] = (gpu['memory_used'] / gpu['memory_total'] * 100) if gpu.get('memory_total', 0) > 0 else 0
                gpu['type'] = 'nvidia'
            gpu_stats = gpu_data
    except Exception as e:
        print(f"GPU detection error: {e}")
    
    return {
        'cpu': {
            'percent': cpu_percent,
            'count': cpu_count,
            'freq_current': cpu_freq.current if cpu_freq else 0,
            'freq_max': cpu_freq.max if cpu_freq else 0,
        },
        'ram': {
            'percent': ram.percent,
            'used_gb': ram.used / (1024**3),
            'total_gb': ram.total / (1024**3),
        },
        'gpu': gpu_stats,
    }
