import cx_Oracle
from datetime import datetime, timedelta

# Replace with your actual database credentials and DSN
dsn = cx_Oracle.makedsn('192.168.1.50', '1531', service_name='testcdb')
connection = cx_Oracle.connect('SYSTEM', 'BatMan1234', dsn=dsn)
cursor = connection.cursor()

def fetch_long_running_queries():
    try:
        # Prompt user for time threshold in seconds
        elapsed_time_threshold_seconds = int(input("Enter the minimum elapsed time threshold (in seconds) for long-running queries: "))

        # SQL query to fetch long-running queries that are still running
        sql_query = """
        SELECT sql_id, sql_fulltext, first_load_time, last_active_time, elapsed_time/1000000 as elapsed_sec
        FROM v$sql
        WHERE elapsed_time > :elapsed_time_threshold_seconds * 1000000
        AND last_active_time >= SYSDATE - (elapsed_time / 1000000 / 86400)
        ORDER BY elapsed_time DESC
        """

        cursor.execute(sql_query, {'elapsed_time_threshold_seconds': elapsed_time_threshold_seconds})
        long_running_queries = cursor.fetchall()

        return long_running_queries

    except cx_Oracle.Error as error:
        print(f"Error fetching long-running queries: {error}")
        return []

def display_long_running_queries(long_running_queries):
    for query in long_running_queries:
        sql_id, sql_fulltext_lob, start_time, last_active_time, elapsed_sec = query

        # Convert LOB to string
        sql_text = sql_fulltext_lob.read()
        if len(sql_text) > 200:
            sql_text = sql_text[:200] + "..."  # Displaying only first 200 characters of SQL text

        print(f"SQL ID: {sql_id}")
        print(f"SQL Text: {sql_text}")
        print(f"Start Time: {start_time}")
        print(f"Last Active Time: {last_active_time}")
        print(f"Elapsed Time (sec): {elapsed_sec}")
        print("-" * 50)

def main():
    long_running_queries = fetch_long_running_queries()
    if long_running_queries:
        display_long_running_queries(long_running_queries)
    else:
        print("No long-running queries found.")

    cursor.close()
    connection.close()

if __name__ == "__main__":
    main()
