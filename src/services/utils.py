"""
Utility service with common helper functions.
"""
import os
import hashlib
from datetime import datetime
from typing import Optional
from pathlib import Path


class UtilsService:
    """Service with utility functions"""
    
    @staticmethod
    def generate_file_hash(file_path: str) -> str:
        """
        Generate SHA256 hash of a file.
        
        Args:
            file_path: Path to the file
            
        Returns:
            SHA256 hash string
        """
        sha256_hash = hashlib.sha256()
        with open(file_path, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()
    
    @staticmethod
    def get_file_size(file_path: str) -> int:
        """
        Get file size in bytes.
        
        Args:
            file_path: Path to the file
            
        Returns:
            File size in bytes
        """
        return os.path.getsize(file_path)
    
    @staticmethod
    def get_file_extension(filename: str) -> str:
        """
        Get file extension from filename.
        
        Args:
            filename: Name of the file
            
        Returns:
            File extension (without dot)
        """
        return Path(filename).suffix[1:].lower() if Path(filename).suffix else ""
    
    @staticmethod
    def is_valid_file_extension(filename: str, allowed_extensions: list) -> bool:
        """
        Check if file has an allowed extension.
        
        Args:
            filename: Name of the file
            allowed_extensions: List of allowed extensions (without dots)
            
        Returns:
            True if extension is allowed, False otherwise
        """
        extension = UtilsService.get_file_extension(filename)
        return extension in [ext.lower() for ext in allowed_extensions]
    
    @staticmethod
    def create_upload_directory(directory: str) -> bool:
        """
        Create upload directory if it doesn't exist.
        
        Args:
            directory: Path to the directory
            
        Returns:
            True if directory exists or was created, False otherwise
        """
        try:
            Path(directory).mkdir(parents=True, exist_ok=True)
            return True
        except Exception as e:
            print(f"Error creating directory {directory}: {str(e)}")
            return False
    
    @staticmethod
    def format_datetime(dt: datetime, format_str: str = "%Y-%m-%d %H:%M:%S") -> str:
        """
        Format datetime to string.
        
        Args:
            dt: Datetime object
            format_str: Format string
            
        Returns:
            Formatted datetime string
        """
        return dt.strftime(format_str)
    
    @staticmethod
    def sanitize_filename(filename: str) -> str:
        """
        Sanitize filename by removing dangerous characters.
        
        Args:
            filename: Original filename
            
        Returns:
            Sanitized filename
        """
        # Remove path components
        filename = os.path.basename(filename)
        
        # Remove dangerous characters
        dangerous_chars = ['/', '\\', '..', '<', '>', ':', '"', '|', '?', '*']
        for char in dangerous_chars:
            filename = filename.replace(char, '_')
        
        return filename
    
    @staticmethod
    def get_file_mime_type(extension: str) -> str:
        """
        Get MIME type based on file extension.
        
        Args:
            extension: File extension (without dot)
            
        Returns:
            MIME type string
        """
        mime_types = {
            'pdf': 'application/pdf',
            'doc': 'application/msword',
            'docx': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
            'txt': 'text/plain',
            'jpg': 'image/jpeg',
            'jpeg': 'image/jpeg',
            'png': 'image/png',
        }
        return mime_types.get(extension.lower(), 'application/octet-stream')

