from pydantic import BaseSettings, Field
from typing import List
import os

class APISettings(BaseSettings):
    """API configuration settings"""
    
    # API Basic Settings
    API_TITLE: str = Field(default="Media Monitoring Knowledge Assistant API", description="API title")
    API_VERSION: str = Field(default="1.0.0", description="API version")
    API_DESCRIPTION: str = Field(
        default="A comprehensive API for media monitoring and knowledge management using vector search capabilities",
        description="API description"
    )
    
    # Server Settings
    HOST: str = Field(default="0.0.0.0", description="Server host")
    PORT: int = Field(default=8000, description="Server port")
    DEBUG: bool = Field(default=False, description="Debug mode")
    RELOAD: bool = Field(default=True, description="Auto-reload on code changes")
    
    # CORS Settings
    CORS_ORIGINS: List[str] = Field(
        default=["*"], 
        description="Allowed CORS origins"
    )
    CORS_ALLOW_CREDENTIALS: bool = Field(default=True, description="Allow CORS credentials")
    CORS_ALLOW_METHODS: List[str] = Field(
        default=["*"], 
        description="Allowed CORS methods"
    )
    CORS_ALLOW_HEADERS: List[str] = Field(
        default=["*"], 
        description="Allowed CORS headers"
    )
    
    # File Upload Settings
    MAX_FILE_SIZE: int = Field(
        default=50 * 1024 * 1024,  # 50MB
        description="Maximum file size in bytes"
    )
    ALLOWED_FILE_TYPES: List[str] = Field(
        default=[
            ".pdf", ".doc", ".docx", ".txt", ".rtf", 
            ".md", ".html", ".xml", ".json"
        ],
        description="Allowed file extensions"
    )
    TEMP_DIR: str = Field(
        default="temp",
        description="Temporary directory for file uploads"
    )
    
    # Search Settings
    DEFAULT_TOP_K: int = Field(default=5, description="Default number of search results")
    MAX_TOP_K: int = Field(default=50, description="Maximum number of search results")
    MIN_QUERY_LENGTH: int = Field(default=1, description="Minimum query length")
    MAX_QUERY_LENGTH: int = Field(default=1000, description="Maximum query length")
    
    # Rate Limiting (for future implementation)
    RATE_LIMIT_ENABLED: bool = Field(default=False, description="Enable rate limiting")
    RATE_LIMIT_REQUESTS: int = Field(default=100, description="Requests per minute")
    RATE_LIMIT_WINDOW: int = Field(default=60, description="Rate limit window in seconds")
    
    # Authentication (for future implementation)
    AUTH_ENABLED: bool = Field(default=False, description="Enable authentication")
    JWT_SECRET_KEY: str = Field(default="", description="JWT secret key")
    JWT_ALGORITHM: str = Field(default="HS256", description="JWT algorithm")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(default=30, description="Access token expiry")
    
    # Logging Settings
    LOG_LEVEL: str = Field(default="INFO", description="Logging level")
    LOG_FORMAT: str = Field(
        default="json", 
        description="Log format (json or text)"
    )
    
    # Monitoring Settings
    METRICS_ENABLED: bool = Field(default=False, description="Enable metrics collection")
    HEALTH_CHECK_INTERVAL: int = Field(
        default=30, 
        description="Health check interval in seconds"
    )
    
    # Contact Information
    CONTACT_NAME: str = Field(default="Media Monitoring Team", description="Contact name")
    CONTACT_EMAIL: str = Field(default="support@mediamonitoring.com", description="Contact email")
    
    # License Information
    LICENSE_NAME: str = Field(default="MIT", description="License name")
    LICENSE_URL: str = Field(
        default="https://opensource.org/licenses/MIT", 
        description="License URL"
    )
    
    class Config:
        env_file = ".env"
        env_prefix = "API_"
        case_sensitive = False

# Create global instance
api_settings = APISettings()

# Helper functions
def get_cors_origins() -> List[str]:
    """Get CORS origins from environment or default"""
    origins = os.getenv("CORS_ORIGINS")
    if origins:
        return [origin.strip() for origin in origins.split(",")]
    return api_settings.CORS_ORIGINS

def get_allowed_file_types() -> List[str]:
    """Get allowed file types from environment or default"""
    file_types = os.getenv("ALLOWED_FILE_TYPES")
    if file_types:
        return [ft.strip() for ft in file_types.split(",")]
    return api_settings.ALLOWED_FILE_TYPES

def is_file_type_allowed(filename: str) -> bool:
    """Check if file type is allowed"""
    if not filename:
        return False
    
    file_extension = os.path.splitext(filename)[1].lower()
    return file_extension in get_allowed_file_types()

def format_file_size(size_bytes: int) -> str:
    """Format file size in human readable format"""
    if size_bytes == 0:
        return "0B"
    
    size_names = ["B", "KB", "MB", "GB"]
    i = 0
    while size_bytes >= 1024 and i < len(size_names) - 1:
        size_bytes /= 1024.0
        i += 1
    
    return f"{size_bytes:.1f}{size_names[i]}"
