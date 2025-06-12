import psutil
import time

with open('usage_log.txt', 'w') as f:
    while True:
        cpu_usage = psutil.cpu_percent(interval=1)
        memory_info = psutil.virtual_memory()
        f.write(f'CPU Usage: {cpu_usage}%\n')
        f.write(f'Memory Usage: {memory_info.percent}%\n')
        time.sleep(5)
