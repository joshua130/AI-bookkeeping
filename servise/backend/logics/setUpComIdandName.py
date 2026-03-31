from server import app, get_db_connection
from flask import request

@app.route('/setUp/companyIdandName', methods=['POST'])
def companyIdandName():
    code = request.form.get('code')
    name = request.form.get('name')
    conn = get_db_connection()