import psutil
import subprocess
import json

def get_system_stats():
    """Get CPU, RAM, and GPU stats with proper names"""
    
    # CPU info
    cpu_name = "CPU"
    try:
        # Try to get CPU model name
        with open('/proc/cpuinfo', 'r') as f:
            for line in f:
                if 'model name' in line:
                    cpu_name = line.split(':')[1].strip()
                    # Simplify name (remove extra spaces/details)
                    cpu_name = ' '.join(cpu_name.split())
                    break
    except:
        pass
    
    cpu_percent = psutil.cpu_percent(interval=1)
    
    # RAM info
    ram = psutil.virtual_memory()
    ram_used_gb = ram.used / (1024**3)
    ram_total_gb = ram.total / (1024**3)
    ram_percent = ram.percent
    
    # GPU info
    gpus = []
    try:
        result = subprocess.run(
            ['nvidia-smi', '--query-gpu=index,name,utilization.gpu,memory.used,memory.total', 
             '--format=csv,noheader,nounits'],
            capture_output=True, text=True, timeout=5
        )
        
        if result.returncode == 0:
            for line in result.stdout.strip().split('\n'):
                if line:
                    parts = [p.strip() for p in line.split(',')]
                    gpu_index = parts[0]
                    gpu_name = parts[1]
                    gpu_util = float(parts[2])
                    vram_used = float(parts[3]) / 1024  # Convert to GB
                    vram_total = float(parts[4]) / 1024
                    
                    # Simplify GPU name (e.g., "NVIDIA GeForce GTX 1070 Ti" -> "GTX 1070 Ti")
                    short_name = gpu_name.replace('NVIDIA GeForce', '').replace('NVIDIA', '').strip()
                    
                    gpus.append({
                        'index': int(gpu_index),
                        'name': gpu_name,
                        'short_name': short_name,
                        'utilization': gpu_util,
                        'vram_used': vram_used,
                        'vram_total': vram_total
                    })
    except:
        pass
    
    return {
        'cpu': {
            'name': cpu_name,
            'short_name': cpu_name.split('@')[0].strip() if '@' in cpu_name else cpu_name,
            'utilization': cpu_percent
        },
        'ram': {
            'used_gb': round(ram_used_gb, 1),
            'total_gb': round(ram_total_gb, 1),
            'percent': ram_percent
        },
        'gpus': gpus
    }
