from flask import Flask, jsonify, request
from flask_cors import CORS
from bson import ObjectId
from Backend.servicios.servicio_tienda import ServicioTienda

app = Flask(__name__)
CORS(app)  # Permite que el Frontend hable con Python de forma local

# Inicializamos el servicio de la tienda
servicio = ServicioTienda()

# Creamos un usuario de sesión local temporal para manejar el carrito
usuario_sesion = {
    "_id": ObjectId(),  # Genera un ID válido de Mongo
    "usuario": "yaha_cliente",
    "nombre": "Yaha",
    "carrito": [],
    "historial_compras": []
}

@app.route('/api/productos', methods=['GET'])
def listar_productos():
    try:
        productos = servicio.listar_productos()
        for p in productos:
            p['_id'] = str(p['_id'])  # Convertimos el ObjectId a texto
        return jsonify(productos), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/categorias', methods=['GET'])
def obtener_categorias():
    try:
        categorias = servicio.listar_categorias()
        return jsonify(categorias), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/productos/categoria/<cat>', methods=['GET'])
def filtrar_por_categoria(cat):
    try:
        productos = servicio.buscar_por_categoria(cat)
        for p in productos:
            p['_id'] = str(p['_id'])
        return jsonify(productos), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/carrito', methods=['GET'])
def ver_carrito():
    try:
        items = servicio.ver_carrito(usuario_sesion)
        return jsonify(items), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/carrito/agregar', methods=['POST'])
def agregar_al_carrito():
    try:
        data = request.json
        prod_id = str(data.get("producto_id"))
        cantidad = int(data.get("cantidad", 1))
        
        exito, mensaje = servicio.agregar_al_carrito(usuario_sesion, prod_id, cantidad)
        return jsonify({"exito": exito, "mensaje": mensaje, "carrito": usuario_sesion["carrito"]}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/carrito/comprar', methods=['POST'])
def procesar_compra():
    try:
        exito, mensaje, compra = servicio.realizar_compra(usuario_sesion)
        return jsonify({"exito": exito, "mensaje": mensaje}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    print(" Servidor de la Tienda corriendo en http://127.0.0.1:5000")
    app.run(debug=True, port=5000)