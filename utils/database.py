import psycopg2
from datetime import datetime


class DBConnector:
    def __init__(self, db_url, initial_queries=None):
        self.db_url = db_url
        self.conn = None
        self.initial_queries = initial_queries or []
        
    def add_initial_query(self, query):
        self.initial_queries.append(query)

    def get_connection(self, force_update=False):
        if self.conn is None or self.conn.closed or force_update:
            try:
                self.conn = psycopg2.connect(self.db_url)
                cur = self.conn.cursor()
                for query in self.initial_queries:
                    cur.execute(query)
                self.conn.commit()
            except Exception:
                self.conn = None
        return self.conn


class DBLogger:
    def __init__(self, connector):
        self.connector = connector
        self.connector.add_initial_query("CREATE TABLE IF NOT EXISTS dialog(chat_id varchar, user_name varchar, query varchar, response varchar, actualtime timestamp)")
    
    def log_message(self, message, response=None):
        conn = self.connector.get_connection()
        if conn is not None:
            cur = conn.cursor()
            query = "INSERT INTO dialog VALUES('{}', '{}', '{}', '{}', TIMESTAMP '{}')".format(
                message.chat.id, 
                message.chat.username, 
                message.text, 
                response, 
                datetime.now()
            )
            cur.execute(query)
            conn.commit()

class GroupManager:
    def __init__(self, connector):
        self.connector = connector
        self.users = []
        self.admins = []
        self.update_groups()
    
    def update_groups(self):
        # todo: connect to database or Google Sheets
        self.users = ["cointegrated"]
        self.admins = ["cointegrated"]