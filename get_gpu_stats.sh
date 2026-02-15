#!/bin/bash
nvidia-smi --query-gpu=index,name,utilization.gpu,memory.used,memory.total,temperature.gpu --format=csv,noheader,nounits 2>/dev/null | python3 -c "
import sys, json
result = []
for line in sys.stdin:
    parts = [p.strip() for p in line.split(',')]
    if len(parts) >= 6:
        result.append({
            'index': int(parts[0]),
            'name': parts[1],
            'utilization': float(parts[2]),
            'memory_used': float(parts[3]),
            'memory_total': float(parts[4]),
            'temperature': float(parts[5])
        })
print(json.dumps(result))
"
