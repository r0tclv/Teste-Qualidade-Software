from flask import Flask, request, jsonify
import sqlite3
import os

app = Flask(__name__)
DATABASE = None  # Will be set to 'disciplinas.db' when None at init


def get_db():
    db_path = app.config.get('DATABASE') or 'disciplinas.db'
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS disciplinas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            data_inicio TEXT NOT NULL,
            data_termino TEXT NOT NULL,
            vagas INTEGER NOT NULL,
            verao INTEGER NOT NULL DEFAULT 0
        )
    ''')
    conn.commit()
    conn.close()


@app.route('/disciplinas', methods=['GET'])
def get_disciplinas():
    conn = get_db()
    rows = conn.execute('SELECT * FROM disciplinas').fetchall()
    conn.close()
    disciplinas = []
    for row in rows:
        disciplinas.append({
            'id': row['id'],
            'titulo': row['titulo'],
            'data_inicio': row['data_inicio'],
            'data_termino': row['data_termino'],
            'vagas': row['vagas'],
            'verao': bool(row['verao'])
        })
    return jsonify(disciplinas)


@app.route('/disciplinas/<int:id>', methods=['GET'])
def get_disciplina(id):
    conn = get_db()
    row = conn.execute('SELECT * FROM disciplinas WHERE id = ?', (id,)).fetchone()
    conn.close()
    if row is None:
        return jsonify({'error': 'Disciplina nao encontrada'}), 404
    return jsonify({
        'id': row['id'],
        'titulo': row['titulo'],
        'data_inicio': row['data_inicio'],
        'data_termino': row['data_termino'],
        'vagas': row['vagas'],
        'verao': bool(row['verao'])
    })


@app.route('/disciplinas', methods=['POST'])
def create_disciplina():
    data = request.get_json()
    if not data or not all(k in data for k in ('titulo', 'data_inicio', 'data_termino', 'vagas', 'verao')):
        return jsonify({'error': 'Campos obrigatorios: titulo, data_inicio, data_termino, vagas, verao'}), 400

    conn = get_db()
    cursor = conn.execute(
        'INSERT INTO disciplinas (titulo, data_inicio, data_termino, vagas, verao) VALUES (?, ?, ?, ?, ?)',
        (data['titulo'], data['data_inicio'], data['data_termino'], data['vagas'], int(data['verao']))
    )
    conn.commit()
    new_id = cursor.lastrowid
    conn.close()
    return jsonify({'id': new_id, 'mensagem': 'Disciplina criada com sucesso'}), 201


@app.route('/disciplinas/<int:id>', methods=['PUT'])
def update_disciplina(id):
    conn = get_db()
    row = conn.execute('SELECT * FROM disciplinas WHERE id = ?', (id,)).fetchone()
    if row is None:
        conn.close()
        return jsonify({'error': 'Disciplina nao encontrada'}), 404

    data = request.get_json()
    if not data:
        conn.close()
        return jsonify({'error': 'Nenhum dado fornecido'}), 400

    titulo = data.get('titulo', row['titulo'])
    data_inicio = data.get('data_inicio', row['data_inicio'])
    data_termino = data.get('data_termino', row['data_termino'])
    vagas = data.get('vagas', row['vagas'])
    verao = data.get('verao', row['verao'])

    conn.execute(
        'UPDATE disciplinas SET titulo = ?, data_inicio = ?, data_termino = ?, vagas = ?, verao = ? WHERE id = ?',
        (titulo, data_inicio, data_termino, vagas, int(verao), id)
    )
    conn.commit()
    conn.close()
    return jsonify({'mensagem': 'Disciplina atualizada com sucesso'})


@app.route('/disciplinas/<int:id>', methods=['DELETE'])
def delete_disciplina(id):
    conn = get_db()
    row = conn.execute('SELECT * FROM disciplinas WHERE id = ?', (id,)).fetchone()
    if row is None:
        conn.close()
        return jsonify({'error': 'Disciplina nao encontrada'}), 404

    conn.execute('DELETE FROM disciplinas WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return jsonify({'mensagem': 'Disciplina removida com sucesso'})


@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok'})


if __name__ == '__main__':
    init_db()
    app.run(debug=True, port=5000)
