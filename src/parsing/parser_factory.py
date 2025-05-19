"""
Factory for creating GTO chart parsers based on file type.
"""
import os
from typing import List

from .base_parser import BaseGTOParser
from .pdf_parser import PDFGTOParser
from .html_parser import HTMLGTOParser

class ParserFactory:
    """
    Factory class for creating appropriate GTO chart parsers.
    
    This class determines the correct parser to use based on the file format.
    """
    
    @staticmethod
    def create_parser(file_path: str) -> BaseGTOParser:
        """
        Create an appropriate parser for the given file.
        
        Args:
            file_path: Path to the file to parse
            
        Returns:
            An instance of the appropriate parser
            
        Raises:
            ValueError: If no suitable parser is found
        """
        # Get file extension
        _, ext = os.path.splitext(file_path)
        ext = ext.lower()
        
        # Select parser based on file extension
        if ext == '.pdf':
            return PDFGTOParser()
        elif ext in ('.html', '.htm'):
            return HTMLGTOParser()
        # Add additional parser types as needed
        
        raise ValueError(f"No suitable parser found for file type: {ext}")
    
    @staticmethod
    def get_supported_extensions() -> List[str]:
        """
        Get a list of supported file extensions.
        
        Returns:
            List of supported file extensions
        """
        return ['.pdf', '.html', '.htm']
    
    @staticmethod
    def parse_file(file_path: str):
        """
        Parse a file using the appropriate parser.
        
        Args:
            file_path: Path to the file to parse
            
        Returns:
            Parsed data in a standardized DataFrame
            
        Raises:
            ValueError: If no suitable parser is found
        """
        parser = ParserFactory.create_parser(file_path)
        return parser.parse(file_path) 