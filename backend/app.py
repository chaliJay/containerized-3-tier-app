from flask import Flask, jsonify
import os
import mysql.connector

app = Flask(__name__)

DB_HOST = os.getenv('DB_HOST','db')
DB_USER = os.getenv('DB_USER', 'appuser')
DB_PASSWORD = os.getenv('DB_PASSWORD','changeme')
DB_NAME = os.getenv('DB_NAME','appdb')

@app.get('/api/health')
def health():
      return jsonify(status='ok')

@app.route('/api')
def index():
    try:
      conn = mysql.connector.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD, database=DB_NAME)
      cur = conn.cursor()

      cur.execute("SELECT 'Hello from MYSQL via Flask! '")
      message = cur.fetchone()[0]

      cur.execute("INSERT INTO counter () VALUES ()")
      conn.commit()
        
      cur.execute("SELECT COUNT(*) FROM counter")
      visitor_count = cur.fetchone()[0]

      cur.execute("SELECT NOW()")
      db_time = cur.fetchone()[0]
        
      cur.close()
      conn.close()
        
      return jsonify({
            "message": message,
            "visitor_count": visitor_count,
            "db_time": str(db_time)
      })
    except Exception as e:
        return jsonify({"error": str(e)})
    
if __name__ == '__main__':
      app.run(host = '0.0.0.0', port = 8000, debug = True)
