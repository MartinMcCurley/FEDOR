"""
Test cases for GTO chart parsers.
"""
import unittest
import os
import pandas as pd
from tempfile import NamedTemporaryFile

from src.parsing.base_parser import BaseGTOParser
from src.parsing.pdf_parser import PDFGTOParser
from src.parsing.html_parser import HTMLGTOParser
from src.parsing.parser_factory import ParserFactory

class TestParsers(unittest.TestCase):
    """Test cases for GTO chart parsers."""
    
    def setUp(self):
        """Set up test fixtures."""
        # Create a temporary PDF file for testing
        self.pdf_file = NamedTemporaryFile(suffix='.pdf', delete=False)
        self.pdf_file.close()
        
        # Create a temporary HTML file for testing
        self.html_file = NamedTemporaryFile(suffix='.html', delete=False)
        self.html_file.close()
    
    def tearDown(self):
        """Tear down test fixtures."""
        # Remove temporary files
        try:
            os.unlink(self.pdf_file.name)
            os.unlink(self.html_file.name)
        except:
            pass
    
    def test_pdf_parser_identification(self):
        """Test that PDFGTOParser correctly identifies PDF files."""
        parser = PDFGTOParser()
        self.assertTrue(parser._identify_format(self.pdf_file.name))
        self.assertFalse(parser._identify_format(self.html_file.name))
    
    def test_html_parser_identification(self):
        """Test that HTMLGTOParser correctly identifies HTML files."""
        parser = HTMLGTOParser()
        self.assertTrue(parser._identify_format(self.html_file.name))
        self.assertFalse(parser._identify_format(self.pdf_file.name))
    
    def test_factory_creates_correct_parser(self):
        """Test that ParserFactory creates the correct parser type."""
        pdf_parser = ParserFactory.create_parser(self.pdf_file.name)
        html_parser = ParserFactory.create_parser(self.html_file.name)
        
        self.assertIsInstance(pdf_parser, PDFGTOParser)
        self.assertIsInstance(html_parser, HTMLGTOParser)
        
        with self.assertRaises(ValueError):
            ParserFactory.create_parser('invalid.xyz')
    
    def test_supported_extensions(self):
        """Test that ParserFactory returns correct supported extensions."""
        extensions = ParserFactory.get_supported_extensions()
        self.assertIn('.pdf', extensions)
        self.assertIn('.html', extensions)
        self.assertIn('.htm', extensions)
    
    def test_standardize_hand_notation(self):
        """Test hand notation standardization."""
        parser = PDFGTOParser()  # Any parser will work for this test
        
        # Test pairs
        self.assertEqual(parser.standardize_hand_notation('AA'), 'AA')
        self.assertEqual(parser.standardize_hand_notation('55'), '55')
        
        # Test suited hands
        self.assertEqual(parser.standardize_hand_notation('AKs'), 'AKs')
        self.assertEqual(parser.standardize_hand_notation('T9s'), 'T9s')
        
        # Test offsuit hands
        self.assertEqual(parser.standardize_hand_notation('AKo'), 'AKo')
        self.assertEqual(parser.standardize_hand_notation('T9o'), 'T9o')
        
        # Test defaults for unspecified suit status
        self.assertEqual(parser.standardize_hand_notation('AK'), 'AKs')
        self.assertEqual(parser.standardize_hand_notation('T9'), 'T9s')
    
    def test_parse_result_format(self):
        """Test parsing result has correct format."""
        # This is a simple structure test, not checking actual parsing logic
        factory = ParserFactory()
        
        # Create a parser and mock parse-worthy content
        parser = PDFGTOParser()
        metadata = {
            "eff_stack": 25.0,
            "position": "BTN",
            "context": "BTN_RFI_25bb",
        }
        sample_data = [
            {"hand": "AA", "action": "raise", "frequency": 100},
        ]
        
        # Call _parse_content directly with our simplified data
        result = parser._parse_content({"mock": "content"}, metadata)
        
        # Verify result structure
        self.assertIsInstance(result, list)
        self.assertGreater(len(result), 0)
        self.assertIsInstance(result[0], dict)
        
        # Check required fields are present
        required_fields = ["context", "hand_range", "action", "frequency", "eff_stack"]
        for field in required_fields:
            self.assertIn(field, result[0]) 