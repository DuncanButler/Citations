#!/usr/bin/env python
"""
Main entry point for Copilot Citations CLI tool.
"""

import argparse
import os
import sys

# Adjust import path when running the script directly
if __name__ == "__main__":
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
    from citation_extractor import CitationExtractor
    from citation_generator import CitationGenerator
else:
    from src.citation_extractor import CitationExtractor
    from src.citation_generator import CitationGenerator


def main() -> int:
    """Main entry point for the application."""
    parser = argparse.ArgumentParser(
        description="Extract and generate documentation for Copilot citations in code."
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
        help=(
            "Output file path for the generated documentation "
            "(default: Documentation/citations.md)"
        ),
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

    args = parser.parse_args()

    # Ensure input directory exists
    if not os.path.isdir(args.directory):
        print(f"Error: Directory not found: {args.directory}")
        return 1

    # Ensure output directory exists
    output_dir = os.path.dirname(args.output)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir, exist_ok=True)

    try:
        # Extract citations
        extractor = CitationExtractor()
        citations = extractor.extract_from_directory(args.directory, args.extensions)

        if not citations:
            print("No citations found in the specified directory.")
            return 0

        # Generate documentation
        generator = CitationGenerator(output_format=args.format)
        success = generator.generate(citations, args.output)

        if success:
            print(f"Citations documentation generated successfully: {args.output}")
            return 0
        else:
            print("Failed to generate citations documentation.")
            return 1

    except Exception as e:
        print(f"Error: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
