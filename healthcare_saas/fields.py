"""
Custom encrypted field implementation using cryptography library
Compatible with Django 5.x and provides field-level encryption for PHI
"""
from django.db import models
from cryptography.fernet import Fernet
from django.conf import settings
import base64


def get_encryption_key():
    """Get or generate encryption key"""
    key = getattr(settings, 'ENCRYPTION_KEY', 'your-32-byte-encryption-key-here-change-this')
    # Ensure key is properly formatted
    if len(key) < 32:
        key = key.ljust(32, '0')
    return base64.urlsafe_b64encode(key[:32].encode())[:43] + b'='


class EncryptedField:
    """Mixin for encrypted fields"""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fernet = Fernet(get_encryption_key())
    
    def get_prep_value(self, value):
        """Encrypt before saving to database"""
        if value is None or value == '':
            return value
        if isinstance(value, str):
            encrypted = self.fernet.encrypt(value.encode())
            return encrypted.decode()
        return value
    
    def from_db_value(self, value, expression, connection):
        """Decrypt when loading from database"""
        if value is None or value == '':
            return value
        try:
            decrypted = self.fernet.decrypt(value.encode())
            return decrypted.decode()
        except Exception:
            return value
    
    def to_python(self, value):
        """Convert to Python value"""
        if isinstance(value, str) or value is None:
            return value
        return str(value)


class EncryptedCharField(EncryptedField, models.CharField):
    """Encrypted CharField"""
    pass


class EncryptedTextField(EncryptedField, models.TextField):
    """Encrypted TextField"""
    pass


class EncryptedEmailField(EncryptedField, models.EmailField):
    """Encrypted EmailField"""
    pass


class EncryptedDateField(models.DateField):
    """Encrypted DateField - stores as encrypted string"""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fernet = Fernet(get_encryption_key())
    
    def get_prep_value(self, value):
        """Encrypt date before saving"""
        if value is None:
            return None
        # Convert date to string and encrypt
        date_str = value.isoformat() if hasattr(value, 'isoformat') else str(value)
        encrypted = self.fernet.encrypt(date_str.encode())
        return encrypted.decode()
    
    def from_db_value(self, value, expression, connection):
        """Decrypt when loading from database"""
        if value is None:
            return None
        try:
            from datetime import datetime
            decrypted = self.fernet.decrypt(value.encode()).decode()
            return datetime.fromisoformat(decrypted).date()
        except Exception:
            return None
    
    def to_python(self, value):
        """Convert to Python date"""
        if value is None:
            return value
        if isinstance(value, str):
            from datetime import datetime
            try:
                return datetime.fromisoformat(value).date()
            except Exception:
                return None
        return value
