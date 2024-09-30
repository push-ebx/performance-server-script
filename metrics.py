import json
import psutil
import time
from datetime import datetime
from speedtest import Speedtest

INTERVAL = 1
net_io_start = psutil.net_io_counters()
time.sleep(INTERVAL)
net_io_end = psutil.net_io_counters()

rx_bytes_per_sec = (net_io_end.bytes_recv - net_io_start.bytes_recv) / INTERVAL
tx_bytes_per_sec = (net_io_end.bytes_sent - net_io_start.bytes_sent) / INTERVAL

rx_kb_per_sec = round(rx_bytes_per_sec / 1024, 2)
tx_kb_per_sec = round(tx_bytes_per_sec / 1024, 2)

speed_test = Speedtest()
speed_test.get_best_server()
download_speed = round(speed_test.download() / (1024 * 1024), 2)
upload_speed = round(speed_test.upload() / (1024 * 1024), 2)

metrics = {
    "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
    "cpu_usage": psutil.cpu_percent(interval=1),
    "memory_usage": psutil.virtual_memory().percent,
    "network": {
        "rx_kb_per_sec": rx_kb_per_sec,
        "tx_kb_per_sec": tx_kb_per_sec
    },
    "internet_speed": {
        "download_mbps": download_speed,
        "upload_mbps": upload_speed
    }
}

try:
    with open('metrics.json', 'r') as f:
        data = json.load(f)
except FileNotFoundError:
    data = []

data.append(metrics)
data = data[-24:]

with open('metrics.json', 'w') as f:
    json.dump(data, f, indent=4)

