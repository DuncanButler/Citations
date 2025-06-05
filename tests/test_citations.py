"""
Tests for the Copilot citations extractor.
"""

import os
import tempfile
import unittest
from typing import Dict, List

# Need to fix the import path to find our source modules
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

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
        self.assertEqual(citations[0]["source"], "https://example.com/test")
        self.assertEqual(citations[0]["author"], "Test Author")
        self.assertEqual(citations[0]["date"], "2025-01-01")

    def test_extract_multiple_citations(self):
        """Test extracting multiple citations from a string."""
        code = """
        # First citation block
        # [CITATION] Source: https://example.com/first
        # [CITATION] Author: First Author
        # [CITATION] Date: 2025-01-01
        # [CITATION] Description: First example
        def first_function():
            pass
        
        # Second citation block
        # [CITATION] Source: https://example.com/second
        # [CITATION] Author: Second Author
        # [CITATION] Date: 2025-01-02
        def second_function():
            pass"""

        citations = self.extractor.extract_from_string(code)

        self.assertEqual(len(citations), 2)
        self.assertEqual(citations[0]["source"], "https://example.com/first")
        self.assertEqual(citations[0]["author"], "First Author")
        self.assertEqual(citations[0]["date"], "2025-01-01")
        self.assertEqual(citations[0]["description"], "First example")
        self.assertEqual(citations[1]["source"], "https://example.com/second")
        self.assertEqual(citations[1]["author"], "Second Author")
        self.assertEqual(citations[1]["date"], "2025-01-02")

    def test_extract_different_comment_styles(self):
        """Test extracting citations from different comment styles."""
        # JavaScript style
        js_code = """
        // [CITATION] Source: https://example.com/js
        // [CITATION] Author: JS Author
        function jsFunction() {}
        """

        # C style inline
        c_code = """
        /* [CITATION] Source: https://example.com/c */
        /* [CITATION] Author: C Author */
        int main() { return 0; }
        """

        # C style multiline
        c_multiline = """
        /*
         * [CITATION] Source: https://example.com/c-multi
         * [CITATION] Author: C Multi Author
         */
        int main() { return 0; }
        """

        # HTML style
        html_code = """
        <!-- [CITATION] Source: https://example.com/html -->
        <!-- [CITATION] Author: HTML Author -->
        <html><body></body></html>
        """

        # SQL style
        sql_code = """
        -- [CITATION] Source: https://example.com/sql
        -- [CITATION] Author: SQL Author
        SELECT * FROM users;
        """

        test_cases = [
            (js_code, "https://example.com/js", "JS Author"),
            (c_code, "https://example.com/c", "C Author"),
            (c_multiline, "https://example.com/c-multi", "C Multi Author"),
            (html_code, "https://example.com/html", "HTML Author"),
            (sql_code, "https://example.com/sql", "SQL Author"),
        ]

        for code, expected_source, expected_author in test_cases:
            citations = self.extractor.extract_from_string(code)
            self.assertEqual(len(citations), 1)
            self.assertEqual(citations[0]["source"], expected_source)
            self.assertEqual(citations[0]["author"], expected_author)

    def test_extract_partial_citations(self):
        """Test extracting citations with missing fields."""
        code = """
        # [CITATION] Source: https://example.com/partial
        # No author or date provided
        def partial_function():
            pass
        """

        citations = self.extractor.extract_from_string(code)

        self.assertEqual(len(citations), 1)
        self.assertEqual(citations[0]["source"], "https://example.com/partial")
        self.assertNotIn("author", citations[0])
        self.assertNotIn("date", citations[0])

    def test_extract_empty_string(self):
        """Test extracting citations from empty string."""
        citations = self.extractor.extract_from_string("")
        self.assertEqual(len(citations), 0)

    def test_extract_no_citations(self):
        """Test extracting from string with no citations."""
        code = """
        # This is just a regular comment
        def regular_function():
            pass
        """

        citations = self.extractor.extract_from_string(code)
        self.assertEqual(len(citations), 0)

    def test_extract_from_file_nonexistent(self):
        """Test extracting from a non-existent file."""
        citations = self.extractor.extract_from_file("nonexistent.py")
        self.assertEqual(len(citations), 0)

    def test_extract_from_directory_empty(self):
        """Test extracting from an empty/non-existent directory."""
        citations = self.extractor.extract_from_directory("nonexistent_directory")
        self.assertEqual(len(citations), 0)

    def test_extract_from_directory_with_files(self):
        """Test extracting citations from a directory with multiple files."""
        # Create a temporary directory with test files
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create a Python file with citations
            python_file = os.path.join(temp_dir, "test.py")
            with open(python_file, "w") as f:
                f.write(
                    """
# [CITATION] Source: https://example.com/python-file
# [CITATION] Author: Python File Author
def python_function():
    pass
"""
                )

            # Create a JavaScript file with citations
            js_file = os.path.join(temp_dir, "test.js")
            with open(js_file, "w") as f:
                f.write(
                    """
// [CITATION] Source: https://example.com/js-file
// [CITATION] Author: JS File Author
function jsFunction() {}
"""
                )

            # Create a file without citations
            no_citation_file = os.path.join(temp_dir, "no_citations.py")
            with open(no_citation_file, "w") as f:
                f.write(
                    """
def regular_function():
    pass
"""
                )

            # Create a file with unsupported extension
            text_file = os.path.join(temp_dir, "readme.txt")
            with open(text_file, "w") as f:
                f.write("This is just a text file")

            # Extract citations from the directory
            citations = self.extractor.extract_from_directory(temp_dir)

            # Should find citations in 2 files (Python and JavaScript)
            self.assertEqual(len(citations), 2)

            # Check that relative paths are used
            self.assertIn("test.py", citations)
            self.assertIn("test.js", citations)

            # Check citation content
            self.assertEqual(
                citations["test.py"][0]["source"], "https://example.com/python-file"
            )
            self.assertEqual(citations["test.py"][0]["author"], "Python File Author")
            self.assertEqual(
                citations["test.js"][0]["source"], "https://example.com/js-file"
            )
            self.assertEqual(citations["test.js"][0]["author"], "JS File Author")

    def test_extract_from_directory_custom_extensions(self):
        """Test extracting citations with custom file extensions."""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create a file with custom extension
            custom_file = os.path.join(temp_dir, "test.custom")
            with open(custom_file, "w") as f:
                f.write(
                    """
# [CITATION] Source: https://example.com/custom
# [CITATION] Author: Custom Author
"""
                )

            # Extract with default extensions (should find nothing)
            citations_default = self.extractor.extract_from_directory(temp_dir)
            self.assertEqual(len(citations_default), 0)

            # Extract with custom extensions (should find the file)
            citations_custom = self.extractor.extract_from_directory(
                temp_dir, [".custom"]
            )
            self.assertEqual(len(citations_custom), 1)
            self.assertIn("test.custom", citations_custom)


class TestCitationGenerator(unittest.TestCase):
    """Test the CitationGenerator class."""

    def setUp(self):
        """Set up test fixtures."""
        self.generator = CitationGenerator()

    def test_markdown_generation(self):
        """Test generating Markdown documentation."""
        test_citations: Dict[str, List[Dict[str, str]]] = {
            "test.py": [
                {
                    "source": "https://example.com/test",
                    "author": "Test Author",
                    "date": "2025-01-01",
                }
            ]
        }

        test_output = "test_output.md"
        # Generate the documentation
        result = self.generator.generate(test_citations, test_output)
        self.assertTrue(result)

        # Check that the file was created
        self.assertTrue(os.path.exists(test_output))

        # Clean up
        if os.path.exists(test_output):
            os.remove(test_output)

    def test_html_generation(self):
        """Test generating HTML documentation."""
        test_citations: Dict[str, List[Dict[str, str]]] = {
            "test.py": [
                {
                    "source": "https://example.com/test",
                    "author": "Test Author",
                    "date": "2025-01-01",
                    "description": "Test description",
                }
            ]
        }

        generator = CitationGenerator("html")
        test_output = "test_output.html"
        # Generate the documentation
        result = generator.generate(test_citations, test_output)
        self.assertTrue(result)

        # Check that the file was created
        self.assertTrue(os.path.exists(test_output))

        # Check content
        with open(test_output, "r", encoding="utf-8") as f:
            content = f.read()
            self.assertIn("<!DOCTYPE html>", content)
            self.assertIn("<title>Code Citations</title>", content)
            self.assertIn("https://example.com/test", content)
            self.assertIn("Test Author", content)
            self.assertIn("2025-01-01", content)
            self.assertIn("Test description", content)

        # Clean up
        if os.path.exists(test_output):
            os.remove(test_output)

    def test_json_generation(self):
        """Test generating JSON documentation."""
        test_citations: Dict[str, List[Dict[str, str]]] = {
            "test.py": [
                {
                    "source": "https://example.com/test",
                    "author": "Test Author",
                    "date": "2025-01-01",
                    "description": "Test description",
                }
            ]
        }

        generator = CitationGenerator("json")
        test_output = "test_output.json"
        # Generate the documentation
        result = generator.generate(test_citations, test_output)
        self.assertTrue(result)

        # Check that the file was created
        self.assertTrue(os.path.exists(test_output))

        # Check JSON structure
        import json

        with open(test_output, "r", encoding="utf-8") as f:
            data = json.load(f)
            self.assertEqual(data["title"], "Code Citations")
            self.assertIn("files", data)
            self.assertIn("test.py", data["files"])
            self.assertEqual(data["files"]["test.py"]["citation_count"], 1)
            self.assertEqual(len(data["files"]["test.py"]["citations"]), 1)

            citation = data["files"]["test.py"]["citations"][0]
            self.assertEqual(citation["source"], "https://example.com/test")
            self.assertEqual(citation["author"], "Test Author")
            self.assertEqual(citation["date"], "2025-01-01")
            self.assertEqual(citation["description"], "Test description")

        # Clean up
        if os.path.exists(test_output):
            os.remove(test_output)

    def test_multiple_files_html_generation(self):
        """Test generating HTML documentation with multiple files."""
        test_citations: Dict[str, List[Dict[str, str]]] = {
            "test1.py": [
                {
                    "source": "https://example.com/test1",
                    "author": "Author 1",
                }
            ],
            "test2.js": [
                {
                    "source": "https://example.com/test2",
                    "author": "Author 2",
                    "date": "2025-01-02",
                }
            ],
        }

        generator = CitationGenerator("html")
        test_output = "test_multiple.html"
        result = generator.generate(test_citations, test_output)
        self.assertTrue(result)

        with open(test_output, "r", encoding="utf-8") as f:
            content = f.read()
            self.assertIn("test1.py", content)
            self.assertIn("test2.js", content)
            self.assertIn("Author 1", content)
            self.assertIn("Author 2", content)

        # Clean up
        if os.path.exists(test_output):
            os.remove(test_output)

    def test_multiple_files_json_generation(self):
        """Test generating JSON documentation with multiple files."""
        test_citations: Dict[str, List[Dict[str, str]]] = {
            "test1.py": [
                {
                    "source": "https://example.com/test1",
                    "author": "Author 1",
                }
            ],
            "test2.js": [
                {
                    "source": "https://example.com/test2",
                    "author": "Author 2",
                    "date": "2025-01-02",
                }
            ],
        }

        generator = CitationGenerator("json")
        test_output = "test_multiple.json"
        result = generator.generate(test_citations, test_output)
        self.assertTrue(result)

        import json

        with open(test_output, "r", encoding="utf-8") as f:
            data = json.load(f)
            self.assertEqual(len(data["files"]), 2)
            self.assertIn("test1.py", data["files"])
            self.assertIn("test2.js", data["files"])

        # Clean up
        if os.path.exists(test_output):
            os.remove(test_output)

    def test_empty_citations(self):
        """Test generating documentation with empty citations."""
        # Test that empty citations return False
        result = self.generator.generate({}, "empty_test.md")
        self.assertFalse(result)

    def test_unsupported_format(self):
        """Test creating generator with unsupported format."""
        with self.assertRaises(ValueError):
            CitationGenerator("unsupported")


if __name__ == "__main__":
    unittest.main()
