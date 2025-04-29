from flask import Flask, request, jsonify
import sqlite3
import os  # Para verificar si el archivo de la base de datos ya existe

app = Flask(__name__)

DATABASE = "biblioteca.sqlite"

# Crear base de datos y tabla si no existen
def init_db():
    if not os.path.exists(DATABASE):  # Comprobar si ya existe la base de datos
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS libro (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                codigo TEXT NOT NULL,
                nombre TEXT NOT NULL,
                autor TEXT NOT NULL,
                editorial TEXT NOT NULL,
                imagen TEXT
            )
        """)
        conn.commit()
        conn.close()
        print("Base de datos y tabla creadas exitosamente!")

# Conexión a la base de datos
def db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

# Rutas de la API
@app.route('/libros', methods=['GET'])
def get_libros():
    conn = db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM libro")
    libros = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return jsonify(libros)

@app.route('/libros', methods=['POST'])
def add_libro():
    new_libro = request.json
    codigo = new_libro.get('codigo')
    nombre = new_libro.get('nombre')
    autor = new_libro.get('autor')
    editorial = new_libro.get('editorial')
    imagen = new_libro.get('imagen')

    conn = db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO libro (codigo, nombre, autor, editorial, imagen) 
        VALUES (?, ?, ?, ?, ?)
    """, (codigo, nombre, autor, editorial, imagen))
    conn.commit()
    conn.close()

    return jsonify({"message": "Libro agregado con éxito"}), 201

@app.route('/libros/<string:codigo>', methods=['DELETE'])
def delete_libro(codigo):
    conn = db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM libro WHERE codigo = ?", (codigo,))
    conn.commit()
    conn.close()
    
    return jsonify({"message": f"Libro con código {codigo} eliminado"}), 200

@app.route('/libros/<string:codigo>', methods=['PUT'])
def update_libro(codigo):
    update_data = request.json
    nombre = update_data.get('nombre')
    autor = update_data.get('autor')
    editorial = update_data.get('editorial')
    imagen = update_data.get('imagen')

    conn = db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE libro 
        SET nombre = ?, autor = ?, editorial = ?, imagen = ?
        WHERE codigo = ?
    """, (nombre, autor, editorial, imagen, codigo))
    conn.commit()
    conn.close()

    return jsonify({"message": f"Libro con código {codigo} actualizado"}), 200

@app.route('/libros/<string:codigo>', methods=['GET'])
def get_libro_por_codigo(codigo):
    conn = db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM libro WHERE codigo = ?", (codigo,))
    libro = cursor.fetchone()
    conn.close()

    if libro:
        return jsonify(dict(libro)), 200
    else:
        return jsonify({"message": f"No se encontró un libro con el código {codigo}"}), 404

# Ejecutar el programa
if __name__ == "__main__":
    init_db()  # Crear base de datos y tablas al iniciar
    port = int(os.environ.get("PORT", 5000))  # Render asigna un puerto dinámico
    app.run(host="0.0.0.0", port=port)  # Flask escucha en 0.0.0.0