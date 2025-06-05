# Copilot Citations Python

## Introduction:
The current setup for GitHub Copilot is that citations and references are turned on, so when I use Copilot to write code, it will automatically add citations and references to the code. This is useful for ensuring that the code is properly attributed and that the sources are properly cited.

I want these citations and references to be added to the code as comments but also added as a separate file in the documentation directory so that we can use them in the documentation.

## Proposed Solutions:

### 1. Visual Studio Code Extension
A custom VS Code extension could be developed that:
- Monitors Copilot-generated code and extracts citation comments
- Parses citation information into structured data
- Automatically maintains a citations.md (or similar) file in the documentation directory
- Works across multiple programming languages
- Could provide a UI for managing and verifying citations

### 2. Post-Processing Script Solution
A Python-based solution that:
- Scans the codebase for specially formatted citation comments
- Extracts metadata like URL, author, date referenced
- Generates structured documentation in Markdown or other formats
- Could be implemented as a git pre-commit hook or scheduled task
- Example implementation would parse comments like `// [Copilot Citation: URL, Author, Date]`

### 3. Standardized Comment Format
Establish a consistent format for Copilot citations:
```
// [CITATION] Source: https://example.com/resource
// [CITATION] Author: Example Author
// [CITATION] Date: 2025-06-05
// [CITATION] Description: Explanation of what was referenced
```

### 4. Documentation Integration
- Extend existing documentation tools (Sphinx, JSDoc, etc.) to recognize citation comments
- Automatically include citations in generated documentation
- Create a dedicated citations section in project documentation

## Implementation Plan:
1. Start with a Python script that extracts citations from code files
2. Define a standard format for citation comments across the project
3. Create a script that generates a citations.md file in the Documentation directory
4. Set up automated processing as part of the build pipeline
5. Eventually, consider developing a proper VS Code extension if the approach proves valuable

## Next Steps:
- Create a prototype citation extraction script
- Define the standard citation format for the project
- Test with various Copilot-generated code samples
- Integrate with project documentation workflow