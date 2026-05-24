# Tienda Online - Documentación del Proyecto

## Descripción General
Sistema de tienda online desarrollado en Python con MongoDB. Implementa un CRUD completo para gestionar usuarios, productos, carrito de compras e historial de compras.

## Estructura del Proyecto

### Archivos Principales
- **`principal.py`** - Punto de entrada de la aplicación. Ejecutar con: `py principal.py`
- **`datos_iniciales.py`** - Carga productos de prueba. Ejecutar una sola vez: `py datos_iniciales.py`
- **`configuracion.py`** - Variables de configuración (URI de MongoDB, nombre de BD)
- **`base_datos.py`** - Conexión centralizada a MongoDB con índices
- **`utilidades.py`** - Funciones auxiliares para formatear información en consola

### Carpeta `repositorios/`
Capa de acceso a datos (Data Access Layer). Implementa CRUD para cada entidad:

- **`repositorio_usuario.py`** - Gestiona usuarios:
  - `crear()` - Crear nuevo usuario
  - `obtener_por_email()` - Buscar por email (login)
  - `obtener_por_id()` - Buscar por ID incremental
  - `actualizar()` - Modificar nombre o email
  - `eliminar()` - Borrar usuario
  - `guardar_carrito()` - Guardar estado del carrito
  - `agregar_compra()` - Agregar compra al historial
  - **`obtener_siguiente_id()`** - Genera IDs incrementales únicos (1, 2, 3...)

- **`repositorio_producto.py`** - Gestiona productos:
  - `crear()` - Crear nuevo producto
  - `obtener_por_id()` - Buscar por ID incremental
  - `listar_todos()` - Listar todos los productos activos
  - `buscar_por_categoria()` - Filtrar por categoría
  - `actualizar()` - Modificar producto
  - `eliminar()` - Baja lógica (marca como inactivo)
  - `descontar_stock()` - Reduce inventario de manera atómica
  - `listar_categorias()` - Obtener categorías disponibles
  - **`obtener_siguiente_id()`** - Genera IDs incrementales únicos (1, 2, 3...)

### Carpeta `servicios/`
Capa de lógica de negocio (Business Logic Layer). Orquesta las operaciones de repositorios:

- **`servicio_autenticacion.py`** - Gestiona autenticación:
  - `registrar()` - Registro de nuevo usuario
  - `iniciar_sesion()` - Login con validación de contraseña

- **`servicio_tienda.py`** - Gestiona operaciones de compra:
  - `listar_productos()` - Obtener todos los productos
  - `buscar_por_categoria()` - Buscar productos por categoría
  - `listar_categorias()` - Obtener categorías
  - `agregar_al_carrito()` - Agregar producto al carrito
  - `ver_carrito()` - Mostrar contenido del carrito
  - `vaciar_carrito()` - Limpiar el carrito
  - `realizar_compra()` - Procesar compra (valida stock, descuenta inventario)
  - `ver_historial()` - Historial de compras del usuario

## Sistema de IDs Incrementales

Cada usuario y producto obtiene un **ID numérico único e incremental** (1, 2, 3...) generado automáticamente:

### Cómo Funciona
1. Se mantiene una colección `contadores` en MongoDB
2. Al crear un usuario: se obtiene `usuarios_id` y se incrementa
3. Al crear un producto: se obtiene `productos_id` y se incrementa
4. Los contadores se crean automáticamente con `upsert=True` si no existen

### Beneficios
- IDs simples y amigables para el usuario
- Fácil de seguimiento y debugging
- Se mantiene el `_id` de MongoDB en paralelo para integridad referencial
- Búsquedas más rápidas por ID incremental que por ObjectId

## Funciones CRUD Implementadas (Requisitos del Proyecto)

### Usuarios
1. **CREATE** - Registrar nuevo usuario ✅
2. **READ** - Obtener usuario por email o ID ✅
3. **UPDATE** - Modificar nombre o email ✅
4. **DELETE** - Eliminar usuario ✅

### Productos
1. **CREATE** - Crear nuevo producto ✅
2. **READ** - Listar todos / buscar por categoría ✅
3. **UPDATE** - Modificar datos del producto ✅
4. **DELETE** - Baja lógica (marcar como inactivo) ✅

## Requisitos Funcionales Adicionales

- ✅ **Carrito de Compras** - Agregar/quitar productos, actualizar cantidades
- ✅ **Gestión de Inventario** - Descontar stock de manera atómica
- ✅ **Historial de Compras** - Registrar todas las compras del usuario
- ✅ **Búsqueda por Categoría** - Filtrar productos
- ✅ **Autenticación** - Contraseñas hasheadas con bcrypt

## Instalación

### 1. Crear entorno virtual
```bash
python -m venv venv
venv\Scripts\activate
```

### 2. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 3. Configurar variables de entorno
Crear archivo `.env` con:
```
MONGODB_URI=mongodb+srv://usuario:contraseña@host/
MONGODB_DB=tienda_online
```

### 4. Cargar datos iniciales
```bash
python datos_iniciales.py
```

### 5. Ejecutar la aplicación
```bash
python principal.py
```

## Modelos de Datos

### Usuario
```json
{
  "_id": ObjectId,
  "id": 1,
  "nombre": "Juan Pérez",
  "email": "juan@example.com",
  "hash_contraseña": "bcrypt_hash",
  "carrito": [],
  "historial_compras": [],
  "creado_en": "2024-01-01T12:00:00Z"
}
```

### Producto
```json
{
  "_id": ObjectId,
  "id": 1,
  "nombre": "Laptop HP 15",
  "descripcion": "Intel i5, 8GB RAM, 256GB SSD",
  "categoria": "electronica",
  "precio": 899.99,
  "stock": 10,
  "activo": true
}
```

### Compra (en historial)
```json
{
  "fecha": "2024-01-15T14:30:00Z",
  "items": [
    {
      "producto_id": 1,
      "nombre": "Laptop HP 15",
      "cantidad": 1,
      "precio_unitario": 899.99,
      "subtotal": 899.99
    }
  ],
  "total": 899.99,
  "estado": "completada"
}
```

## Notas de Seguridad

- ✅ Contraseñas hasheadas con bcrypt (nunca en texto plano)
- ✅ Email único por usuario
- ✅ Mensajes de error genéricos en autenticación (no revelan si email existe)
- ✅ Operaciones de stock atómicas (evita condiciones de carrera)
- ✅ Baja lógica en productos (preserva historial)

## Autor
Proyecto Final - Bases de Datos 2 (2026)
