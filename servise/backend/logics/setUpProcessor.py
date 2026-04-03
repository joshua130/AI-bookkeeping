from flask import Blueprint, request
import pandas as pd
import sqlite3

setUpProcessor_bp = Blueprint('setUpProcessor', __name__)

# データベース接続の関数
def get_db_connection():
    conn = sqlite3.connect(r'servise\backend\main.db')
    conn.row_factory = sqlite3.Row
    return conn



@setUpProcessor_bp.route('/setUp/postAccountItem', methods=['POST'])

def postIdAndName():
    conn = get_db_connection()

    code = request.form.get('code').strip()
    name = request.form.get('name').strip()

    cursor = conn.cursor()
    cursor.execute("SELECT id FROM companies WHERE id = ?", (code,))
    existing_id = cursor.fetchone()

    if existing_id:
        conn.close()
        return f'会社コード「{code}」は既に登録されています。', 400

    cursor.execute("INSERT INTO companies (id, name) VALUES (?, ?)", (code, name))
    conn.commit()
    conn.close()
    return '会社情報が正常に登録されました', 200





def postAccountItem():
    conn = get_db_connection()

    code = request.form.get('code').strip()
    print("Received Code:", code)
    file = request.files.get('file')

    cursor = conn.cursor()
    cursor.execute("SELECT id FROM accounts WHERE id = ?", (code,))
    existing_id = cursor.fetchone()

    if existing_id:
        conn.close()
        return f'会社コード「{code}」は既に登録されています。', 400

    file.seek(0)

    if not is_valid_file(file, accountItem_columns):
        conn.close()
        return '無効なファイル形式です', 400
    
    file.seek(0)  # ファイルポインタを先頭に戻す
    
    df = pd.read_csv(file,  names=accountItem_columns, skiprows=1)
    df = df.drop(columns=['フリガナ','資金'])
    df = df.rename(columns = {'勘定科目コード': 'accountItemCode', '勘定科目名': 'accountItemName', '口座別管理': 'manageByAccount', '取引先別管理': 'manageByPartner'})
    df.insert(0, 'id', code)

    print(df.head())  # デバッグ用にデータフレームの内容を表示

    df.to_sql('accounts', conn, if_exists='append', index=False)

    conn.commit()
    conn.close()
    return '勘定科目が正常に登録されました', 200
    

        

def is_valid_file(file , expected_columns):
    try:
        df_header = pd.read_csv(file , nrows=0)
        actual_header = df_header.columns.tolist()

        return set(expected_columns).issubset(set(actual_header))
    except Exception:
        return False
    
accountItem_columns = ['勘定科目コード','勘定科目名', 'フリガナ', '口座別管理', '取引先別管理', '資金']

