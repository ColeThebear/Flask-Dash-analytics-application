import os
from dotenv import load_dotenv
env = os.getenv("FLASK_ENV", "Dev")
load_dotenv(f"instance/Prod.env")

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "default_secret")
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    APP_VERSION = "1.0.0"
    DEPLOY_DATE = "2025-10-06"
    ENVIRONMENT = "development"
    @staticmethod
    def get_git_commit():
        return "unknown"
    
class DevelopmentConfig(Config):
    DEBUG = True

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.getenv("TEST_DATABASE_URL")

class ProductionConfig(Config):
    DEBUG = False

    @staticmethod
    def get_git_commit():
        try:
            import subprocess
            return subprocess.check_output(['git', 'rev-parse', '--short', 'HEAD']).decode().strip()
        except Exception:
            return "Unavailable"