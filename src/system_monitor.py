import psutil
import subprocess
import torch

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
    
    if torch.cuda.is_available():
        for i in range(torch.cuda.device_count()):
            props = torch.cuda.get_device_properties(i)
            stats['gpus'].append({
                'id': i,
                'name': props.name,
                'memory_used_gb': round(torch.cuda.memory_allocated(i) / (1024**3), 1),
                'memory_total_gb': round(props.total_memory / (1024**3), 1),
                'utilization': 0
            })
    
    return stats
