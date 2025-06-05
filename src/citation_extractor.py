"""
Citation extractor module for Copilot-generated code.
"""

import os
import re
from typing import Dict, List, Optional


class CitationExtractor:
    """
    Extracts citations from code files based on standardized comment formats.
    
    # [CITATION] Source: GitHub Copilot Documentation
    # [CITATION] Date: 2025-06-05
    """
    
    def __init__(self, patterns: Optional[List[str]] = None):
        """Initialize with citation patterns to search for."""
        self.patterns = patterns or [
            r'(?:\/\/|\#)\s*\[CITATION\]\s*Source:\s*(.+)',
            r'(?:\/\/|\#)\s*\[CITATION\]\s*Author:\s*(.+)',
            r'(?:\/\/|\#)\s*\[CITATION\]\s*Date:\s*(.+)',
            r'(?:\/\/|\#)\s*\[CITATION\]\s*Description:\s*(.+)'
        ]
        self.compiled_patterns = [re.compile(pattern) for pattern in self.patterns]
        
    def extract_from_file(self, file_path: str) -> List[Dict[str, str]]:
        """Extract citations from a single file."""
        if not os.path.isfile(file_path):
            return []
        
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        return self.extract_from_string(content)
    
    def extract_from_string(self, content: str) -> List[Dict[str, str]]:
        """Extract citations from a string."""
        citations: List[Dict[str, str]] = []
        lines = content.splitlines()
        current_citation: Dict[str, str] = {}
        
        for line in lines:
            for i, pattern in enumerate(self.compiled_patterns):
                match = pattern.search(line)
                if match:
                    # Extract the type of citation from pattern
                    if i == 0:  # Source pattern
                        if current_citation and 'source' in current_citation:
                            # Save previous citation if we find a new source
                            citations.append(current_citation)
                            current_citation = {}
                        current_citation['source'] = match.group(1).strip()
                    elif i == 1:  # Author pattern
                        current_citation['author'] = match.group(1).strip()
                    elif i == 2:  # Date pattern
                        current_citation['date'] = match.group(1).strip()
                    elif i == 3:  # Description pattern
                        current_citation['description'] = match.group(1).strip()
        
        # Add the last citation if it exists
        if current_citation:
            citations.append(current_citation)
            
        return citations
    
    def extract_from_directory(self, directory_path: str, file_extensions: Optional[List[str]] = None) -> Dict[str, List[Dict[str, str]]]:
        """Extract citations from all files in a directory."""
        result: Dict[str, List[Dict[str, str]]] = {}
        extensions = file_extensions or ['.py', '.js', '.ts', '.java', '.cs', '.cpp', '.c']
        
        if not os.path.isdir(directory_path):
            return result
        
        for root, _, files in os.walk(directory_path):
            for file in files:
                if any(file.endswith(ext) for ext in extensions):
                    file_path = os.path.join(root, file)
                    citations = self.extract_from_file(file_path)
                    if citations:
                        relative_path = os.path.relpath(file_path, directory_path)
                        result[relative_path] = citations
        
        return result
