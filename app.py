from flask import Flask, request, jsonify, send_from_directory
import psycopg2
from psycopg2 import Error

app = Flask(__name__)

# Configuration de la base de données PostgreSQL
DB_HOST = "db"
DB_NAME = "identity_db"
DB_USER = "user"
DB_PASS = "password"

def get_db_connection():
    conn = None
    try:
        conn = psycopg2.connect(host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASS)
        return conn
    except Error as e:
        print(f"Erreur de connexion à la base de données: {e}")
        return None

def init_db():
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS identities (
                id VARCHAR(20) PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                dob VARCHAR(10) NOT NULL,
                fingerprint VARCHAR(255) NOT NULL,
                status VARCHAR(50) NOT NULL
            );
        """)
        conn.commit()
        cursor.close()
        conn.close()

# Initialisation de la base de données au démarrage de l'application
with app.app_context():
    init_db()

@app.route("/")
def serve_index():
    return send_from_directory(".", "index.html")

@app.route("/register", methods=["POST"])
def register_identity():
    data = request.json
    if not data or 'name' not in data or 'dob' not in data or 'fingerprint' not in data:
        return jsonify({'error': 'Données manquantes: nom, date de naissance, empreinte digitale sont requis.'}), 400

    conn = get_db_connection()
    if not conn:
        return jsonify({'error': 'Impossible de se connecter à la base de données.'}), 500

    cursor = conn.cursor()
    try:
        # Générer un ID unique (simple incrément pour la démo, en prod utiliser un UUID ou une séquence DB)
        cursor.execute("SELECT COUNT(*) FROM identities;")
        count = cursor.fetchone()[0]
        identity_id = f'ID-{count + 1:05d}'

        cursor.execute("""
            INSERT INTO identities (id, name, dob, fingerprint, status)
            VALUES (%s, %s, %s, %s, %s)
        """, (identity_id, data['name'], data['dob'], data['fingerprint'], 'active'))
        conn.commit()

        return jsonify({
            'message': 'Identité enregistrée avec succès',
            'identity': {
                'id': identity_id,
                'name': data['name'],
                'dob': data['dob'],
                'fingerprint': data['fingerprint'],
                'status': 'active'
            }
        }), 201
    except Error as e:
        conn.rollback()
        return jsonify({'error': f'Erreur lors de l\'enregistrement: {e}'}), 500
    finally:
        cursor.close()
        conn.close()

@app.route("/authenticate", methods=["POST"])
def authenticate_identity():
    data = request.json
    if not data or 'id' not in data or 'fingerprint' not in data:
        return jsonify({'error': 'Données manquantes: ID et empreinte digitale sont requis.'}), 400

    conn = get_db_connection()
    if not conn:
        return jsonify({'error': 'Impossible de se connecter à la base de données.'}), 500

    cursor = conn.cursor()
    try:
        cursor.execute("SELECT id, name, dob, fingerprint, status FROM identities WHERE id = %s;", (data['id'],))
        stored_identity = cursor.fetchone()

        if not stored_identity:
            return jsonify({'error': 'Identité non trouvée.'}), 404

        identity_dict = {
            'id': stored_identity[0],
            'name': stored_identity[1],
            'dob': stored_identity[2],
            'fingerprint': stored_identity[3],
            'status': stored_identity[4]
        }

        if identity_dict['fingerprint'] == data['fingerprint']:
            return jsonify({'message': 'Authentification réussie', 'identity': identity_dict}), 200
        else:
            return jsonify({'error': 'Empreinte digitale incorrecte.'}), 401
    except Error as e:
        return jsonify({'error': f'Erreur lors de l\'authentification: {e}'}), 500
    finally:
        cursor.close()
        conn.close()

@app.route("/identity/<identity_id>", methods=["GET"])
def get_identity(identity_id):
    conn = get_db_connection()
    if not conn:
        return jsonify({'error': 'Impossible de se connecter à la base de données.'}), 500

    cursor = conn.cursor()
    try:
        cursor.execute("SELECT id, name, dob, fingerprint, status FROM identities WHERE id = %s;", (identity_id,))
        stored_identity = cursor.fetchone()

        if not stored_identity:
            return jsonify({'error': 'Identité non trouvée.'}), 404

        identity_dict = {
            'id': stored_identity[0],
            'name': stored_identity[1],
            'dob': stored_identity[2],
            'fingerprint': stored_identity[3],
            'status': stored_identity[4]
        }
        return jsonify({'identity': identity_dict}), 200
    except Error as e:
        return jsonify({'error': f'Erreur lors de la récupération de l\'identité: {e}'}), 500
    finally:
        cursor.close()
        conn.close()

@app.route("/identities", methods=["GET"])
def list_identities():
    conn = get_db_connection()
    if not conn:
        return jsonify({'error': 'Impossible de se connecter à la base de données.'}), 500

    cursor = conn.cursor()
    try:
        cursor.execute("SELECT id, name, dob, fingerprint, status FROM identities;")
        all_identities = cursor.fetchall()

        identities_list = []
        for identity in all_identities:
            identities_list.append({
                'id': identity[0],
                'name': identity[1],
                'dob': identity[2],
                'fingerprint': identity[3],
                'status': identity[4]
            })
        return jsonify({'identities': identities_list}), 200
    except Error as e:
        return jsonify({'error': f'Erreur lors de la liste des identités: {e}'}), 500
    finally:
        cursor.close()
        conn.close()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)