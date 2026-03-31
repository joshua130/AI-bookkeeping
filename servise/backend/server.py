import sqlite3
from flask import Flask ,jsonify, request
from flask_cors import CORS
from logics.setUpProcessor import setUpProcessor_bp

app = Flask(__name__)
CORS(app)
app.register_blueprint(setUpProcessor_bp)


# 会社情報を取得するエンドポイント
# 基本的にはコードと会社名を返すためにつかう
@app.route('/get_company', methods=['GET'])
def get_company():
    conn = get_db_connection()
    companies = conn.execute('SELECT * FROM companies').fetchall()
    conn.close()
    return jsonify([dict(company) for company in companies])




if __name__ == '__main__':
    app.run(debug=True, host="127.0.0.1", port=5000)