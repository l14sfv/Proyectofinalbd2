# Servicio de tienda: Lógica de carrito y compras.
# Gestiona agregar productos al carrito, checkout y historial de compras.
from datetime import datetime, timezone

from Backend.repositorios.repositorio_producto import RepositorioProducto
from Backend.repositorios.repositorio_usuario import RepositorioUsuario


class ServicioTienda:
    """
    Gestiona las operaciones de compra: carrito, transacciones e inventario.
    Valida stock y coordina la actualización de la base de datos.
    """

    def __init__(self) -> None:
        self._productos = RepositorioProducto()
        self._usuarios = RepositorioUsuario()

    def listar_productos(self) -> list[dict]:
        """Devuelve todos los productos disponibles en la tienda."""
        return self._productos.listar_todos()

    def buscar_por_categoria(self, categoria: str) -> list[dict]:
        """Busca y devuelve productos de una categoría específica."""
        return self._productos.buscar_por_categoria(categoria)

    def listar_categorias(self) -> list[str]:
        """Devuelve todas las categorías de productos disponibles."""
        return self._productos.listar_categorias()

    def agregar_al_carrito(
        self, usuario: dict, producto_id: str, cantidad: int
    ) -> tuple[bool, str]:
        """
        Agrega un producto al carrito del usuario.
        Valida que el producto exista y que haya stock suficiente.
        Si el producto ya está en el carrito, suma la cantidad.
        """
        if cantidad < 1:
            return False, "La cantidad debe ser al menos 1."

        producto = self._productos.obtener_por_id(producto_id)
        if not producto:
            return False, "Producto no encontrado."

        # Gestión de inventario: no agregar si no hay stock.
        if producto["stock"] < cantidad:
            return False, f"Stock insuficiente. Disponible: {producto['stock']}."

        carrito = list(usuario.get("carrito", []))
        pid = str(producto["id"])  # Usar el id incremental

        # Si el producto ya está en el carrito, sumamos cantidad en lugar de duplicar.
        for item in carrito:
            if item["producto_id"] == pid:
                nueva_cantidad = item["cantidad"] + cantidad
                if nueva_cantidad > producto["stock"]:
                    return (
                        False,
                        f"No puedes agregar más. Stock disponible: {producto['stock']}.",
                    )
                item["cantidad"] = nueva_cantidad
                item["subtotal"] = round(item["cantidad"] * item["precio_unitario"], 2)
                self._usuarios.guardar_carrito(usuario["_id"], carrito)
                usuario["carrito"] = carrito  # mantener sincronizado el dict en memoria
                return True, "Cantidad actualizada en el carrito."

        carrito.append(
            {
                "producto_id": pid,
                "nombre": producto["nombre"],
                "categoria": producto["categoria"],
                "precio_unitario": producto["precio"],
                "cantidad": cantidad,
                "subtotal": round(cantidad * producto["precio"], 2),
            }
        )
        self._usuarios.guardar_carrito(usuario["_id"], carrito)
        usuario["carrito"] = carrito
        return True, "Producto agregado al carrito."

    def ver_carrito(self, usuario: dict) -> list[dict]:
        """Devuelve el contenido actual del carrito del usuario."""
        return usuario.get("carrito", [])

    def vaciar_carrito(self, usuario: dict) -> None:
        """Limpia todos los ítems del carrito del usuario."""
        self._usuarios.guardar_carrito(usuario["_id"], [])
        usuario["carrito"] = []

    def realizar_compra(self, usuario: dict) -> tuple[bool, str, dict | None]:
        """
        Procesa la compra completa: valida stock, descuenta inventario y registra la compra.
        Usa dos pasadas: primero valida, luego descuenta (para evitar estados inconsistentes).
        """
        carrito = usuario.get("carrito", [])
        if not carrito:
            return False, "El carrito está vacío.", None

        # Primera pasada: validar stock antes de descontar nada.
        for item in carrito:
            producto = self._productos.obtener_por_id(item["producto_id"])
            if not producto:
                return False, f"Producto '{item['nombre']}' ya no está disponible.", None
            if producto["stock"] < item["cantidad"]:
                return (
                    False,
                    f"Stock insuficiente para '{item['nombre']}'. "
                    f"Disponible: {producto['stock']}, solicitado: {item['cantidad']}.",
                )

        # Segunda pasada: descontar inventario y registrar la compra.
        items_comprados = []
        for item in carrito:
            ok = self._productos.descontar_stock(item["producto_id"], item["cantidad"])
            if not ok:
                return (
                    False,
                    f"No se pudo completar la compra: stock agotado para '{item['nombre']}'.",
                    None,
                )
            items_comprados.append(
                {
                    "producto_id": item["producto_id"],
                    "nombre": item["nombre"],
                    "cantidad": item["cantidad"],
                    "precio_unitario": item["precio_unitario"],
                    "subtotal": item["subtotal"],
                }
            )

        total = round(sum(i["subtotal"] for i in items_comprados), 2)
        compra = {
            "fecha": datetime.now(timezone.utc),
            "items": items_comprados,
            "total": total,
            "estado": "completada",
        }
        self._usuarios.agregar_compra(usuario["_id"], compra)
        self.vaciar_carrito(usuario)

        # Recargar desde BD para tener historial y carrito actualizados.
        usuario_actualizado = self._usuarios.obtener_por_id(usuario["_id"])
        if usuario_actualizado:
            usuario.update(usuario_actualizado)

        return True, f"Compra realizada. Total: ${total:.2f}", compra

    def ver_historial(self, usuario: dict) -> list[dict]:
        """Devuelve el historial de compras del usuario."""
        return usuario.get("historial_compras", [])
