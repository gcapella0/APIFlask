import psycopg2
from flask import Flask, jsonify, request

app = Flask(__name__)

#-----Conecto la BD
def conectar_bd():
    return psycopg2.connect(
        host="Localhost",
        database="PruebaAPI",
        user="test",
        password=""
    )

#-----Obtener productos
@app.route('/api/productos', methods=['GET'])
def obtener_productos():
    try:
        #Conectar a la base de datos
        conexion = conectar_bd()
        cursor = conexion.cursor()

        #Consultar todos los productos
        cursor.execute("SELECT * FROM productos")
        productos = cursor.fetchall()

        #Cerrar la conexión a la base de datos
        cursor.close()
        conexion.close()

        #Convertir los resultados en formato JSON
        return jsonify(productos)

    except (Exception, psycopg2.Error) as error:
        #En caso de errores
        print("Error al obtener los productos:", error)
        return jsonify({"error": "Error al obtener los productos"}), 500
    

#-----Agregar productos
@app.route('/api/productos', methods=['POST'])
def agregar_producto():
    try:
        #Obtener los datos del producto
        data = request.get_json()
        nombre = data['nombre']
        precio = data['precio']

        #Conectar a la base de datos
        conexion = conectar_bd()
        cursor = conexion.cursor()

        #Insertar el nuevo producto en la base de datos
        cursor.execute("INSERT INTO productos (nombre, precio) VALUES (%s, %s)", (nombre, precio))
        conexion.commit()

        #Cerrar la conexión a la base de datos
        cursor.close()
        conexion.close()

        return jsonify({"mensaje": "Producto agregado exitosamente"}), 201

    except (Exception, psycopg2.Error) as error:
        #En caso de errores
        print("Error al agregar el producto:", error)
        return jsonify({"error": "Error al agregar el producto"}), 500
    
#-----Actualizar un producto
@app.route('/api/productos/<int:id>', methods=['PUT'])
def actualizar_producto(id):
    try:
        #Obtener los datos del producto
        data = request.get_json()
        nombre = data['nombre']
        precio = data['precio']

        #Conectar a la base de datos
        conexion = conectar_bd()
        cursor = conexion.cursor()

        #Actualizar el producto en la base de datos
        cursor.execute("UPDATE productos SET nombre = %s, precio = %s WHERE id = %s", (nombre, precio, id))
        conexion.commit()

        #Cerrar la conexión a la base de datos
        cursor.close()
        conexion.close()

        return jsonify({"mensaje": "Producto actualizado exitosamente"}), 200

    except (Exception, psycopg2.Error) as error:
        #En caso de errores
        print("Error al actualizar el producto:", error)
        return jsonify({"error": "Error al actualizar el producto"}), 500
    
#-----Eliminar un producto
@app.route('/api/productos/<int:id>', methods=['DELETE'])
def eliminar_producto(id):
    try:
        #Conectar a la base de datos
        conexion = conectar_bd()
        cursor = conexion.cursor()

        #Eliminar el producto de la base de datos
        cursor.execute("DELETE FROM productos WHERE id = %s", (id,))
        conexion.commit()

        #Cerrar la conexión a la base de datos
        cursor.close()
        conexion.close()

        return jsonify({"mensaje": "Producto eliminado exitosamente"}), 200

    except (Exception, psycopg2.Error) as error:
        #En caso de errores
        print("Error al eliminar el producto:", error)
        return jsonify({"error": "Error al eliminar el producto"}), 500




if __name__ == '__main__':
    app.run(debug=True)
