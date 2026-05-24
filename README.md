# TiendaMongoDB - Proyectofinalbd2

Aplicación de tienda online desarrollada con **Python** y **MongoDB**. Sistema completo de gestión de usuarios, productos, carrito de compras e historial de compras con autenticación y control de inventario.

## Descripción del Proyecto

Sistema de tienda online que implementa un **CRUD completo** con arquitectura en capas:

- **Capa de Acceso a Datos** (Repositorios)
- **Capa de Lógica de Negocio** (Servicios)
- **Interfaz de Usuario** (Menú en consola y Frontend web)

##  Estructura del Proyecto

```
Proyectofinalbd2/
├── Backend/                          # API y lógica del servidor
│   ├── app_api.py                   # API REST (si aplica)
│   ├── base_datos.py                # Conexión a MongoDB e índices
│   ├── configuracion.py             # Variables de configuración
│   ├── main.py                      # Punto de entrada principal
│   ├── utilidades.py                # Funciones auxiliares
│   ├── requirements.txt             # Dependencias Python
│   ├── repositorios/                # Capa de Acceso a Datos
│   │   ├── __init__.py
│   │   ├── repositorio_usuario.py   # CRUD de usuarios
│   │   └── repositorio_producto.py  # CRUD de productos
│   ├── servicios/                   # Capa de Lógica de Negocio
│   │   ├── __init__.py
│   │   ├── servicio_autenticacion.py # Autenticación y registro
│   │   └── servicio_tienda.py       # Lógica de compra y carrito
│   └── README.md                    # Documentación del Backend
│
└── Frontend/                         # Interfaz web
    ├── index.html                   # Página principal
    ├── app.js                       # Lógica del cliente
    └── style.css                    # Estilos
```

##  Requisitos Previos

- **Python 3.8+**
- **MongoDB** (local o remoto)
- **Node.js** (opcional, para servidor Frontend)

##  Instalación

### 1. Clonar el Repositorio

```bash
git clone https://github.com/tuusuario/Proyectofinalbd2.git
cd Proyectofinalbd2
```

### 2. Configurar Backend

```bash
cd Backend

# Crear entorno virtual
python -m venv venv

# Activar entorno virtual
# En Windows:
venv\Scripts\activate
# En Linux/Mac:
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt
```

### 3. Configurar Variables de Entorno

Crear archivo `.env` en la carpeta `Backend/`:

```env
MONGODB_URI=mongodb://localhost:27017
DATABASE_NAME=tienda_db
```

##  Uso

### Ejecutar la Aplicación Principal (Backend)

```bash
cd Backend
python main.py
```

Se abrirá un menú interactivo en consola donde podrás:

1. **Registrarse** o **Iniciar sesión**
2. Ver productos disponibles
3. Buscar por categoría
4. Agregar productos al carrito
5. Realizar compras

### Acceder al Frontend

```bash
cd Frontend
# Abrir index.html en tu navegador
```

##  Características Principales

### Autenticación

-  Registro de nuevos usuarios
-  Inicio de sesión con contraseña encriptada (bcrypt)
-  Validación de credenciales

### Gestión de Productos

-  Listar todos los productos
-  Buscar por categoría
-  Control de inventario (stock)
-  Baja lógica de productos

### Carrito de Compras

-  Agregar/remover productos
-  Cálculo de total
-  Persistencia del carrito

### Historial de Compras

-  Registro de transacciones
-  Consulta de historial por usuario

##  Tecnologías Utilizadas

| Componente           | Tecnología              |
| -------------------- | ----------------------- |
| Backend              | Python 3                |
| Base de Datos        | MongoDB                 |
| Autenticación        | bcrypt                  |
| Variables de Entorno | python-dotenv           |
| Frontend             | HTML5, CSS3, JavaScript |

### Dependencias Python

```
pymongo>=4.6.0     # Driver de MongoDB
bcrypt>=4.1.0      # Encriptación de contraseñas
python-dotenv>=1.0.0  # Gestión de variables de entorno
```

##  Licencia

Este proyecto es parte de un trabajo académico para la asignatura de Bases de Datos II.

##  Autor

Yaharys Bejarano
Luis Forero
Universidad: Universidad de La Salle
Fecha: Mayo 2026

**Nota**: Asegúrate de tener MongoDB en ejecución antes de iniciar la aplicación.
