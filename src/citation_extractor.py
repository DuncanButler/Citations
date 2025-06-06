"""
Citation extractor module for Copilot-generated code.
"""

import os
import re
from typing import Dict, List, Optional


class CitationExtractor:
    """
    Extracts citations from code files based on standardized comment formats.

    Supports multiple comment styles:
    - # for Python, Shell, Ruby, Perl, etc.
    - // for JavaScript, TypeScript, C++, Java, C#, Go, etc.
    - /* */ for C, C++, Java, JavaScript, CSS, etc.
    - * for continuation lines in multiline C-style comments
    - <!-- --> for HTML, XML, etc.
    - -- for SQL, Haskell, etc.

    Citation format:
    # [CITATION] Source: https://example.com/resource
    # [CITATION] Author: Example Author
    # [CITATION] Date: 2025-06-05
    # [CITATION] Description: Brief explanation of what was referenced
    """

    def __init__(self, patterns: Optional[List[str]] = None):
        """
        Initialize with citation patterns to search for.

        Args:
            patterns: Optional list of regex patterns to override defaults.
                     Default patterns support #, //, /*, *, <!--, and -- comments.
        """
        self.patterns = patterns or [
            r"(?:\/\/|\#|\/\*|\*|<!--|--)\s*\[CITATION\]\s*Source:\s*(.+?)(?:\s*\*\/|-->|$)",  # noqa: E501
            r"(?:\/\/|\#|\/\*|\*|<!--|--)\s*\[CITATION\]\s*Author:\s*(.+?)(?:\s*\*\/|-->|$)",  # noqa: E501
            r"(?:\/\/|\#|\/\*|\*|<!--|--)\s*\[CITATION\]\s*Date:\s*(.+?)(?:\s*\*\/|-->|$)",  # noqa: E501
            r"(?:\/\/|\#|\/\*|\*|<!--|--)\s*\[CITATION\]\s*Description:\s*(.+?)(?:\s*\*\/|-->|$)",  # noqa: E501
        ]
        self.compiled_patterns = [re.compile(pattern) for pattern in self.patterns]

    def extract_from_file(self, file_path: str) -> List[Dict[str, str]]:
        """
        Extract citations from a single file.

        Args:
            file_path: Path to the file to extract citations from.

        Returns:
            List of citation dictionaries with keys: source, author, date, description.
            Returns empty list if file doesn't exist or has no citations.
        """
        if not os.path.isfile(file_path):
            return []        
        
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        return self.extract_from_string(content)
        
    def extract_from_string(self, content: str) -> List[Dict[str, str]]:
        """
        Extract citations from a string.

        Args:
            content: String content to extract citations from.

        Returns:
            List of citation dictionaries. Each citation may contain:
            - 'source': URL or reference source
            - 'author': Author name
            - 'date': Date string
            - 'description': Description of what was referenced
        """
        citations: List[Dict[str, str]] = []
        lines = content.splitlines()
        current_citation: Dict[str, str] = {}

        for line in lines:
            for i, pattern in enumerate(self.compiled_patterns):
                match = pattern.search(line)
                if match:
                    # Extract the type of citation from pattern
                    if i == 0:  # Source pattern
                        if current_citation and "source" in current_citation:
                            # Save previous citation if we find a new source
                            citations.append(current_citation)
                            current_citation = {}
                        current_citation["source"] = match.group(1).strip()
                    elif i == 1:  # Author pattern
                        current_citation["author"] = match.group(1).strip()
                    elif i == 2:  # Date pattern
                        current_citation["date"] = match.group(1).strip()
                    elif i == 3:  # Description pattern
                        current_citation["description"] = match.group(1).strip()
        
        # Add the last citation if it exists and has a source
        if current_citation and "source" in current_citation:
            citations.append(current_citation)

        return citations

    def extract_from_directory(
        self, directory_path: str, file_extensions: Optional[List[str]] = None, 
        recursive: bool = True, ignore_patterns: Optional[List[str]] = None
    ) -> Dict[str, List[Dict[str, str]]]:  # noqa: E501
        """
        Extract citations from all files in a directory.
          Args:
            directory_path: Path to directory to scan.
            file_extensions: List of file extensions to include.
                           Defaults to common programming languages (.py, .js, .ts, etc.),
                           web files (.html, .xml, .css), data files (.sql, .json, .yaml),
                           and documentation files (.md, .rst).
            recursive: Whether to scan directories recursively. Default is True.
            ignore_patterns: List of directory or file patterns to ignore (e.g., node_modules, .git)

        Returns:
            Dictionary mapping relative file paths to lists of citations found in each file.
            Only includes files that contain citations.
        """
        result: Dict[str, List[Dict[str, str]]] = {}
        extensions = file_extensions or [
            # Programming languages
            ".py",
            ".js",
            ".ts",
            ".java",
            ".cs",
            ".cpp",
            ".c",
            ".go",
            ".rb",
            ".php",
            # Web files
            ".html",
            ".xml",
            ".css",
            ".svg",
            # Data/config files
            ".sql",
            ".json",
            ".yaml",
            ".yml",
            # Documentation
            ".md",
            ".rst",
        ]

        ignore_patterns = ignore_patterns or []

        if not os.path.isdir(directory_path):
            return result
          # Helper function to check if path should be ignored
        def should_ignore(path: str) -> bool:
            for pattern in ignore_patterns:
                if pattern in path:
                    return True
            return False

        if recursive:
            # Walk recursively through the directory
            for root, dirs, files in os.walk(directory_path):
                # Filter out directories that match ignore patterns
                dirs[:] = [d for d in dirs if not should_ignore(os.path.join(root, d))]
                
                for file in files:
                    file_path = os.path.join(root, file)
                    if should_ignore(file_path):
                        continue
                        
                    if any(file.endswith(ext) for ext in extensions):
                        citations = self.extract_from_file(file_path)
                        if citations:
                            relative_path = os.path.relpath(file_path, directory_path)
                            result[relative_path] = citations
        else:
            # Non-recursive mode, only check files in the top directory
            for file in os.listdir(directory_path):
                file_path = os.path.join(directory_path, file)
                if os.path.isfile(file_path) and not should_ignore(file_path):
                    if any(file.endswith(ext) for ext in extensions):
                        citations = self.extract_from_file(file_path)
                        if citations:
                            relative_path = os.path.relpath(file_path, directory_path)
                            result[relative_path] = citations

        return result
