#!/usr/bin/env python
"""
Main entry point for Copilot Citations CLI tool.

This module provides a command-line interface for extracting and generating
documentation for Copilot citations in code files.

Usage:
    python -m src.__main__ [options]
    python src/__main__.py [options]

Options:
    -d, --directory DIR     Directory to scan for citations (default: .)
    -o, --output FILE       Output file path (default: Documentation/citations.md)
    -f, --format FORMAT     Output format: markdown, html, or json (default: markdown)
    -e, --extensions EXT    File extensions to scan (default: .py .js .ts .java .cs .cpp .c)
    -r, --recursive         Scan directories recursively (default: enabled)
    --no-recursive          Disable recursive directory scanning
    --ignore PATTERNS       Patterns to ignore (comma-separated, e.g., node_modules,.git,__pycache__)
    --count-only            Only count citations without generating output files
    -v, --verbose           Enable verbose output
    -h, --help              Show this help message
    --version               Show version information
"""

import argparse
import logging
import os
import sys
import time

# Adjust import path when running the script directly
if __name__ == "__main__":
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
    from citation_extractor import CitationExtractor
    from citation_generator import CitationGenerator
else:
    from src.citation_extractor import CitationExtractor
    from src.citation_generator import CitationGenerator

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("copilot-citations")


def get_version() -> str:
    """Return the version of the application."""
    return "0.1.0"


def main() -> int:
    """Main entry point for the application."""
    parser = argparse.ArgumentParser(
        description="Extract and generate documentation for Copilot citations in code.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    parser.add_argument(
        "-d",
        "--directory",
        dest="directory",
        type=str,
        default=".",
        help="Directory to scan for citations (default: current directory)",
    )

    parser.add_argument(
        "-o",
        "--output",
        dest="output",
        type=str,
        default="Documentation/citations.md",
        help="Output file path for the generated documentation (default: Documentation/citations.md)",
    )

    parser.add_argument(
        "-f",
        "--format",
        dest="format",
        type=str,
        choices=["markdown", "html", "json"],
        default="markdown",
        help="Output format for the documentation (default: markdown)",
    )

    parser.add_argument(
        "-e",
        "--extensions",
        dest="extensions",
        type=str,
        nargs="+",
        default=[".py", ".js", ".ts", ".java", ".cs", ".cpp", ".c"],
        help="File extensions to scan (default: .py .js .ts .java .cs .cpp .c)",
    )
    
    # Add recursive option as a mutually exclusive group
    recursive_group = parser.add_mutually_exclusive_group()
    recursive_group.add_argument(
        "-r",
        "--recursive",
        dest="recursive",
        action="store_true",
        default=True,
        help="Scan directories recursively (default: enabled)",
    )
    recursive_group.add_argument(
        "--no-recursive",
        dest="recursive",
        action="store_false",
        help="Disable recursive directory scanning",
    )
    
    parser.add_argument(
        "--ignore",
        dest="ignore",
        type=str,
        default="node_modules,.git,__pycache__,dist,build",
        help="Comma-separated patterns to ignore (e.g., node_modules,.git)",
    )
    
    parser.add_argument(
        "--count-only",
        dest="count_only",
        action="store_true",
        help="Only count citations without generating output files",
    )
    
    parser.add_argument(
        "-v",
        "--verbose",
        dest="verbose",
        action="store_true",
        help="Enable verbose output",
    )
    
    parser.add_argument(
        "--version",
        action="version",
        version=f"Copilot Citations v{get_version()}",
        help="Show version information",
    )
    
    args = parser.parse_args()

    # Set up logging level
    if args.verbose:
        logger.setLevel(logging.DEBUG)
    
    logger.debug("Starting Copilot Citations extraction")
    logger.debug(f"Scanning directory: {args.directory}")
    logger.debug(f"Output file: {args.output}")
    logger.debug(f"Output format: {args.format}")
    logger.debug(f"File extensions: {args.extensions}")
    logger.debug(f"Recursive scanning: {args.recursive}")
    logger.debug(f"Ignore patterns: {args.ignore}")
    logger.debug(f"Count only mode: {args.count_only}")

    # Ensure input directory exists
    if not os.path.isdir(args.directory):
        print(f"Error: Directory not found: {args.directory}")
        return 1

    # Parse ignore patterns
    ignore_patterns = [p.strip() for p in args.ignore.split(",") if p.strip()]

    try:
        # Extract citations
        start_time = time.time()
        extractor = CitationExtractor()
        logger.debug("Starting citation extraction...")
        
        citations = extractor.extract_from_directory(
            args.directory, 
            args.extensions,
            recursive=args.recursive,
            ignore_patterns=ignore_patterns
        )
        
        extraction_time = time.time() - start_time
        
        # Count results
        total_citations = sum(len(cites) for cites in citations.values())
        file_count = len(citations)
        
        if args.verbose:
            logger.debug(f"Extraction completed in {extraction_time:.2f}s")
            logger.debug(f"Found {total_citations} citations in {file_count} files")

        if not citations:
            print("No citations found in the specified directory.")
            return 0

        # Print citation statistics
        print(f"Found {total_citations} citations in {file_count} files.")
        
        # If count-only mode, exit here
        if args.count_only:
            if args.verbose:
                # Show a breakdown of citations by file
                print("\nCitation breakdown by file:")
                for file_path, file_citations in citations.items():
                    print(f"  {file_path}: {len(file_citations)} citations")
            return 0

        # Generate documentation
        logger.debug(f"Generating {args.format} documentation...")
        start_time = time.time()
        generator = CitationGenerator(output_format=args.format)
        success = generator.generate(citations, args.output)
        generation_time = time.time() - start_time
        
        if success:
            if args.verbose:
                logger.debug(f"Documentation generated in {generation_time:.2f}s")
            print(f"Citations documentation generated successfully: {args.output}")
            return 0
        else:
            print("Failed to generate citations documentation.")
            return 1

    except KeyboardInterrupt:
        print("\nOperation cancelled by user.")
        return 130  # Standard exit code for SIGINT
    except ValueError as e:
        print(f"Validation error: {e}")
        return 1
    except PermissionError as e:
        print(f"Permission error: {e}")
        print("Make sure you have the necessary permissions to read/write the specified files.")
        return 1
    except Exception as e:
        print(f"Error: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
