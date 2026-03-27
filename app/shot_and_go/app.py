import os
import sqlite3
import dotenv
from flask import Flask, request, jsonify
from datetime import datetime

dotenv.load_dotenv()

app = Flask(__name__)
UPLOAD_FOLDER = os.getenv("WATCH_DIR")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# 簡易的なAPIアクセスキー (セキュリティのため)
API_KEY = 'YOUR_SECRET_API_KEY' # アプリ側にも同じ値を設定します
DB_FILE = "main.db"  # SQLiteデータベースファイル


#データベースの初期化
def init_db():
    with sqlite3.connect(DB_FILE) as conn:
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS companies (
                code TEXT PRIMARY KEY,
                name TEXT UNIQUE NOT NULL
            )
        ''')
        conn.commit()

init_db()

#顧問先リスト取得（select）
#APIキーが正しい場合のみ、データベースから顧問先の名前を取得して返す
#APIキーが間違っている場合は、401 Unauthorizedを返す

# --- 2. 顧問先リストを取得する窓口 ---
@app.route('/companies', methods=['GET'])
def get_companies():
    key = request.headers.get('x-api-key')
    if key != API_KEY:
        return "Unauthorized", 401
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT code, name FROM companies ORDER BY code ASC")
        companies = [{"code": row[0], "name": row[1]} for row in cursor.fetchall()]
    return jsonify(companies)

# スマホからのPOSTリクエストのみを受け付ける窓口
@app.route('/upload', methods=['POST'])
def upload():
    # シンプルなセキュリティチェック
    key = request.headers.get('x-api-key')
    if key != API_KEY:
        return "Unauthorized", 401

    company_name = request.form.get('company', 'Unknown')
    company_folder = os.path.join(UPLOAD_FOLDER, company_name)
    os.makedirs(company_folder, exist_ok=True)

    file = request.files.get('photo')
    if not file:
        return "No file", 400

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    _, extension = os.path.splitext(file.filename)
    new_filename = f"{timestamp}{extension}"
    
    filepath = os.path.join(company_folder, new_filename)
    file.save(filepath)
    print(f"✅ [{company_name}] 保存完了")
    return "OK", 200

# --- 3. 顧問先を追加する窓口 ---
@app.route('/add_company', methods=['POST'])
def add_company():
    key = request.headers.get('x-api-key')
    if key != API_KEY:
        return "Unauthorized", 401
    
    # スマホから送られてくるJSONデータを取得
    data = request.get_json()
    new_name = data.get('name', '').strip()
    
    if not new_name:
        return "Name is required", 400

    try:
        with sqlite3.connect(DB_FILE) as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO companies (name) VALUES (?)", (new_name,))
            conn.commit()
        return "Company added", 200
    except sqlite3.IntegrityError:
        return "Company already exists", 409

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)    