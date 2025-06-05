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
                f"Unsupported output format: {output_format}. Supported formats: {self.supported_formats}"
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
                f.write("<!DOCTYPE html>\n")
                f.write("<html lang='en'>\n")
                f.write("<head>\n")
                f.write("    <meta charset='UTF-8'>\n")
                f.write(
                    "    <meta name='viewport' content='width=device-width, "
                    "initial-scale=1.0'>\n"
                )
                f.write("    <title>Code Citations</title>\n")
                f.write("    <style>\n")
                f.write(
                    "        body { font-family: Arial, sans-serif; "
                    "margin: 40px; }\n"
                )
                f.write(
                    "        h1 { color: #333; "
                    "border-bottom: 2px solid #333; }\n"
                )
                f.write(
                    "        h2 { color: #666; "
                    "border-bottom: 1px solid #ccc; }\n"
                )
                f.write("        h3 { color: #888; }\n")
                f.write(
                    "        ul { list-style-type: none; padding-left: 0; }\n"
                )
                f.write("        li { margin: 5px 0; }\n")
                f.write("        strong { color: #333; }\n")
                f.write("        .citation { margin-bottom: 20px; }\n")
                f.write("    </style>\n")
                f.write("</head>\n")
                f.write("<body>\n")
                f.write("    <h1>Code Citations</h1>\n\n")

                for file_path, file_citations in citations.items():
                    f.write(f"    <h2>{file_path}</h2>\n\n")

                    for i, citation in enumerate(file_citations, 1):
                        f.write("    <div class='citation'>\n")
                        f.write(f"        <h3>Citation {i}</h3>\n")
                        f.write("        <ul>\n")

                        if "source" in citation:
                            f.write(
                                f"            <li><strong>Source:</strong> "
                                f"{citation['source']}</li>\n"
                            )
                        if "author" in citation:
                            f.write(
                                f"            <li><strong>Author:</strong> "
                                f"{citation['author']}</li>\n"
                            )
                        if "date" in citation:
                            f.write(
                                f"            <li><strong>Date:</strong> "
                                f"{citation['date']}</li>\n"
                            )
                        if "description" in citation:
                            f.write(
                                f"            <li><strong>Description:</strong> "
                                f"{citation['description']}</li>\n"
                            )

                        f.write("        </ul>\n")
                        f.write("    </div>\n\n")

                f.write("</body>\n")
                f.write("</html>\n")

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
