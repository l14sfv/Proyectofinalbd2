# Conexión centralizada a MongoDB: un solo cliente reutilizable en toda la aplicación.
from pymongo import ASCENDING, MongoClient
from pymongo.database import Database

from Backend.configuracion import NOMBRE_BD_MONGODB, URI_MONGODB

# Cliente global de MongoDB.
_cliente: MongoClient | None = None


def obtener_cliente() -> MongoClient:
    """
    Obtiene el cliente de MongoDB (patrón singleton).
    Crea el cliente una sola vez para no abrir muchas conexiones simultáneas.
    """
    global _cliente
    if _cliente is None:
        # serverSelectionTimeoutMS: falla rápido si MongoDB no responde.
        _cliente = MongoClient(URI_MONGODB, serverSelectionTimeoutMS=5000)
    return _cliente


def obtener_bd() -> Database:
    """Devuelve la base de datos configurada (colecciones: productos, usuarios, contadores)."""
    return obtener_cliente()[NOMBRE_BD_MONGODB]


def inicializar_indices() -> None:
    """
    Crea índices para búsquedas rápidas y aplica reglas de negocio:
    - email único: no puede haber dos usuarios con el mismo correo.
    - categoría/nombre: aceleran listar y filtrar productos.
    """
    bd = obtener_bd()
    bd.usuarios.create_index([("email", ASCENDING)], unique=True)
    bd.productos.create_index([("categoria", ASCENDING)])
    bd.productos.create_index([("nombre", ASCENDING)])


def cerrar_conexion() -> None:
    """Cierra la conexión al salir del programa para liberar recursos."""
    global _cliente
    if _cliente is not None:
        _cliente.close()
        _cliente = None
