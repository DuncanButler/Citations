"""
Citation generator module for Copilot-generated code.
"""

from typing import Dict, List


class CitationGenerator:
    """
    Generates citation documentation from extracted citations.
    """

    def __init__(self, output_format: str = "markdown"):
        """Initialize with output format."""
        self.output_format = output_format
        self.supported_formats = ["markdown", "html", "json"]
        if output_format not in self.supported_formats:
            raise ValueError(
                f"Unsupported output format: {output_format}. "
                f"Supported formats: {self.supported_formats}"
            )

    def generate(
        self, citations: Dict[str, List[Dict[str, str]]], output_path: str
    ) -> bool:
        """Generate citation documentation."""
        if not citations:
            return False

        if self.output_format == "markdown":
            return self._generate_markdown(citations, output_path)
        elif self.output_format == "html":
            return self._generate_html(citations, output_path)
        elif self.output_format == "json":
            return self._generate_json(citations, output_path)

        return False

    def _generate_markdown(
        self, citations: Dict[str, List[Dict[str, str]]], output_path: str
    ) -> bool:
        """Generate Markdown documentation."""
        try:
            with open(output_path, "w", encoding="utf-8") as f:
                f.write("# Code Citations\n\n")

                for file_path, file_citations in citations.items():
                    f.write(f"## {file_path}\n\n")

                    for i, citation in enumerate(file_citations, 1):
                        f.write(f"### Citation {i}\n\n")

                        if "source" in citation:
                            f.write(f"- **Source**: {citation['source']}\n")
                        if "author" in citation:
                            f.write(f"- **Author**: {citation['author']}\n")
                        if "date" in citation:
                            f.write(f"- **Date**: {citation['date']}\n")
                        if "description" in citation:
                            f.write(f"- **Description**: {citation['description']}\n")

                        f.write("\n")

            return True
        except Exception as e:
            print(f"Error generating Markdown documentation: {e}")
            return False

    def _generate_html(
        self, citations: Dict[str, List[Dict[str, str]]], output_path: str
    ) -> bool:
        """Generate HTML documentation."""
        try:
            with open(output_path, "w", encoding="utf-8") as f:
                html_content = """<!DOCTYPE html>
<html lang='en'>
<head>
    <meta charset='UTF-8'>
    <meta name='viewport' content='width=device-width, initial-scale=1.0'>
    <title>Code Citations</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 40px; }}
        h1 {{ color: #333; border-bottom: 2px solid #333; }}
        h2 {{ color: #666; border-bottom: 1px solid #ccc; }}
        h3 {{ color: #888; }}
        ul {{ list-style-type: none; padding-left: 0; }}
        li {{ margin: 5px 0; }}
        strong {{ color: #333; }}
        .citation {{ margin-bottom: 20px; }}
    </style>
</head>
<body>
    <h1>Code Citations</h1>
"""
                for file_path, file_citations in citations.items():
                    html_content += f"""
    <h2>{file_path}</h2>
"""
                    for i, citation in enumerate(file_citations, 1):
                        html_content += f"""
    <div class='citation'>
        <h3>Citation {i}</h3>
        <ul>
"""
                        if "source" in citation:
                            html_content += f"""
            <li><strong>Source:</strong> {citation['source']}</li>
"""
                        if "author" in citation:
                            html_content += f"""
            <li><strong>Author:</strong> {citation['author']}</li>
"""
                        if "date" in citation:
                            html_content += f"""
            <li><strong>Date:</strong> {citation['date']}</li>
"""
                        if "description" in citation:
                            html_content += f"""
            <li><strong>Description:</strong> {citation['description']}</li>
"""
                        html_content += """
        </ul>
    </div>
"""
                html_content += """
</body>
</html>
"""
                f.write(html_content)
            return True
        except Exception as e:
            print(f"Error generating HTML documentation: {e}")
            return False

    def _generate_json(
        self, citations: Dict[str, List[Dict[str, str]]], output_path: str
    ) -> bool:
        """Generate JSON documentation."""
        try:
            import json

            # Structure the data for JSON output
            json_data = {
                "title": "Code Citations",
                "generated_at": None,  # Could add timestamp if needed
                "files": {},
            }

            for file_path, file_citations in citations.items():
                json_data["files"][file_path] = {
                    "citation_count": len(file_citations),
                    "citations": [],
                }

                for i, citation in enumerate(file_citations, 1):
                    citation_entry = {
                        "id": i,
                        "source": citation.get("source", ""),
                        "author": citation.get("author", ""),
                        "date": citation.get("date", ""),
                        "description": citation.get("description", ""),
                    }
                    json_data["files"][file_path]["citations"].append(
                        citation_entry
                    )

            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(json_data, f, indent=2, ensure_ascii=False)

            return True
        except Exception as e:
            print(f"Error generating JSON documentation: {e}")
            return False
