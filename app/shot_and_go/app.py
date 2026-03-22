import os
import json
import dotenv
from flask import Flask, request, jsonify
from datetime import datetime

dotenv.load_dotenv()

app = Flask(__name__)
UPLOAD_FOLDER = os.getenv("WATCH_DIR")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# 簡易的なAPIアクセスキー (セキュリティのため)
API_KEY = 'YOUR_SECRET_API_KEY' # アプリ側にも同じ値を設定します

COMPANY_FILE = "companies.json"  # 企業情報のJSONファイル

if not os.path.exists(COMPANY_FILE):
    with open(COMPANY_FILE, 'w', encoding='utf-8') as f:
        json.dump([], f, ensure_ascii=False, indent=4)

@app.route('/companies', methods=['GET'])
def get_companies():
    key = request.headers.get('x-api-key')
    if key != API_KEY:
        return "Unauthorized", 401
    with open(COMPANY_FILE, 'r', encoding='utf-8') as f:
        companies = json.load(f)
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
    new_name = data.get('name')
    
    if not new_name:
        return "Name is required", 400

    # 現在のリストを読み込む
    with open(COMPANY_FILE, 'r', encoding='utf-8') as f:
        companies = json.load(f)
    
    # 重複チェック（既にある名前なら追加しない）
    if new_name not in companies:
        companies.append(new_name)
        # JSONを更新（indent=4で綺麗に保存）
        with open(COMPANY_FILE, 'w', encoding='utf-8') as f:
            json.dump(companies, f, ensure_ascii=False, indent=4)
        print(f"🆕 顧問先を追加しました: {new_name}")
        return jsonify({"message": "Success", "companies": companies}), 200
    else:
        return "Already exists", 409

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)    