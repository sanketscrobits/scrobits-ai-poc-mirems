"""
Singleton base class
"""
 
class SingletonBase:
    """Provides Singleton behavior to any class that inherits it."""
    _instance = None
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
 
 