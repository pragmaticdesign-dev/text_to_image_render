import os
from dotenv import load_dotenv
from pydantic import BaseModel

# Load .env file if present
load_dotenv()

class Settings(BaseModel):
    """
    Application Configuration
    """
    PROJECT_NAME: str = "Render Engine"
    API_V1_STR: str = "/api/v1"
    
    # Browser Config
    BROWSER_TIMEOUT_MS: int = 30000  # 30 seconds
    
    # Security (If you need basic auth later)
    API_KEY: str = os.getenv("API_KEY", "")

# Singleton instance
settings = Settings()