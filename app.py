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

# Ejecutar el programa
if __name__ == "__main__":
    init_db()  # Crear base de datos y tablas al iniciar
    app.run(debug=True)
   

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)