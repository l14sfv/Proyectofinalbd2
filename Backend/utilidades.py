# Funciones auxiliares para mostrar información en la consola (sin lógica de negocio).


def formatear_producto(producto: dict) -> str:
    """Convierte un documento de producto en texto legible para el usuario."""
    return (
        f"  ID: {producto['id']}\n"
        f"  Nombre: {producto['nombre']}\n"
        f"  Categoría: {producto['categoria']}\n"
        f"  Precio: ${producto['precio']:.2f}\n"
        f"  Stock: {producto['stock']}\n"
        f"  {producto.get('descripcion', '')}"
    )


def formatear_lista_productos(productos: list[dict]) -> str:
    """Formatea una lista de productos para mostrar en la consola."""
    if not productos:
        return "  (No hay productos para mostrar)"
    lineas = []
    for i, p in enumerate(productos, 1):
        lineas.append(f"\n[{i}] {formatear_producto(p)}")
    return "".join(lineas)


def formatear_carrito(carrito: list[dict]) -> str:
    """Muestra ítems del carrito y calcula el total a pagar."""
    if not carrito:
        return "  El carrito está vacío."
    lineas = []
    total = 0.0
    for i, item in enumerate(carrito, 1):
        lineas.append(
            f"\n[{i}] {item['nombre']} x{item['cantidad']} "
            f"@ ${item['precio_unitario']:.2f} = ${item['subtotal']:.2f}"
        )
        total += item["subtotal"]
    lineas.append(f"\n  TOTAL: ${total:.2f}")
    return "".join(lineas)


def leer_entero(mensaje: str, minimo: int | None = None) -> int:
    """
    Lee un número entero desde la consola.
    Valida que el entrada sea un número entero válido.
    """
    while True:
        try:
            valor = int(input(mensaje))
            if minimo is not None and valor < minimo:
                print(f"Ingrese un número mayor o igual a {minimo}.")
                continue
            return valor
        except ValueError:
            print("Ingrese un número válido.")
