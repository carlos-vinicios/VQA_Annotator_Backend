import os
from dotenv import load_dotenv

class EnvironmentVariables():
    
    def __init__(self, dotenv_path=".env"):
        
        load_dotenv(dotenv_path)

        self.REPORTS_PATH = os.environ.get("REPORTS_PATH", "data")
        self.SECRET_KEY = os.environ.get("SECRET_KEY", "")
        self.ALGORITHM = os.environ.get("ALGORITHM", "HS256")
        self.ACCESS_TOKEN_EXPIRE_MINUTES = os.environ.get("ACCESS_TOKEN_EXPIRE_MINUTES", 30)
        self.MONGODB_URI = os.environ.get("MONGODB_URI", "")