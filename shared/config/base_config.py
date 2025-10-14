"""Base configuration management using Pydantic Settings."""

import os
from typing import Dict, Any, Optional, List
from enum import Enum
from pydantic import BaseSettings, Field, validator


class Environment(str, Enum):
    """Environment enumeration."""
    DEVELOPMENT = "development"
    TESTING = "testing"
    STAGING = "staging"
    PRODUCTION = "production"


class LogLevel(str, Enum):
    """Log level enumeration."""
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


class BaseConfig(BaseSettings):
    """Base configuration using Pydantic Settings.
    
    Provides common configuration management with environment
    variable loading and validation.
    """
    
    # Environment
    environment: Environment = Field(
        Environment.DEVELOPMENT,
        description="Application environment"
    )
    debug: bool = Field(False, description="Debug mode flag")
    
    # Application settings
    app_name: str = Field("RAG AI System", description="Application name")
    app_version: str = Field("0.1.0", description="Application version")
    
    # API settings
    api_host: str = Field("127.0.0.1", description="API host")
    api_port: int = Field(8000, description="API port")
    api_workers: int = Field(1, description="Number of API workers")
    
    # Security
    secret_key: Optional[str] = Field(None, description="Secret key for encryption")
    allowed_hosts: List[str] = Field(
        default_factory=lambda: ["*"],
        description="Allowed hosts"
    )
    
    # Database
    database_url: Optional[str] = Field(None, description="Database connection URL")
    database_pool_size: int = Field(10, description="Database connection pool size")
    
    # Redis/Cache
    redis_url: Optional[str] = Field(None, description="Redis connection URL")
    cache_ttl: int = Field(3600, description="Cache TTL in seconds")
    
    # Rate limiting
    rate_limit_per_minute: int = Field(60, description="Rate limit per minute")
    rate_limit_burst: int = Field(10, description="Rate limit burst size")
    
    class Config:
        """Pydantic settings configuration."""
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False
        
    @validator("environment", pre=True)
    def validate_environment(cls, v):
        """Validate environment value."""
        if isinstance(v, str):
            return Environment(v.lower())
        return v
    
    @validator("secret_key")
    def validate_secret_key(cls, v, values):
        """Validate secret key in production."""
        if values.get("environment") == Environment.PRODUCTION and not v:
            raise ValueError("SECRET_KEY is required in production environment")
        return v
    
    @property
    def is_development(self) -> bool:
        """Check if running in development mode."""
        return self.environment == Environment.DEVELOPMENT
    
    @property
    def is_production(self) -> bool:
        """Check if running in production mode."""
        return self.environment == Environment.PRODUCTION
    
    def get_database_config(self) -> Dict[str, Any]:
        """Get database configuration."""
        return {
            "url": self.database_url,
            "pool_size": self.database_pool_size,
        }
    
    def get_redis_config(self) -> Dict[str, Any]:
        """Get Redis configuration."""
        return {
            "url": self.redis_url,
            "ttl": self.cache_ttl,
        }


class LoggingConfig(BaseSettings):
    """Structured logging configuration.
    
    Provides logging configuration with multiple handlers,
    formatters, and log levels.
    """
    
    # Log levels
    log_level: LogLevel = Field(LogLevel.INFO, description="Global log level")
    root_log_level: LogLevel = Field(LogLevel.WARNING, description="Root logger level")
    
    # Log formatting
    log_format: str = Field(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        description="Log format string"
    )
    date_format: str = Field(
        "%Y-%m-%d %H:%M:%S",
        description="Date format string"
    )
    
    # File logging
    log_file: Optional[str] = Field(None, description="Log file path")
    log_file_max_size: int = Field(
        10 * 1024 * 1024,  # 10MB
        description="Maximum log file size in bytes"
    )
    log_file_backup_count: int = Field(5, description="Number of backup log files")
    
    # Console logging
    log_to_console: bool = Field(True, description="Enable console logging")
    console_log_level: LogLevel = Field(LogLevel.INFO, description="Console log level")
    
    # Structured logging
    use_json_logging: bool = Field(False, description="Use JSON log formatting")
    include_extra_fields: bool = Field(True, description="Include extra fields in logs")
    
    # Logger-specific levels
    logger_levels: Dict[str, str] = Field(
        default_factory=lambda: {
            "uvicorn": "INFO",
            "httpx": "WARNING",
            "urllib3": "WARNING",
        },
        description="Logger-specific log levels"
    )
    
    class Config:
        """Pydantic settings configuration."""
        env_prefix = "LOG_"
        env_file = ".env"
        case_sensitive = False
    
    @validator("log_level", "root_log_level", "console_log_level", pre=True)
    def validate_log_levels(cls, v):
        """Validate log level values."""
        if isinstance(v, str):
            return LogLevel(v.upper())
        return v
    
    def get_logging_dict_config(self) -> Dict[str, Any]:
        """Get logging configuration dictionary.
        
        Returns:
            Dict[str, Any]: Logging configuration for dictConfig
        """
        config = {
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {
                "standard": {
                    "format": self.log_format,
                    "datefmt": self.date_format,
                },
            },
            "handlers": {},
            "loggers": {},
            "root": {
                "level": self.root_log_level.value,
                "handlers": [],
            },
        }
        
        # Console handler
        if self.log_to_console:
            config["handlers"]["console"] = {
                "class": "logging.StreamHandler",
                "level": self.console_log_level.value,
                "formatter": "standard",
                "stream": "ext://sys.stdout",
            }
            config["root"]["handlers"].append("console")
        
        # File handler
        if self.log_file:
            config["handlers"]["file"] = {
                "class": "logging.handlers.RotatingFileHandler",
                "level": self.log_level.value,
                "formatter": "standard",
                "filename": self.log_file,
                "maxBytes": self.log_file_max_size,
                "backupCount": self.log_file_backup_count,
            }
            config["root"]["handlers"].append("file")
        
        # Logger-specific levels
        for logger_name, level in self.logger_levels.items():
            config["loggers"][logger_name] = {
                "level": level,
                "handlers": [],
                "propagate": True,
            }
        
        return config