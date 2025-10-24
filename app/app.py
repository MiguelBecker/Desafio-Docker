import os
import time
from flask import Flask, request, jsonify
import psycopg2
import psycopg2.extras

DB_HOST = os.getenv("DB_HOST", "meu-banco")
DB_NAME = os.getenv("DB_NAME", "mensagensdb")
DB_USER = os.getenv("DB_USER", "usuario")
DB_PASS = os.getenv("DB_PASS", "senha123")

def get_conn():
    for i in range(10):
        try:
            return psycopg2.connect(
                host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASS
            )
        except Exception as e:
            print(f"Tentando conectar ao banco... ({i+1}/10) - {e}")
            time.sleep(2)
    raise RuntimeError("Não foi possível conectar ao PostgreSQL.")

conn = get_conn()
with conn.cursor() as cur:
    cur.execute("""
        CREATE TABLE IF NOT EXISTS mensagens (
            id SERIAL PRIMARY KEY,
            texto TEXT NOT NULL,
            criado_em TIMESTAMP DEFAULT NOW()
        );
    """)
    conn.commit()

app = Flask(__name__)

@app.route('/mensagem', methods=['POST'])
def add_msg():
    data = request.get_json(silent=True) or {}
    texto = data.get('texto')
    if not texto:
        return jsonify({"erro": "Campo 'texto' é obrigatório"}), 400
    with conn.cursor() as cur:
        cur.execute("INSERT INTO mensagens (texto) VALUES (%s) RETURNING id;", (texto,))
        novo_id = cur.fetchone()[0]
    conn.commit()
    return jsonify({"status": "mensagem salva", "id": novo_id}), 201

@app.route('/mensagens', methods=['GET'])
def get_msgs():
    with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
        cur.execute("SELECT id, texto, criado_em FROM mensagens ORDER BY id;")
        rows = cur.fetchall()
    return jsonify(rows)

@app.route('/health')
def health():
    return jsonify({"status": "ok"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
