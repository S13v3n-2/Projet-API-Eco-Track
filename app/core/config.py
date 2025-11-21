import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    PROJECT_NAME: str = "EcoTrack"
    VERSION: str = "1.0.0"

    # Chemin absolu vers le dossier data
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    DATA_DIR = os.path.join(BASE_DIR, "data")

    # Créer le dossier data s'il n'existe pas
    os.makedirs(DATA_DIR, exist_ok=True)

    # Chemin complet vers la base de données avec format correct pour Windows
    DB_FILE_PATH = os.path.join(DATA_DIR, "ecotrack.db").replace('\\', '/')
    DATABASE_URL: str = os.getenv("DATABASE_URL", f"sqlite:///{DB_FILE_PATH}")

    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-here-change-in-production")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    def __init__(self):
        print(f"📁 Dossier data: {self.DATA_DIR}")
        print(f"📄 Fichier DB: {self.DB_FILE_PATH}")
        print(f"🔗 URL DB: {self.DATABASE_URL}")


settings = Settings()