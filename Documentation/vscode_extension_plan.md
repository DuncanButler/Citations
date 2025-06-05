# VS Code Extension Development Plan

## Overview
The VS Code extension will provide an intuitive interface for extracting citations from code and generating documentation. It will integrate with our Python-based citation tools and provide a seamless user experience within VS Code.

## Features
- Commands for extracting citations from the current workspace
- Commands for generating documentation in different formats
- Settings for configuring citation extraction behavior
- Status bar indicator for long-running operations
- Automatic opening of generated documentation

## Development Steps

### 1. Extension Setup
- Initialize the VS Code extension project structure
- Set up TypeScript configuration
- Configure package.json with appropriate metadata
- Add extension activation events and commands

### 2. Command Implementation
- Implement the 'Extract Citations' command
- Implement the 'Generate Documentation' command
- Set up process communication with Python backend
- Add error handling and user feedback

### 3. User Interface
- Add status bar integration for progress indication
- Create settings UI for configuring the extension
- Implement file pickers for input/output selection

### 4. Testing
- Write unit tests for extension functionality
- Set up integration tests with the Python backend
- Test across different platforms (Windows, macOS, Linux)

### 5. Documentation
- Create README with installation and usage instructions
- Add inline documentation for extension code
- Create a simple demo/walkthrough guide

### 6. Publishing
- Package extension for distribution
- Publish to VS Code Marketplace
- Set up automatic updates for future versions

## Extension Dependencies
- Node.js and npm for development
- TypeScript for code implementation
- @types/vscode for VS Code API types
- Child process module for Python integration

## Extension Settings
- `copilotCitations.defaultOutputFormat`: Default format for generated documentation
- `copilotCitations.defaultOutputPath`: Default path for generated documentation
- `copilotCitations.fileExtensions`: File extensions to include in citation scanning
- `copilotCitations.pythonPath`: Custom Python interpreter path

## Resources
- [VS Code Extension API](https://code.visualstudio.com/api)
- [VS Code Extension Samples](https://github.com/microsoft/vscode-extension-samples)
- [Publishing Extensions](https://code.visualstudio.com/api/working-with-extensions/publishing-extension)
