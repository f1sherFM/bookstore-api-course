#!/usr/bin/env python3
"""
Syntax validation utility for localization process.
Validates file syntax after modifications to ensure no syntax errors were introduced.
"""

import ast
import json
import yaml
import subprocess
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple


class SyntaxValidator:
    """Validates syntax of various file types after localization."""
    
    def __init__(self):
        """Initialize syntax validator."""
        self.validators = {
            '.py': self._validate_python,
            '.json': self._validate_json,
            '.yml': self._validate_yaml,
            '.yaml': self._validate_yaml,
            '.md': self._validate_markdown,
            '.sh': self._validate_shell,
            '.ps1': self._validate_powershell,
        }
    
    def validate_file(self, file_path: str) -> Tuple[bool, Optional[str]]:
        """Validate syntax of a single file.
        
        Args:
            file_path: Path to file to validate
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        path = Path(file_path)
        
        if not path.exists():
            return False, f"File not found: {file_path}"
        
        extension = path.suffix.lower()
        validator = self.validators.get(extension)
        
        if validator is None:
            # No specific validator, assume valid
            return True, None
        
        try:
            return validator(file_path)
        except Exception as e:
            return False, f"Validation error: {str(e)}"
    
    def validate_files(self, file_paths: List[str]) -> Dict[str, Tuple[bool, Optional[str]]]:
        """Validate syntax of multiple files.
        
        Args:
            file_paths: List of file paths to validate
            
        Returns:
            Dictionary mapping file paths to validation results
        """
        results = {}
        for file_path in file_paths:
            results[file_path] = self.validate_file(file_path)
        return results
    
    def _validate_python(self, file_path: str) -> Tuple[bool, Optional[str]]:
        """Validate Python file syntax."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Parse AST to check syntax
            ast.parse(content, filename=file_path)
            return True, None
            
        except SyntaxError as e:
            return False, f"Python syntax error: {e.msg} at line {e.lineno}"
        except Exception as e:
            return False, f"Python validation error: {str(e)}"
    
    def _validate_json(self, file_path: str) -> Tuple[bool, Optional[str]]:
        """Validate JSON file syntax."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                json.load(f)
            return True, None
            
        except json.JSONDecodeError as e:
            return False, f"JSON syntax error: {e.msg} at line {e.lineno}"
        except Exception as e:
            return False, f"JSON validation error: {str(e)}"
    
    def _validate_yaml(self, file_path: str) -> Tuple[bool, Optional[str]]:
        """Validate YAML file syntax."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                # Handle multi-document YAML files (common in Kubernetes)
                documents = list(yaml.safe_load_all(f))
                # If we got here without exception, YAML is valid
            return True, None
            
        except yaml.YAMLError as e:
            return False, f"YAML syntax error: {str(e)}"
        except Exception as e:
            return False, f"YAML validation error: {str(e)}"
    
    def _validate_markdown(self, file_path: str) -> Tuple[bool, Optional[str]]:
        """Validate Markdown file (basic check for UTF-8 encoding)."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                f.read()
            return True, None
            
        except UnicodeDecodeError as e:
            return False, f"Markdown encoding error: {str(e)}"
        except Exception as e:
            return False, f"Markdown validation error: {str(e)}"
    
    def _validate_shell(self, file_path: str) -> Tuple[bool, Optional[str]]:
        """Validate shell script syntax using bash -n."""
        try:
            result = subprocess.run(
                ['bash', '-n', file_path],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if result.returncode == 0:
                return True, None
            else:
                return False, f"Shell syntax error: {result.stderr.strip()}"
                
        except subprocess.TimeoutExpired:
            return False, "Shell validation timeout"
        except FileNotFoundError:
            # bash not available, skip validation
            return True, None
        except Exception as e:
            return False, f"Shell validation error: {str(e)}"
    
    def _validate_powershell(self, file_path: str) -> Tuple[bool, Optional[str]]:
        """Validate PowerShell script syntax."""
        try:
            result = subprocess.run(
                ['powershell', '-NoProfile', '-Command', f'Get-Command -Syntax (Get-Content "{file_path}" -Raw)'],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if result.returncode == 0:
                return True, None
            else:
                return False, f"PowerShell syntax error: {result.stderr.strip()}"
                
        except subprocess.TimeoutExpired:
            return False, "PowerShell validation timeout"
        except FileNotFoundError:
            # PowerShell not available, skip validation
            return True, None
        except Exception as e:
            return False, f"PowerShell validation error: {str(e)}"


def main():
    """Command line interface for syntax validator."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Syntax validator for localization")
    parser.add_argument("files", nargs="+", help="Files to validate")
    parser.add_argument("--quiet", "-q", action="store_true", help="Only show errors")
    
    args = parser.parse_args()
    
    validator = SyntaxValidator()
    results = validator.validate_files(args.files)
    
    all_valid = True
    for file_path, (is_valid, error_msg) in results.items():
        if is_valid:
            if not args.quiet:
                print(f"✓ {file_path}: Valid")
        else:
            print(f"✗ {file_path}: {error_msg}")
            all_valid = False
    
    if not all_valid:
        sys.exit(1)


if __name__ == "__main__":
    main()