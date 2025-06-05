"""
Tests for the Copilot citations extractor.
"""

import os
import unittest
from typing import Dict, List

# Need to fix the import path to find our source modules
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.citation_extractor import CitationExtractor
from src.citation_generator import CitationGenerator


class TestCitationExtractor(unittest.TestCase):
    """Test the CitationExtractor class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.extractor = CitationExtractor()
    
    def test_extract_from_string(self):
        """Test extracting citations from a string."""
        code = """
        # This is a test function
        # [CITATION] Source: https://example.com/test
        # [CITATION] Author: Test Author
        # [CITATION] Date: 2025-01-01
        def test_function():
            # Some code here
            pass
        """
        
        citations = self.extractor.extract_from_string(code)
        
        self.assertEqual(len(citations), 1)
        self.assertEqual(citations[0]['source'], 'https://example.com/test')
        self.assertEqual(citations[0]['author'], 'Test Author')
        self.assertEqual(citations[0]['date'], '2025-01-01')


class TestCitationGenerator(unittest.TestCase):
    """Test the CitationGenerator class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.generator = CitationGenerator()
    
    def test_markdown_generation(self):
        """Test generating Markdown documentation."""
        test_citations: Dict[str, List[Dict[str, str]]] = {
            'test.py': [
                {
                    'source': 'https://example.com/test',
                    'author': 'Test Author',
                    'date': '2025-01-01'
                }
            ]
        }
        
        test_output = 'test_output.md'
        
        # Generate the documentation
        result = self.generator._generate_markdown(test_citations, test_output)
        self.assertTrue(result)
        
        # Check that the file was created
        self.assertTrue(os.path.exists(test_output))
        
        # Clean up
        if os.path.exists(test_output):
            os.remove(test_output)


if __name__ == '__main__':
    unittest.main()
