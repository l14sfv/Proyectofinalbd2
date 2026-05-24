# CRUD de la colección "productos" (inventario de la tienda).
# Cada producto en MongoDB tiene:
# - nombre, descripción, categoría, precio, stock, activo.
# - activo=False es "eliminar" sin borrar el documento (baja lógica).
from bson import ObjectId
from pymongo.collection import Collection
from pymongo import ReturnDocument

from Backend.base_datos import obtener_bd


class RepositorioProducto:
    """
    Gestiona todas las operaciones CRUD de productos en MongoDB.
    Implementa inventario, búsqueda y categorización de productos.
    Usa "baja lógica" en lugar de eliminar documentos físicamente.
    """

    def __init__(self) -> None:
        self._coleccion: Collection = obtener_bd().productos

    def obtener_siguiente_id(self) -> int:
        """
        Obtiene el próximo ID incremental para un producto nuevo.
        Implementa autoincremento: 1, 2, 3, 4...
        """
        contadores = obtener_bd()["contadores"]
        resultado = contadores.find_one_and_update(
            {"_id": "productos_id"},       # documento único del contador para productos
            {"$inc": {"seq": 1}},          # suma 1 al campo seq
            upsert=True,                   # crea el documento si aún no existe
            return_document=ReturnDocument.AFTER  # devuelve el documento ya actualizado
        )
        return resultado["seq"]

    def crear(self, datos: dict) -> ObjectId:
        """
        CREATE: Inserta un nuevo producto en la base de datos.
        Valida y normaliza los datos antes de guardar.
        """
        documento = {
            "id": self.obtener_siguiente_id(),  # ID incremental único
            "nombre": datos["nombre"],
            "descripcion": datos.get("descripcion", ""),
            "categoria": datos["categoria"].strip().lower(),  # normalizar búsquedas
            "precio": float(datos["precio"]),
            "stock": int(datos["stock"]),
            "activo": datos.get("activo", True),
        }
        resultado = self._coleccion.insert_one(documento)
        return resultado.inserted_id

    def obtener_por_id(self, producto_id: ObjectId | str) -> dict | None:
        """
        READ: Busca un producto por su ID incremental (solo si está activo).
        Los productos inactivos no se muestran.
        """
        try:
            producto_id_int = int(producto_id)
            return self._coleccion.find_one({"id": producto_id_int, "activo": True})
        except (ValueError, TypeError):
            return None

    def listar_todos(self) -> list[dict]:
        """
        READ: Devuelve el catálogo completo ordenado por nombre.
        Solo muestra productos activos.
        """
        return list(self._coleccion.find({"activo": True}).sort("nombre", 1))

    def buscar_por_categoria(self, categoria: str) -> list[dict]:
        """
        READ: Filtra productos por categoría (requisito del proyecto).
        Solo muestra productos activos y los ordena por nombre.
        """
        return list(
            self._coleccion.find(
                {"categoria": categoria.strip().lower(), "activo": True}
            ).sort("nombre", 1)
        )

    def actualizar(self, producto_id: ObjectId | str, datos: dict) -> bool:
        """
        UPDATE: Modifica solo los campos especificados del producto.
        Valida tipos de datos antes de actualizar.
        """
        oid = ObjectId(producto_id)
        campos = {}
        for clave in ("nombre", "descripcion", "categoria", "precio", "stock", "activo"):
            if clave in datos:
                valor = datos[clave]
                if clave == "categoria":
                    valor = str(valor).strip().lower()
                elif clave == "precio":
                    valor = float(valor)
                elif clave == "stock":
                    valor = int(valor)
                campos[clave] = valor
        if not campos:
            return False
        resultado = self._coleccion.update_one({"_id": oid}, {"$set": campos})
        return resultado.matched_count > 0

    def eliminar(self, producto_id: ObjectId | str) -> bool:
        """
        DELETE lógico: Marca el producto como inactivo sin borrarlo físicamente.
        Esto preserva el historial de compras que referencia este producto.
        """
        resultado = self._coleccion.update_one(
            {"_id": ObjectId(producto_id)},
            {"$set": {"activo": False}},
        )
        return resultado.matched_count > 0

    def descontar_stock(self, producto_id: ObjectId | str, cantidad: int) -> bool:
        """
        Resta stock de manera atómica.
        Solo descuenta si hay suficiente stock disponible.
        Evita condiciones de carrera en compras simultáneas.
        """
        resultado = self._coleccion.update_one(
            {"id": int(producto_id), "stock": {"$gte": cantidad}, "activo": True},
            {"$inc": {"stock": -cantidad}},
        )
        return resultado.modified_count > 0

    def listar_categorias(self) -> list[str]:
        """
        Lista todas las categorías distintas de productos activos.
        Se usa para ayudar al usuario a filtrar productos.
        """
        return self._coleccion.distinct("categoria", {"activo": True})
