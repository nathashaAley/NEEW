from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import cx_Oracle
import paramiko
import cohere
import psutil
import logging
from googlesearch import search
from bs4 import BeautifulSoup
import requests
import re
import connection
import longrun
import cursor
import json

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Dummy user data for authentication
users = {
    'admin': 'adminpass1',  # Admin credentials
     'user1': 'userpass1' 
}

# Database connection details
oracle_username = 'apps'   # Update username
oracle_password = 'apps'   # Update password
oracle_dsn = '192.168.1.50:1531/TEST'  #Update DSN

# Replace with your actual database credentials and DSN
dsn = cx_Oracle.makedsn('192.168.1.50', '1531', service_name='testcdb')
connection = cx_Oracle.connect('SYSTEM', 'BatMan1234', dsn=dsn)
cursor = connection.cursor()

try:
    cx_Oracle.init_oracle_client(lib_dir=r"C:\oracle\instantclient_19_23")
except Exception as e:
    print(f"Error initializing Oracle Client: {e}")

# Database configuration (replace with your database credentials)
db_config = {
    'username': 'your_db_username',
    'password': 'your_db_password',
    'hostname': 'your_db_hostname',
    'port': 'your_db_port',
    'service_name': 'your_db_service_name'
}

# Function to check if logged in
def is_logged_in():
    return session.get('logged_in', False)

@app.route('/')
def home():
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Check if username and password match admin or user1 credentials
        if (username == 'admin' and password == 'adminpass1') or \
           (username == 'user1' and password == 'userpass1'):
            # Set the session variables
            session['logged_in'] = True
            session['username'] = username
            
            # Redirect to connection page
            return redirect(url_for('connect'))
        else:
            # Invalid credentials
            error = 'Invalid username or password. Please try again.'
            return render_template('login.html', error=error)

    # For GET requests or initial page load
    return render_template('login.html')

@app.route('/connect', methods=['GET', 'POST'])
def connect():
    if not is_logged_in():
        return redirect(url_for('login'))

    if request.method == 'POST':
        # Retrieve form data
        hostname = request.form.get('hostname')
        port = request.form.get('port')
        db_username = request.form.get('db_username')
        db_password = request.form.get('db_password')
        service_name = request.form.get('service_name')
        ssh_username = request.form.get('ssh_username')
        ssh_password = request.form.get('ssh_password')

        # Example: Check database and SSH connection (replace with actual logic)
        db_connected = True
        ssh_connected = True

        if db_connected and ssh_connected:
            # Set session variables or use a database to store connection status
            session['db_connected'] = True
            session['ssh_connected'] = True

            # Return JSON response indicating success
            return jsonify({'status': 'success', 'message': 'Successfully connected!'})

        # If connection fails, return JSON response with error message
        return jsonify({'status': 'error', 'message': 'Connection failed. Please check your credentials.'})

    # Render the connect.html template
    return render_template('connect.html')

@app.route('/dashboard')
def dashboard():
    if not is_logged_in():
        return redirect(url_for('login'))
    
    username = session.get('username', 'Guest')  # Get the username from session
    db_connected = session.get('db_connected', False)
    ssh_connected = session.get('ssh_connected', False)
    
    admin_cards = [
        'CPU Utilization', 'Session Locks', 'Log4j Vulnerabilities','Long-Running Queries', 'Concurrent Programs',
        'Alert Logs','Audit Logs', 'Add Data Files', 'Kill Session Locks',
        'Request ID from SID', 'SID from PID', 'ID from Request ID',
        'Create User', 'Grant Privilege', 'Executed Program Status', 'Bounce Database',
        'Fetch Log File', 'Fetch Output Files'
    ]
    
    user_cards = [
        'Create User', 'Grant Privilege', 'Executed Program Status',
        'Check Status', 'Bounce Database', 'Request Now',
        'Fetch Log File', 'View Logs', 'Fetch Output Files'
    ]
    
    if username == 'admin':
        cards = admin_cards
    elif username == 'user1':
        cards = user_cards
    else:
        cards = []  # Handle other roles or default case
    
    return render_template('dashboard.html', username=username, db_connected=db_connected, ssh_connected=ssh_connected, cards=cards)


def test_db_connection(hostname, port, service_name, db_username, db_password):
    dsn = cx_Oracle.makedsn(hostname, port, service_name)
    try:
        connection = cx_Oracle.connect(db_username, db_password, dsn)
        connection.close()
        return True
    except cx_Oracle.DatabaseError as e:
        print(f"Database connection failed: {e}")
        return False

@app.route('/db_connect', methods=['POST'])
def db_connect():
    if not is_logged_in():
        return redirect(url_for('login'))

    hostname = request.form.get('hostname')
    port = request.form.get('port')
    db_username = request.form.get('db_username')
    db_password = request.form.get('db_password')
    service_name = request.form.get('service_name')

    if test_db_connection(hostname, port, service_name, db_username, db_password):
        session['db_connected'] = True
        session['db_details'] = {
            'hostname': hostname,
            'port': port,
            'db_username': db_username,
            'db_password': db_password,
            'service_name': service_name
        }
        return jsonify({'status': 'success', 'message': 'Database connection successful!'})
    else:
        return jsonify({'status': 'error', 'message': 'Failed to connect to the database. Please check your credentials.'})

@app.route('/create_user', methods=['POST'])
def create_user():
    if not is_logged_in() or not session.get('db_connected'):
        return jsonify({'status': 'error', 'message': 'Not connected to the database.'})

    db_details = session['db_details']
    dsn = cx_Oracle.makedsn(db_details['hostname'], db_details['port'], db_details['service_name'])
    try:
        connection = cx_Oracle.connect(db_details['db_username'], db_details['db_password'], dsn)
        cursor = connection.cursor()

        username = request.form.get('username')
        password = request.form.get('password')
        default_tablespace = request.form.get('default_tablespace')
        temporary_tablespace = request.form.get('temporary_tablespace')
        profile = request.form.get('profile')
        account_status = request.form.get('account_status')
        privileges = request.form.get('privileges')
        roles = request.form.get('roles')

        # Deserialize JSON data
        privileges = json.loads(privileges)
        roles = json.loads(roles)

        create_user_sql = f"""
        CREATE USER {username} IDENTIFIED BY {password}
        DEFAULT TABLESPACE {default_tablespace}
        TEMPORARY TABLESPACE {temporary_tablespace}
        PROFILE {profile}
        ACCOUNT {account_status}
        """
        cursor.execute(create_user_sql)

        for privilege in privileges:
            cursor.execute(f"GRANT {privilege} TO {username}")

        for role in roles:
            cursor.execute(f"GRANT {role} TO {username}")

        connection.commit()
        cursor.close()
        connection.close()
        return jsonify({'status': 'success', 'message': f'User {username} created successfully!'})

    except cx_Oracle.DatabaseError as e:
        error, = e.args
        return jsonify({'status': 'error', 'message': f'Error creating user: {error}'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': f'Unexpected error: {str(e)}'})

    except cx_Oracle.DatabaseError as e:
        error, = e.args
        return jsonify({'status': 'error', 'message': f'Error creating user: {error}'})

@app.route('/ssh_connect', methods=['POST'])
def ssh_connect():
    if not is_logged_in():
        return jsonify({'status': 'error', 'message': 'You are not logged in!'})

    ssh_username = request.form.get('ssh_username')
    ssh_password = request.form.get('ssh_password')
    hostname = request.form.get('ssh_hostname')
    
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        client.connect(hostname, username=ssh_username, password=ssh_password)
        client.close()
        
        session['ssh_connected'] = True  # Update ssh_connected status in session
        session['ssh_username'] = ssh_username
        session['ssh_password'] = ssh_password
        session['ssh_hostname'] = hostname
        
        return jsonify({'status': 'success', 'message': 'SSH connection successful!'})
    except paramiko.SSHException as e:
        return jsonify({'status': 'error', 'message': f'SSH connection failed: {str(e)}'})

@app.route('/chat', methods=['POST'])
def chat():
    co = cohere.Client('e1ZNFE0xtCTu9A4HtBXT93s9aTpRXvvQ79wEndBN')
    user_message = request.json.get('message')
    response = co.generate(
        model='command-nightly',
        prompt=user_message,
        max_tokens=300,
        temperature=0.9,
        k=0,
        p=0.75,
        stop_sequences=[],
        return_likelihoods='NONE'
    )
    bot_response = response.generations[0].text.strip()
    return jsonify({'response': bot_response})

@app.route('/fetch-long-running-queries', methods=['POST'])
def fetch_long_running_queries():
    cursor = connection.cursor()
    try:
        elapsed_time_threshold_seconds = int(request.json.get('elapsed_time', 3600))

        sql_query = """
        SELECT sql_id, sql_fulltext, first_load_time, last_active_time, elapsed_time/1000000 as elapsed_sec
        FROM v$sql
        WHERE elapsed_time > :elapsed_time_threshold_seconds * 1000000
        AND last_active_time >= SYSDATE - (elapsed_time / 1000000 / 86400)
        ORDER BY elapsed_time DESC
        """

        cursor.execute(sql_query, {'elapsed_time_threshold_seconds': elapsed_time_threshold_seconds})
        long_running_queries = cursor.fetchall()

        queries = []
        for query in long_running_queries:
            sql_id, sql_fulltext_lob, start_time, last_active_time, elapsed_sec = query
            sql_text = sql_fulltext_lob.read()
            if len(sql_text) > 200:
                sql_text = sql_text[:200] + "..."
            queries.append({
                'sql_id': sql_id,
                'sql_text': sql_text,
                'start_time': start_time.strftime("%Y-%m-%d %H:%M:%S"),
                'last_active_time': last_active_time.strftime("%Y-%m-%d %H:%M:%S"),
                'elapsed_sec': elapsed_sec
            })

        return jsonify({'success': True, 'queries': queries})

    except cx_Oracle.Error as error:
        print(f"Error fetching long-running queries: {error}")
        return jsonify({'success': False, 'error': str(error)})

    finally:
        cursor.close()

# Serve static files (e.g., longrun.js)
@app.route('/static/js/<path:path>')
def serve_static_js(path):
    return app.send_static_file('js/' + path)

@app.route('/fetch-log4j-vulnerability')
def fetch_log4j_vulnerability():
    query = "log4j vulnerability announcement oracle site:support.oracle.com"
    
    try:
        for url in search(query, num_results=1):
            if 'support.oracle.com' in url:
                app.logger.debug(f"Found URL: {url}")
                title, release_date, filename = search_and_extract_log4j_vulnerability(url)
                return jsonify({
                    "title": title,
                    "release_date": release_date,
                    "filename": filename
                })
        return jsonify({"error": "No relevant search result found on Oracle support site."})
    except Exception as e:
        app.logger.error(f"Error performing Google search: {e}")
        return jsonify({"error": f"Error performing Google search: {e}"})

def search_and_extract_log4j_vulnerability(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            if soup.find(text=re.compile(r'log4j', re.IGNORECASE)):
                title = soup.title.text.strip()
                release_date = extract_release_date(soup)
                filename = url.split('/')[-1].split('.')[0]
                return title, release_date, filename
        return "Log4j vulnerability not found", "Unknown Release Date", "Unknown Filename"
    except Exception as e:
        app.logger.error(f"Error searching for Log4j vulnerability: {e}")
        return "Error", "Unknown Release Date", "Unknown Filename"

def extract_release_date(soup):
    try:
        last_updated_text = soup.find(text=re.compile(r'Last updated on', re.IGNORECASE))
        if last_updated_text:
            date_match = re.search(r'Last updated on (.+?)(?=\.|\n|$)', last_updated_text)
            if date_match:
                return date_match.group(1).strip()
        return "Unknown Release Date"
    except Exception as e:
        app.logger.error(f"Error extracting release date: {e}")
        return "Unknown Release Date"
@app.route('/logout')
def logout():
    session['logged_in'] = False
    session['db_connected'] = False  # Reset db_connected status on logout
    session['ssh_connected'] = False  # Reset ssh_connected status on logout
    session.pop('username', None)  # Remove the username from session
    return redirect(url_for('login'))

@app.route('/get_session_locks_data')
def get_session_locks_data():
    try:
        # Connect to Oracle database
        connection = cx_Oracle.connect(oracle_username, oracle_password, oracle_dsn)
        cursor = connection.cursor()

        # SQL query to fetch session locks data
        sql_query = """
        SELECT s1.sid AS blocking_sid, s2.sid AS blocked_sid, s2.sql_id, s2.status, s2.serial#
        FROM v$lock l1
        JOIN v$session s1 ON s1.sid = l1.sid
        JOIN v$lock l2 ON l1.id1 = l2.id1 AND l1.id2 = l2.id2
        JOIN v$session s2 ON s2.sid = l2.sid
        WHERE l1.block = 1 AND l2.request > 0
        """

        cursor.execute(sql_query)
        session_locks = cursor.fetchall()

        session_lock_data = []
        for row in session_locks:
            blocking_sid, blocked_sid, sql_id, status, serial_num = row

            # Fetch full SQL text using SQL_ID
            sql_query_fulltext = f"""
            SELECT sql_fulltext
            FROM v$sql
            WHERE sql_id = '{sql_id}'
            """

            cursor.execute(sql_query_fulltext)
            sql_result = cursor.fetchone()

            if sql_result and isinstance(sql_result[0], cx_Oracle.LOB):
                sql_fulltext = sql_result[0].read()  # Convert LOB to string
            else:
                sql_fulltext = sql_result[0] if sql_result else 'No SQL text found'

            session_lock_data.append({
                'blocking_sid': blocking_sid,
                'blocked_sid': blocked_sid,
                'sql_id': sql_id,
                'sql_fulltext': sql_fulltext,
                'status': status,
                'serial_num': serial_num
            })

        cursor.close()
        connection.close()

        return jsonify(session_lock_data)

    except cx_Oracle.Error as e:
        logging.error(f"Error fetching session locks from database: {e}")
        return jsonify({"error": f"Error fetching session locks from database: {e}"}), 500
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        return jsonify({"error": f"Unexpected error: {e}"}), 500

@app.route('/fetch-concurrent-programs')
def fetch_concurrent_programs():
    try:
        # Connect to Oracle database
        connection = cx_Oracle.connect(oracle_username, oracle_password, oracle_dsn)
        cursor = connection.cursor()

        # SQL query to fetch concurrent programs data
        sql_query = """
        SELECT program_name, status, start_time, end_time, progress
        FROM your_concurrent_programs_table
        """

        cursor.execute(sql_query)
        concurrent_programs = cursor.fetchall()

        cursor.close()
        connection.close()

        # Prepare JSON response
        programs_list = []
        for program in concurrent_programs:
            programs_list.append({
                'program_name': program[0],
                'status': program[1],
                'start_time': str(program[2]),  # Ensure datetime objects are converted to string
                'end_time': str(program[3]),    # Ensure datetime objects are converted to string
                'progress': program[4]
            })

        return jsonify(programs_list)

    except cx_Oracle.Error as e:
        logging.error(f"Error fetching concurrent programs: {e}")
        return jsonify({"error": f"Error fetching concurrent programs: {e}"}), 500
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        return jsonify({"error": f"Unexpected error: {e}"}), 500


    except cx_Oracle.Error as e:
        logging.error(f"Error fetching concurrent programs: {e}")
        return jsonify({"error": f"Error fetching concurrent programs: {e}"}), 500
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        return jsonify({"error": f"Unexpected error: {e}"}), 500



@app.route('/cpu_utilization', methods=['GET'])
def cpu_utilization():
    if not is_logged_in() or not session.get('ssh_connected'):
        return jsonify({'status': 'error', 'message': 'You are not logged in or SSH not connected!'})

    # Replace this block with actual SSH command execution if needed
    cpu_util = psutil.cpu_percent(interval=1)
    
    return jsonify({'status': 'success', 'cpu_util': cpu_util})
if __name__ == '__main__':
    app.run(debug=True)
