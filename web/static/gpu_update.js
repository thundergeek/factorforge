let gpu0Gauge = null;
let gpu1Gauge = null;

function updateMultipleGPUs(gpuData) {
    if (!gpuData || gpuData.length === 0) return;
    
    // GPU 0
    if (gpuData[0]) {
        document.getElementById('gpu0Container').style.display = 'block';
        
        if (!gpu0Gauge) {
            gpu0Gauge = createGauge('gpu0Gauge', 'GPU0', '#ed8936');
        }
        
        const gpu0Percent = gpuData[0].utilization || gpuData[0].memory_percent || 0;
        updateGauge(gpu0Gauge, gpu0Percent);
        document.getElementById('gpu0Value').textContent = gpu0Percent.toFixed(1) + '%';
        
        let gpu0Text = gpuData[0].name.replace('GeForce ', '').substring(0, 15);
        if (gpuData[0].temperature) gpu0Text = gpuData[0].temperature + '°C · ' + gpu0Text;
        document.getElementById('gpu0Info').textContent = gpu0Text;
        
        if (gpu0Percent > 85) {
            gpu0Gauge.data.datasets[0].backgroundColor[0] = '#e53e3e';
        } else {
            gpu0Gauge.data.datasets[0].backgroundColor[0] = '#ed8936';
        }
    }
    
    // GPU 1
    if (gpuData[1]) {
        document.getElementById('gpu1Container').style.display = 'block';
        
        if (!gpu1Gauge) {
            gpu1Gauge = createGauge('gpu1Gauge', 'GPU1', '#9f7aea');
        }
        
        const gpu1Percent = gpuData[1].utilization || gpuData[1].memory_percent || 0;
        updateGauge(gpu1Gauge, gpu1Percent);
        document.getElementById('gpu1Value').textContent = gpu1Percent.toFixed(1) + '%';
        
        let gpu1Text = gpuData[1].name.replace('GeForce ', '').substring(0, 15);
        if (gpuData[1].temperature) gpu1Text = gpuData[1].temperature + '°C · ' + gpu1Text;
        document.getElementById('gpu1Info').textContent = gpu1Text;
        
        if (gpu1Percent > 85) {
            gpu1Gauge.data.datasets[0].backgroundColor[0] = '#e53e3e';
        } else {
            gpu1Gauge.data.datasets[0].backgroundColor[0] = '#9f7aea';
        }
    }
}
