import psutil
from apscheduler.schedulers.background import BackgroundScheduler

cpu_usage_history = []
scheduler = BackgroundScheduler()

# Function to get CPU usage
def get_cpu_usage():
    return psutil.cpu_percent(interval=1)

# Background job to update CPU usage
def update_cpu_usage():
    global cpu_usage_history
    cpu_usage = get_cpu_usage()
    if len(cpu_usage_history) >= 20:
        cpu_usage_history.pop(0)
    cpu_usage_history.append(cpu_usage)

# Function to start CPU monitoring
def start_cpu_monitoring():
    if not scheduler.running:
        scheduler.add_job(func=update_cpu_usage, trigger="interval", seconds=1)
        scheduler.start()

# Function to stop CPU monitoring
def stop_cpu_monitoring():
    if scheduler.running:
        scheduler.shutdown()
