import sqlite3
from flask import Flask ,jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

def get_db_connection():
    conn = sqlite3.connect('C:\\Users\\genjo\\MyProjects\\gemini\\servise\\backend\\main.db')
    conn.row_factory = sqlite3.Row
    return conn


@app.route('/get_company', methods=['GET'])
def get_company():
    conn = get_db_connection()
    companies = conn.execute('SELECT * FROM companies').fetchall()
    conn.close()
    return jsonify([dict(company) for company in companies])

@app.route('/post_company', methods=['POST'])
def post_company():
    conn = get_db_connection()
    


if __name__ == '__main__':
    app.run(debug=True, host="127.0.0.1", port=5000)