# CRUD de la colección "usuarios" (login, carrito e historial por persona).
# Cada usuario guarda en un solo documento:
# - datos de cuenta (nombre, email, contraseña hasheada)
# - carrito: lista de productos pendientes de comprar
# - historial_compras: compras ya realizadas
from datetime import datetime, timezone

import bcrypt
from bson import ObjectId
from pymongo.collection import Collection
from pymongo import ReturnDocument

from Backend.base_datos import obtener_bd


class RepositorioUsuario:
    """
    Gestiona todas las operaciones CRUD de usuarios en MongoDB.
    Maneja autenticación, carrito e historial de compras.
    """

    def __init__(self) -> None:
        self._coleccion: Collection = obtener_bd().usuarios

    @staticmethod
    def _hash_contraseña(contraseña: str) -> str:
        """
        Cifra la contraseña usando bcrypt.
        Nunca guardamos la contraseña en texto plano.
        """
        return bcrypt.hashpw(contraseña.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

    @staticmethod
    def verificar_contraseña(contraseña: str, hash_contraseña: str) -> bool:
        """Verifica si la contraseña ingresada coincide con el hash almacenado."""
        return bcrypt.checkpw(contraseña.encode("utf-8"), hash_contraseña.encode("utf-8"))

    def obtener_siguiente_id(self) -> int:
        """
        Obtiene el próximo ID incremental para un usuario nuevo.
        Implementa autoincremento: 1, 2, 3, 4...
        """
        contadores = obtener_bd()["contadores"]
        resultado = contadores.find_one_and_update(
            {"_id": "usuarios_id"},        # documento único del contador para usuarios
            {"$inc": {"seq": 1}},          # suma 1 al campo seq
            upsert=True,                   # crea el documento si aún no existe
            return_document=ReturnDocument.AFTER  # devuelve el documento ya actualizado
        )
        return resultado["seq"]

    def crear(self, nombre: str, email: str, contraseña: str) -> ObjectId:
        """
        CREATE: Inserta un nuevo usuario en la base de datos.
        Inicializa el carrito e historial como listas vacías.
        """
        documento = {
            "id": self.obtener_siguiente_id(),  # ID incremental único
            "nombre": nombre.strip(),
            "email": email.strip().lower(),
            "hash_contraseña": self._hash_contraseña(contraseña),
            "carrito": [],
            "historial_compras": [],
            "creado_en": datetime.now(timezone.utc),
        }
        resultado = self._coleccion.insert_one(documento)
        return resultado.inserted_id

    def obtener_por_email(self, email: str) -> dict | None:
        """
        READ: Busca un usuario por su correo electrónico.
        Se usa durante el inicio de sesión.
        """
        return self._coleccion.find_one({"email": email.strip().lower()})

    def obtener_por_id(self, usuario_id: ObjectId | str) -> dict | None:
        """
        READ: Obtiene un usuario por su ID incremental.
        Se usa para recargar datos de usuario tras una compra.
        """
        try:
            usuario_id_int = int(usuario_id)
            return self._coleccion.find_one({"id": usuario_id_int})
        except (ValueError, TypeError):
            return None

    def actualizar(self, usuario_id: ObjectId | str, datos: dict) -> bool:
        """
        UPDATE: Modifica nombre o email del usuario (CRUD del proyecto).
        Solo permite cambiar ciertos campos por seguridad.
        """
        campos = {k: v for k, v in datos.items() if k in ("nombre", "email")}
        if not campos:
            return False
        if "email" in campos:
            campos["email"] = campos["email"].strip().lower()
        resultado = self._coleccion.update_one({"_id": ObjectId(usuario_id)}, {"$set": campos})
        return resultado.matched_count > 0

    def eliminar(self, usuario_id: ObjectId | str) -> bool:
        """
        DELETE: Borra el documento del usuario de la base de datos.
        Operación del CRUD del proyecto.
        """
        resultado = self._coleccion.delete_one({"_id": ObjectId(usuario_id)})
        return resultado.deleted_count > 0

    def guardar_carrito(self, usuario_id: ObjectId | str, carrito: list) -> None:
        """
        Guarda el carrito del usuario en la base de datos.
        Cada usuario tiene su propio carrito almacenado como array.
        """
        self._coleccion.update_one(
            {"_id": ObjectId(usuario_id)},
            {"$set": {"carrito": carrito}},
        )

    def agregar_compra(self, usuario_id: ObjectId | str, compra: dict) -> None:
        """
        Agrega una compra al historial del usuario.
        Usa $push para agregar sin borrar compras anteriores.
        """
        self._coleccion.update_one(
            {"_id": ObjectId(usuario_id)},
            {"$push": {"historial_compras": compra}},
        )
