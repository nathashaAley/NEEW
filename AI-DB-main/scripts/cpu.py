from flask import Flask, render_template, jsonify
import psutil
import matplotlib.pyplot as plt
import io
import base64
from apscheduler.schedulers.background import BackgroundScheduler

app = Flask(__name__)
cpu_usage_history = []

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

# Scheduler to update CPU usage every second
scheduler = BackgroundScheduler()
scheduler.add_job(func=update_cpu_usage, trigger="interval", seconds=1)
scheduler.start()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/cpu_usage')
def cpu_usage():
    return jsonify(cpu_usage_history)

@app.route('/cpu_plot')
def cpu_plot():
    fig, ax = plt.subplots()
    ax.plot(cpu_usage_history, label='CPU Usage (%)')
    ax.set_xlabel('Time (seconds)')
    ax.set_ylabel('CPU Usage (%)')
    ax.set_ylim(0, 100)
    ax.legend(loc='upper right')

    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode()

    plt.close(fig)
    return f"data:image/png;base64,{plot_url}"

@app.route('/cpu_notification')
def cpu_notification():
    if cpu_usage_history and max(cpu_usage_history) > 80:  # Threshold for high CPU usage
        return jsonify({'alert': 'High CPU Usage Detected!'})
    return jsonify({'alert': 'CPU Usage is Normal'})

if __name__ == '__main__':
    try:
        app.run(debug=True, host='0.0.0.0', use_reloader=False)
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()
