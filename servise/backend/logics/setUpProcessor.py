from flask import request
import pandas as pd
import sqlite3
from server import app,get_db_connection

@app.route('/setUp/postAccountItem', methods=['POST'])
def postAccountItem():
    conn = get_db_connection()
    
    code = request.form.get('code')
    file = request.files.get('file')
    
    try:
        df = pd.read_csv(file)
        
