import psutil
import subprocess

def get_system_stats():
    stats = {
        'cpu': {
            'utilization': psutil.cpu_percent(interval=0.1),
            'name': '',
            'short_name': ''
        },
        'ram': {
            'used_gb': round(psutil.virtual_memory().used / (1024**3), 1),
            'total_gb': round(psutil.virtual_memory().total / (1024**3), 1),
            'percent': psutil.virtual_memory().percent
        },
        'gpus': []
    }
    
    try:
        with open('/proc/cpuinfo', 'r') as f:
            for line in f:
                if 'model name' in line:
                    cpu_name = line.split(':')[1].strip()
                    stats['cpu']['name'] = cpu_name
                    stats['cpu']['short_name'] = cpu_name.replace(' @ ', ' ').split(' @ ')[0]
                    break
    except:
        stats['cpu']['name'] = 'Unknown CPU'
        stats['cpu']['short_name'] = 'Unknown CPU'
    
    try:
        result = subprocess.run(
            ['nvidia-smi', '--query-gpu=index,name,memory.used,memory.total,utilization.gpu', '--format=csv,noheader,nounits'],
            capture_output=True,
            text=True,
            timeout=2
        )
        if result.returncode == 0:
            for line in result.stdout.strip().split('\n'):
                if line:
                    parts = [p.strip() for p in line.split(',')]
                    if len(parts) == 5:
                        stats['gpus'].append({
                            'id': int(parts[0]),
                            'name': parts[1],
                            'memory_used_gb': round(float(parts[2]) / 1024, 1),
                            'memory_total_gb': round(float(parts[3]) / 1024, 1),
                            'utilization': int(parts[4])
                        })
    except:
        pass
    
    return stats
