"""
Tests for the command-line interface.
"""

import os
import sys
import tempfile
import unittest
from io import StringIO
from typing import List
from unittest import mock

# Need to fix the import path to find our source modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src import __main__ as cli


class TestCLI(unittest.TestCase):
    """Test the command-line interface."""
    
    def _setup_mock_argv(self, mock_argv: mock.MagicMock, args: List[str]) -> None:
        """Helper method to set up the mock argv object with the given args.
        
        Args:
            mock_argv: The mock argv object to set up
            args: The list of command-line arguments
        """        
        mock_argv.__getitem__.side_effect = lambda i: args[i]

    def setUp(self) -> None:
        """Set up test fixtures."""
        self.test_dir = tempfile.mkdtemp()
        
        # Create a test file with citations
        self.test_file_path = os.path.join(self.test_dir, "test_file.py")
        with open(self.test_file_path, "w") as f:
            f.write("""
            # This is a test function
            # [CITATION] Source: https://example.com/cli-test
            # [CITATION] Author: CLI Test Author
            # [CITATION] Date: 2025-06-06
            def test_function():
                pass
            """)
        
        # Create a subdirectory with citations
        self.sub_dir = os.path.join(self.test_dir, "subdir")
        os.makedirs(self.sub_dir, exist_ok=True)
        self.sub_file_path = os.path.join(self.sub_dir, "sub_file.py")
        with open(self.sub_file_path, "w") as f:
            f.write("""
            # This is a test function in a subdirectory
            # [CITATION] Source: https://example.com/subdir-test
            # [CITATION] Author: Subdir Test Author
            def sub_function():
                pass
            """)
            
        # Create a directory to be ignored
        self.ignore_dir = os.path.join(self.test_dir, "node_modules")
        os.makedirs(self.ignore_dir, exist_ok=True)
        self.ignored_file_path = os.path.join(self.ignore_dir, "ignored_file.js")
        with open(self.ignored_file_path, "w") as f:
            f.write("""
            // This file should be ignored by default
            // [CITATION] Source: https://example.com/ignored-test
            // [CITATION] Author: Ignored Test Author
            function ignoredFunction() {
                return true;
            }
            """)
        
        # Create an output directory
        self.output_dir = os.path.join(self.test_dir, "Documentation")
        os.makedirs(self.output_dir, exist_ok=True)
        self.output_path = os.path.join(self.output_dir, "citations.md")

    def tearDown(self) -> None:
        """Tear down test fixtures."""
        # Clean up the temporary directory
        for root, dirs, files in os.walk(self.test_dir, topdown=False):
            for file in files:
                os.remove(os.path.join(root, file))
            for dir in dirs:
                os.rmdir(os.path.join(root, dir))
        os.rmdir(self.test_dir)
    
    @mock.patch('sys.stdout', new_callable=StringIO)
    @mock.patch('sys.argv')
    def test_cli_directory_flag(self, mock_argv: mock.MagicMock, mock_stdout: StringIO) -> None:
        """Test CLI with directory flag."""
        # Setup mock arguments
        self._setup_mock_argv(mock_argv, [
            "copilot_citations",
            "-d", self.test_dir,
            "-o", self.output_path
        ])
        
        # Call the main function
        return_code = cli.main()
        
        # Verify the output
        self.assertEqual(return_code, 0)
        self.assertIn("Citations documentation generated successfully", mock_stdout.getvalue())
        self.assertTrue(os.path.exists(self.output_path))
        
        # Check the content of the output file
        with open(self.output_path, "r") as f:
            content = f.read()
        self.assertIn("https://example.com/cli-test", content)
        self.assertIn("CLI Test Author", content)

    @mock.patch('sys.stdout', new_callable=StringIO)
    @mock.patch('sys.argv')
    def test_cli_nonexistent_directory(self, mock_argv: mock.MagicMock, mock_stdout: StringIO) -> None:
        """Test CLI with a nonexistent directory."""        # Setup mock arguments
        self._setup_mock_argv(mock_argv, [
            "copilot_citations",
            "-d", os.path.join(self.test_dir, "nonexistent"),
            "-o", self.output_path
        ])
        
        # Call the main function
        return_code = cli.main()
        
        # Verify the output
        self.assertEqual(return_code, 1)
        self.assertIn("Error: Directory not found", mock_stdout.getvalue())

    @mock.patch('sys.stdout', new_callable=StringIO)
    @mock.patch('sys.argv')          
    def test_cli_format_flag(self, mock_argv: mock.MagicMock, mock_stdout: StringIO) -> None:
        """Test CLI with format flag."""
        # Setup mock arguments
        self._setup_mock_argv(mock_argv, [
            "copilot_citations",
            "-d", self.test_dir,
            "-o", self.output_path.replace('.md', '.json'),
            "-f", "json"
        ])
        
        # Call the main function
        return_code = cli.main()
        
        # Verify the output
        self.assertEqual(return_code, 0)
        self.assertIn("Citations documentation generated successfully", mock_stdout.getvalue())
        self.assertTrue(os.path.exists(self.output_path.replace('.md', '.json')))

    @mock.patch('sys.stdout', new_callable=StringIO)
    @mock.patch('sys.argv')
    def test_cli_extensions_flag(self, mock_argv: mock.MagicMock, mock_stdout: StringIO) -> None:
        """Test CLI with extensions flag."""
        # First create a file with a different extension
        test_js_path = os.path.join(self.test_dir, "test_file.js")
        with open(test_js_path, "w") as f:
            f.write("""
            // This is a test JavaScript function
            // [CITATION] Source: https://example.com/js-test
            // [CITATION] Author: JS Test Author
            function testFunction() {
                return true;
            }
            """)
        
        # Setup mock arguments
        mock_argv.__getitem__.side_effect = lambda i: [
            "copilot_citations",
            "-d", self.test_dir,
            "-o", self.output_path,
            "-e", ".js"  # Only process JavaScript files
        ][i]
        
        # Call the main function
        return_code = cli.main()
        
        # Verify the output
        self.assertEqual(return_code, 0)
        self.assertIn("Citations documentation generated successfully", mock_stdout.getvalue())
        
        # Check the content of the output file
        with open(self.output_path, "r") as f:
            content = f.read()
        self.assertIn("https://example.com/js-test", content)
        self.assertIn("JS Test Author", content)
        self.assertNotIn("https://example.com/cli-test", content)  # Should not include Python file citations

    @mock.patch('sys.stdout', new_callable=StringIO)
    @mock.patch('sys.argv')
    def test_cli_no_citations(self, mock_argv: mock.MagicMock, mock_stdout: StringIO) -> None:
        """Test CLI when no citations are found."""
        # Create an empty directory
        empty_dir = os.path.join(self.test_dir, "empty")
        os.makedirs(empty_dir, exist_ok=True)
        
        # Setup mock arguments
        mock_argv.__getitem__.side_effect = lambda i: [
            "copilot_citations",
            "-d", empty_dir,
            "-o", self.output_path
        ][i]
        
        # Call the main function
        return_code = cli.main()
        
        # Verify the output
        self.assertEqual(return_code, 0)
        self.assertIn("No citations found", mock_stdout.getvalue())
        self.assertFalse(os.path.exists(self.output_path))
        
    @mock.patch('sys.stdout', new_callable=StringIO)
    @mock.patch('sys.stderr', new_callable=StringIO)
    @mock.patch('sys.argv')
    def test_cli_help(self, mock_argv: mock.MagicMock, mock_stderr: StringIO, mock_stdout: StringIO) -> None:
        """Test CLI help output."""
        # Setup mock arguments
        self._setup_mock_argv(mock_argv, [
            "copilot_citations",
            "--help"
        ])
        
        # Mock argparse's behavior when help is called
        with self.assertRaises(SystemExit):
            cli.main()
        
        # Verify that the help text contains expected information
        combined_output = mock_stdout.getvalue() + mock_stderr.getvalue()
        self.assertIn("usage:", combined_output)
        self.assertIn("Extract and generate documentation for Copilot citations in code", combined_output)
        self.assertIn("--directory", combined_output)
        self.assertIn("--output", combined_output)
        self.assertIn("--format", combined_output)
        self.assertIn("--extensions", combined_output)
    
    @mock.patch('sys.stdout', new_callable=StringIO)
    @mock.patch('sys.argv')
    def test_cli_recursive_flag(self, mock_argv: mock.MagicMock, mock_stdout: StringIO) -> None:
        """Test CLI with recursive flag enabled (default)."""
        # Default behavior should include subdirectories
        mock_argv.__getitem__.side_effect = lambda i: [
            "copilot_citations",
            "-d", self.test_dir,
            "-o", self.output_path
        ][i]
        
        return_code = cli.main()
        
        # Verify output contains citations from both main directory and subdirectory
        self.assertEqual(return_code, 0)
        
        with open(self.output_path, "r") as f:
            content = f.read()
        self.assertIn("https://example.com/cli-test", content)
        self.assertIn("https://example.com/subdir-test", content)
    
    @mock.patch('sys.stdout', new_callable=StringIO)
    @mock.patch('sys.argv')
    def test_cli_no_recursive_flag(self, mock_argv: mock.MagicMock, mock_stdout: StringIO) -> None:
        """Test CLI with recursive flag disabled."""
        # With --no-recursive, should only include top directory
        mock_argv.__getitem__.side_effect = lambda i: [
            "copilot_citations",
            "-d", self.test_dir,
            "-o", self.output_path,
            "--no-recursive"
        ][i]
        
        return_code = cli.main()
        
        # Verify output contains only citations from main directory
        self.assertEqual(return_code, 0)
        
        with open(self.output_path, "r") as f:
            content = f.read()
        self.assertIn("https://example.com/cli-test", content)
        self.assertNotIn("https://example.com/subdir-test", content)
    
    @mock.patch('sys.stdout', new_callable=StringIO)
    @mock.patch('sys.argv')
    def test_cli_ignore_flag(self, mock_argv: mock.MagicMock, mock_stdout: StringIO) -> None:
        """Test CLI with ignore patterns."""
        # Create JS file in main directory to verify it's not being excluded by extensions
        test_js_main_path = os.path.join(self.test_dir, "main.js")
        with open(test_js_main_path, "w") as f:
            f.write("""
            // This is a test JavaScript function in main dir
            // [CITATION] Source: https://example.com/main-js-test
            // [CITATION] Author: Main JS Test Author
            function mainJsFunction() {
                return true;
            }
            """)
        
        # Default behavior should ignore node_modules
        mock_argv.__getitem__.side_effect = lambda i: [
            "copilot_citations",
            "-d", self.test_dir,
            "-o", self.output_path
        ][i]
        
        return_code = cli.main()
        
        # Verify output doesn't contain citations from ignored directory
        self.assertEqual(return_code, 0)
        
        with open(self.output_path, "r") as f:
            content = f.read()
        self.assertIn("https://example.com/cli-test", content)  # Main dir Python file
        self.assertIn("https://example.com/main-js-test", content)  # Main dir JS file
        self.assertNotIn("https://example.com/ignored-test", content)  # Ignored JS file
    
    @mock.patch('sys.stdout', new_callable=StringIO)
    @mock.patch('sys.argv')
    def test_cli_custom_ignore_patterns(self, mock_argv: mock.MagicMock, mock_stdout: StringIO) -> None:
        """Test CLI with custom ignore patterns."""
        # Ignore the subdirectory instead
        mock_argv.__getitem__.side_effect = lambda i: [
            "copilot_citations",
            "-d", self.test_dir,
            "-o", self.output_path,
            "--ignore", "subdir,ignored_pattern"
        ][i]
        
        return_code = cli.main()
        
        # Verify output doesn't contain citations from ignored subdirectory
        self.assertEqual(return_code, 0)
        
        with open(self.output_path, "r") as f:
            content = f.read()
        self.assertIn("https://example.com/cli-test", content)  # Main dir file
        self.assertNotIn("https://example.com/subdir-test", content)  # Ignored subdir file
    
    @mock.patch('sys.stdout', new_callable=StringIO)
    @mock.patch('sys.argv')
    def test_cli_count_only_mode(self, mock_argv: mock.MagicMock, mock_stdout: StringIO) -> None:
        """Test CLI with count-only mode."""
        mock_argv.__getitem__.side_effect = lambda i: [
            "copilot_citations",
            "-d", self.test_dir,
            "--count-only"
        ][i]
        
        return_code = cli.main()
        
        # Verify the output shows the citation count but no file is generated
        self.assertEqual(return_code, 0)
        output = mock_stdout.getvalue()
        self.assertIn("Found", output)
        self.assertIn("citations", output)
        self.assertNotIn("Citations documentation generated successfully", output)
        self.assertFalse(os.path.exists(self.output_path))

    @mock.patch('sys.stdout', new_callable=StringIO)
    @mock.patch('sys.argv')
    def test_cli_verbose_count_only_mode(self, mock_argv: mock.MagicMock, mock_stdout: StringIO) -> None:
        """Test CLI with verbose count-only mode."""
        mock_argv.__getitem__.side_effect = lambda i: [
            "copilot_citations",
            "-d", self.test_dir,
            "--count-only",
            "--verbose"
        ][i]
        
        return_code = cli.main()
        
        # Verify the output includes the breakdown of citations by file
        self.assertEqual(return_code, 0)
        output = mock_stdout.getvalue()
        self.assertIn("Found", output)
        self.assertIn("citations", output)
        self.assertIn("Citation breakdown by file", output)
        self.assertNotIn("Citations documentation generated successfully", output)


if __name__ == "__main__":
    unittest.main()
