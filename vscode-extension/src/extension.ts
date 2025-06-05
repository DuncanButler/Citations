import * as vscode from 'vscode';
import * as fs from 'fs';
import * as path from 'path';
import { exec } from 'child_process';

export function activate(context: vscode.ExtensionContext) {
    // Register command to extract citations
    let extractCitations = vscode.commands.registerCommand('copilot-citations.extractCitations', async () => {
        const workspaceFolders = vscode.workspace.workspaceFolders;
        if (!workspaceFolders) {
            vscode.window.showErrorMessage('No workspace folder is open');
            return;
        }

        const workspacePath = workspaceFolders[0].uri.fsPath;
        
        // This is where we would integrate with the Python extraction script
        vscode.window.showInformationMessage('Extracting Copilot citations...');
        
        // Example of how we might call the Python script
        const pythonScriptPath = path.join(workspacePath, 'src', '__main__.py');
        
        if (!fs.existsSync(pythonScriptPath)) {
            vscode.window.showErrorMessage(`Python script not found: ${pythonScriptPath}`);
            return;
        }
        
        // Run the extraction process
        exec(`python "${pythonScriptPath}" -d "${workspacePath}"`, (error, stdout, stderr) => {
            if (error) {
                vscode.window.showErrorMessage(`Error extracting citations: ${error.message}`);
                return;
            }
            
            if (stderr) {
                vscode.window.showWarningMessage(`Citations extraction warning: ${stderr}`);
            }
            
            vscode.window.showInformationMessage(`Citations extracted: ${stdout}`);
        });
    });

    // Register command to generate documentation
    let generateDocumentation = vscode.commands.registerCommand('copilot-citations.generateDocumentation', async () => {
        const workspaceFolders = vscode.workspace.workspaceFolders;
        if (!workspaceFolders) {
            vscode.window.showErrorMessage('No workspace folder is open');
            return;
        }

        const workspacePath = workspaceFolders[0].uri.fsPath;
        const outputPath = path.join(workspacePath, 'Documentation', 'citations.md');
        
        // Run the documentation generation process
        vscode.window.showInformationMessage('Generating Copilot citations documentation...');
        
        // Example of how we might call the Python script
        const pythonScriptPath = path.join(workspacePath, 'src', '__main__.py');
        
        if (!fs.existsSync(pythonScriptPath)) {
            vscode.window.showErrorMessage(`Python script not found: ${pythonScriptPath}`);
            return;
        }
        
        exec(`python "${pythonScriptPath}" -d "${workspacePath}" -o "${outputPath}"`, (error, stdout, stderr) => {
            if (error) {
                vscode.window.showErrorMessage(`Error generating documentation: ${error.message}`);
                return;
            }
            
            if (stderr) {
                vscode.window.showWarningMessage(`Documentation generation warning: ${stderr}`);
            }
            
            vscode.window.showInformationMessage(`Documentation generated: ${outputPath}`);
            
            // Open the generated documentation file
            vscode.commands.executeCommand('vscode.open', vscode.Uri.file(outputPath));
        });
    });

    context.subscriptions.push(extractCitations, generateDocumentation);
}

export function deactivate() {}
