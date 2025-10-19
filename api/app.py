from flask import Flask, jsonify
import sqlite3
import os
from routes import api_bp
from generate_go import generate_bp

app = Flask(__name__)

DATABASE = 'production.db'

def get_db():
    db = sqlite3.connect(DATABASE)
    db.row_factory = sqlite3.Row
    return db

def init_db():
    with app.app_context():
        db = get_db()
        db.execute('''
            CREATE TABLE IF NOT EXISTS config (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                var_conf TEXT UNIQUE NOT NULL,
                value_conf TEXT NOT NULL
            )
        ''')
        db.execute('''
            CREATE TABLE IF NOT EXISTS model (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                table_code TEXT UNIQUE NOT NULL,
                table_name TEXT NOT NULL
            )
        ''')
        db.execute('''
            CREATE TABLE IF NOT EXISTS model_detail (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                model_code TEXT NOT NULL,
                model_detail_code TEXT NOT NULL,
                model_detail_name TEXT NOT NULL,
                model_detail_type TEXT NOT NULL CHECK (model_detail_type IN ('varchar', 'int', 'id')),
                UNIQUE(model_code, model_detail_code)
            )
        ''')
        # Insert initial config if not exists
        db.execute('INSERT OR IGNORE INTO config (var_conf, value_conf) VALUES (?, ?)', ('LANG', 'Go'))
        db.commit()

# Initialize database on startup
init_db()

# Register API routes
app.register_blueprint(api_bp)
app.register_blueprint(generate_bp)

@app.route('/')
def home():
    return jsonify({"message": "Welcome to the Production API!"})

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)