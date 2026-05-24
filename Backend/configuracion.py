# Lee la configuración desde el archivo .env (no subir .env a Git).
import os

from dotenv import load_dotenv

load_dotenv()

# URI de conexión a MongoDB (local o Atlas).
URI_MONGODB = os.getenv("MONGODB_URI", "mongodb+srv://l14sfp_db_user:TIHPItkMdXMG2ir6@cluster0.onctzzm.mongodb.net/?appName=Cluster0")
# Nombre de la base de datos donde se guardan productos y usuarios.
NOMBRE_BD_MONGODB = os.getenv("MONGODB_DB", "tienda_online")
