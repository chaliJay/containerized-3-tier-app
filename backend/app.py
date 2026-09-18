from flask import Flask, jsonify
import os
import mysql.connector

app = Flask(___name___)

DB_HOST = os.getenv('DB_HOST','db')
DB_USER = os.getenv('DB_USER', 'appuser')
DB_PASSWORD = os.getuser('DB-PASSWORD','changeme')
DB_NAME = os.getenv('DB_NAME','appdb')

@app.get('/api/health')
def health():
        return jsonify(status='ok')

@app.get('/api')
def index():
    conn = mysql.connector.connect(
          hist = DB_HOST, user =DB_USER, password = DB_PASSWORD, database = DB_NAME
    )
    cur = conn.cursor()
    cur.execute("SELECT 'Hello from MYSQL via Flask! '")
    row = cur.fetchone()
    cur.close()
    conn.close()
    return jsonify(message = row[0])

if __name__ == '__main__':
      app.run(host = '0.0.0.0', port = 8000, debug = true)
