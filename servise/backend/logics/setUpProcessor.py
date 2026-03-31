from flask import Blueprint, request
import pandas as pd
import sqlite3

setUpProcessor_bp = Blueprint('setUpProcessor', __name__)

# データベース接続の関数
def get_db_connection():
    conn = sqlite3.connect('C:\\Users\\genjo\\MyProjects\\gemini\\servise\\backend\\main.db')
    conn.row_factory = sqlite3.Row
    return conn


@setUpProcessor_bp.route('/setUp/postAccountItem', methods=['POST'])
def postAccountItem():
    conn = get_db_connection()

    code = request.form.get('code')
    file = request.files.get('file')

    db_columns = ["accountItemName","accountItemCode","manageByAccount","manageByPartner"]

    if not is_valid_file(file, accountItem_columns):
        conn.close()
        return '無効なファイル形式です', 400
    
    file.seek(0)  # ファイルポインタを先頭に戻す
    
    df = pd.read_csv(file,  names=db_columns)
    df.insert(0, 'id', code)

    df.to_sql('account_items', conn, if_exists='append', index=False)
    #　なんかここが間違っているのでデータベースにずれて値が入る。

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

