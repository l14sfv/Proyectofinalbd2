# Punto de entrada: menú en consola para usar la tienda online.
from Backend.base_datos import cerrar_conexion, inicializar_indices
from Backend.servicios.servicio_autenticacion import ServicioAutenticacion
from Backend.servicios.servicio_tienda import ServicioTienda
from Backend.utilidades import formatear_carrito, formatear_lista_productos, leer_entero


def pausa() -> None:
    """Pausa la ejecución esperando que el usuario presione Enter."""
    input("\nPresione Enter para continuar...")


def menu_autenticacion(autenticacion: ServicioAutenticacion) -> dict | None:
    """
    Menú de autenticación: Registro o inicio de sesión.
    Devuelve el documento del usuario o None para salir.
    """
    print("\n=== Autenticación ===")
    print("1. Iniciar sesión")
    print("2. Registrarse")
    print("0. Salir")
    opcion = input("Opción: ").strip()

    if opcion == "0":
        return None
    if opcion == "1":
        email = input("Correo: ").strip()
        contraseña = input("Contraseña: ").strip()
        ok, msg, usuario = autenticacion.iniciar_sesion(email, contraseña)
        print(msg)
        return usuario if ok else None
    if opcion == "2":
        nombre = input("Nombre: ").strip()
        email = input("Correo: ").strip()
        contraseña = input("Contraseña: ").strip()
        ok, msg, usuario = autenticacion.registrar(nombre, email, contraseña)
        print(msg)
        return usuario if ok else None
    print("Opción no válida.")
    return None


def menu_tienda(tienda: ServicioTienda, usuario: dict) -> None:
    """
    Menú principal de la tienda con las funciones del CRUD del proyecto:
    1. Ver todos los productos
    2. Buscar productos por categoría
    3. Agregar producto al carrito
    4. Ver contenido del carrito
    5. Realizar compra
    Además: historial de compras y cerrar sesión.
    """
    while True:
        print(f"\n=== Tienda Online | {usuario['nombre']} ===")
        print("1. Ver todos los productos")
        print("2. Buscar productos por categoría")
        print("3. Agregar producto al carrito")
        print("4. Ver contenido del carrito")
        print("5. Realizar compra")
        print("6. Ver historial de compras")
        print("7. Cerrar sesión")
        print("0. Salir")
        opcion = input("Opción: ").strip()

        if opcion == "0":
            return
        if opcion == "7":
            print("Sesión cerrada.")
            return

        if opcion == "1":
            productos = tienda.listar_productos()
            print(f"\n--- Productos disponibles ({len(productos)}) ---")
            print(formatear_lista_productos(productos))

        elif opcion == "2":
            categorias = tienda.listar_categorias()
            if not categorias:
                print("No hay categorías registradas.")
            else:
                print("Categorías:", ", ".join(categorias))
                cat = input("Ingrese categoría: ").strip()
                productos = tienda.buscar_por_categoria(cat)
                print(f"\n--- Productos en '{cat}' ({len(productos)}) ---")
                print(formatear_lista_productos(productos))

        elif opcion == "3":
            productos = tienda.listar_productos()
            if not productos:
                print("No hay productos disponibles.")
            else:
                print(formatear_lista_productos(productos))
                producto_id = input("\nID del producto: ").strip()
                cantidad = leer_entero("Cantidad: ", minimo=1)
                ok, msg = tienda.agregar_al_carrito(usuario, producto_id, cantidad)
                print(msg)

        elif opcion == "4":
            carrito = tienda.ver_carrito(usuario)
            print("\n--- Tu carrito ---")
            print(formatear_carrito(carrito))

        elif opcion == "5":
            print("\n--- Resumen antes de comprar ---")
            print(formatear_carrito(tienda.ver_carrito(usuario)))
            confirmar = input("¿Confirmar compra? (s/n): ").strip().lower()
            if confirmar == "s":
                ok, msg, compra = tienda.realizar_compra(usuario)
                print(msg)
                if ok and compra:
                    print(f"  Artículos: {len(compra['items'])}")
            else:
                print("Compra cancelada.")

        elif opcion == "6":
            historial = tienda.ver_historial(usuario)
            if not historial:
                print("\nNo tienes compras registradas.")
            else:
                print(f"\n--- Historial de compras ({len(historial)}) ---")
                for i, compra in enumerate(historial, 1):
                    print(f"\n[{i}] Compra del {compra['fecha'].strftime('%d/%m/%Y %H:%M')}")
                    for item in compra["items"]:
                        print(f"    - {item['nombre']} x{item['cantidad']} @ ${item['precio_unitario']:.2f}")
                    print(f"    Total: ${compra['total']:.2f}")


def main() -> None:
    """Función principal: Inicializa la aplicación y ejecuta el menú principal."""
    try:
        inicializar_indices()
        autenticacion = ServicioAutenticacion()
        tienda = ServicioTienda()

        print("\n╔════════════════════════════════════════╗")
        print("║      Bienvenido a la Tienda Online     ║")
        print("╚════════════════════════════════════════╝")

        while True:
            usuario = menu_autenticacion(autenticacion)
            if usuario is None:
                print("\nHasta luego.")
                break
            menu_tienda(tienda, usuario)

    except Exception as exc:
        print(f"Error: {exc}")
    finally:
        cerrar_conexion()


if __name__ == "__main__":
    main()
