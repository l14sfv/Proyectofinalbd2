# Servicio de autenticación: Registro e inicio de sesión.
# Capa intermedia entre el menú y la base de datos de usuarios.
from Backend.repositorios.repositorio_usuario import RepositorioUsuario


class ServicioAutenticacion:
    """
    Gestiona el registro e inicio de sesión de usuarios.
    Valida credenciales y maneja errores de duplicados.
    """

    def __init__(self) -> None:
        self._usuarios = RepositorioUsuario()

    def registrar(self, nombre: str, email: str, contraseña: str) -> tuple[bool, str, dict | None]:
        """
        Registra un nuevo usuario en el sistema.
        Valida que la contraseña tenga longitud mínima.
        Valida que el email sea único en la base de datos.
        """
        if len(contraseña) < 4:
            return False, "La contraseña debe tener al menos 4 caracteres.", None
        if self._usuarios.obtener_por_email(email):
            return False, "Ya existe un usuario con ese correo.", None
        try:
            self._usuarios.crear(nombre, email, contraseña)
        except Exception as exc:
            # El índice único en email también puede lanzar error de duplicado.
            if "duplicate key" in str(exc).lower():
                return False, "Ya existe un usuario con ese correo.", None
            raise
        usuario = self._usuarios.obtener_por_email(email)
        return True, "Usuario registrado correctamente.", usuario

    def iniciar_sesion(self, email: str, contraseña: str) -> tuple[bool, str, dict | None]:
        """
        Inicia sesión de un usuario existente.
        Valida email y contraseña.
        No revela si el email existe o no por razones de seguridad.
        """
        usuario = self._usuarios.obtener_por_email(email)
        if not usuario:
            # Mismo mensaje si no existe o la contraseña falla (no revelar si el email existe).
            return False, "Correo o contraseña incorrectos.", None
        if not RepositorioUsuario.verificar_contraseña(contraseña, usuario["hash_contraseña"]):
            return False, "Correo o contraseña incorrectos.", None
        return True, f"Bienvenido, {usuario['nombre']}.", usuario
