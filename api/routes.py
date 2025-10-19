from flask import Blueprint, jsonify, request
import sqlite3
import os

api_bp = Blueprint('api', __name__)

DATABASE = os.path.join(os.path.dirname(__file__), 'production.db')

def get_db():
    db = sqlite3.connect(DATABASE)
    db.row_factory = sqlite3.Row
    return db

# Config endpoints
@api_bp.route('/api/config', methods=['GET'])
def get_configs():
    db = get_db()
    configs = db.execute('SELECT * FROM config').fetchall()
    db.close()
    return jsonify([dict(row) for row in configs])

@api_bp.route('/api/config/<var_conf>', methods=['GET'])
def get_config(var_conf):
    db = get_db()
    config = db.execute('SELECT * FROM config WHERE var_conf = ?', (var_conf,)).fetchone()
    db.close()
    if config:
        return jsonify(dict(config))
    return jsonify({'error': 'Config not found'}), 404

@api_bp.route('/api/config/<var_conf>', methods=['PUT'])
def update_config(var_conf):
    data = request.get_json()
    value_conf = data.get('value_conf')
    if not value_conf:
        return jsonify({'error': 'value_conf required'}), 400
    db = get_db()
    db.execute('UPDATE config SET value_conf = ? WHERE var_conf = ?', (value_conf, var_conf))
    if db.total_changes == 0:
        db.close()
        return jsonify({'error': 'Config not found'}), 404
    db.commit()
    db.close()
    return jsonify({'message': 'Config updated'})

# Model endpoints
@api_bp.route('/api/model', methods=['GET'])
def get_models():
    db = get_db()
    models = db.execute('SELECT * FROM model').fetchall()
    db.close()
    return jsonify([dict(row) for row in models])

@api_bp.route('/api/model', methods=['POST'])
def create_model():
    data = request.get_json()
    table_code = data.get('table_code')
    table_name = data.get('table_name')
    if not table_code or not table_name:
        return jsonify({'error': 'table_code and table_name required'}), 400
    db = get_db()
    try:
        cursor = db.execute('INSERT INTO model (table_code, table_name) VALUES (?, ?)', (table_code, table_name))
        db.commit()
        model_id = cursor.lastrowid
        db.close()
        return jsonify({'message': 'Model created', 'id': model_id}), 201
    except sqlite3.IntegrityError:
        db.close()
        return jsonify({'error': 'table_code must be unique'}), 400

@api_bp.route('/api/model/<table_code>', methods=['GET'])
def get_model(table_code):
    db = get_db()
    model = db.execute('SELECT * FROM model WHERE table_code = ?', (table_code,)).fetchone()
    db.close()
    if model:
        return jsonify(dict(model))
    return jsonify({'error': 'Model not found'}), 404

@api_bp.route('/api/model/<table_code>', methods=['PUT'])
def update_model(table_code):
    data = request.get_json()
    table_name = data.get('table_name')
    if not table_name:
        return jsonify({'error': 'table_name required'}), 400
    db = get_db()
    db.execute('UPDATE model SET table_name = ? WHERE table_code = ?', (table_name, table_code))
    if db.total_changes == 0:
        db.close()
        return jsonify({'error': 'Model not found'}), 404
    db.commit()
    db.close()
    return jsonify({'message': 'Model updated'})

@api_bp.route('/api/model/<table_code>', methods=['DELETE'])
def delete_model(table_code):
    db = get_db()
    db.execute('DELETE FROM model WHERE table_code = ?', (table_code,))
    if db.total_changes == 0:
        db.close()
        return jsonify({'error': 'Model not found'}), 404
    db.commit()
    db.close()
    return jsonify({'message': 'Model deleted'})

# Model Detail endpoints
@api_bp.route('/api/model_detail', methods=['GET'])
def get_model_details():
    db = get_db()
    details = db.execute('SELECT * FROM model_detail').fetchall()
    db.close()
    return jsonify([dict(row) for row in details])

@api_bp.route('/api/model_detail', methods=['POST'])
def create_model_detail():
    data = request.get_json()
    model_code = data.get('model_code')
    model_detail_code = data.get('model_detail_code')
    model_detail_name = data.get('model_detail_name')
    model_detail_type = data.get('model_detail_type')
    if not all([model_code, model_detail_code, model_detail_name, model_detail_type]):
        return jsonify({'error': 'All fields required'}), 400
    if model_detail_type not in ['varchar', 'int', 'id']:
        return jsonify({'error': 'model_detail_type must be varchar, int, or id'}), 400
    db = get_db()
    try:
        cursor = db.execute('INSERT INTO model_detail (model_code, model_detail_code, model_detail_name, model_detail_type) VALUES (?, ?, ?, ?)',
                   (model_code, model_detail_code, model_detail_name, model_detail_type))
        db.commit()
        detail_id = cursor.lastrowid
        db.close()
        return jsonify({'message': 'Model detail created', 'id': detail_id}), 201
    except sqlite3.IntegrityError:
        db.close()
        return jsonify({'error': 'model_detail_code must be unique for this model_code'}), 400

@api_bp.route('/api/model_detail/<model_detail_code>', methods=['GET'])
def get_model_detail(model_detail_code):
    db = get_db()
    detail = db.execute('SELECT * FROM model_detail WHERE model_detail_code = ?', (model_detail_code,)).fetchone()
    db.close()
    if detail:
        return jsonify(dict(detail))
    return jsonify({'error': 'Model detail not found'}), 404

@api_bp.route('/api/model_detail/<model_detail_code>', methods=['PUT'])
def update_model_detail(model_detail_code):
    data = request.get_json()
    model_code = data.get('model_code')
    model_detail_name = data.get('model_detail_name')
    model_detail_type = data.get('model_detail_type')
    if not all([model_code, model_detail_name, model_detail_type]):
        return jsonify({'error': 'model_code, model_detail_name, and model_detail_type required'}), 400
    if model_detail_type not in ['varchar', 'int', 'id']:
        return jsonify({'error': 'model_detail_type must be varchar, int, or id'}), 400
    db = get_db()
    db.execute('UPDATE model_detail SET model_code = ?, model_detail_name = ?, model_detail_type = ? WHERE model_detail_code = ?',
               (model_code, model_detail_name, model_detail_type, model_detail_code))
    if db.total_changes == 0:
        db.close()
        return jsonify({'error': 'Model detail not found'}), 404
    db.commit()
    db.close()
    return jsonify({'message': 'Model detail updated'})

@api_bp.route('/api/model_detail/<model_detail_code>', methods=['DELETE'])
def delete_model_detail(model_detail_code):
    db = get_db()
    db.execute('DELETE FROM model_detail WHERE model_detail_code = ?', (model_detail_code,))
    if db.total_changes == 0:
        db.close()
        return jsonify({'error': 'Model detail not found'}), 404
    db.commit()
    db.close()
    return jsonify({'message': 'Model detail deleted'})