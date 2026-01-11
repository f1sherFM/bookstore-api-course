#!/usr/bin/env python3
"""
Main orchestration script for localization infrastructure.
Provides unified interface for backup, validation, and language detection utilities.
"""

import sys
import os
from pathlib import Path
from typing import List, Dict, Optional

# Add scripts directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from localization_backup import LocalizationBackup
from syntax_validator import SyntaxValidator
from language_detector import LanguageDetector


class LocalizationInfrastructure:
    """Main orchestration class for localization infrastructure."""
    
    def __init__(self, backup_dir: str = "localization_backups"):
        """Initialize localization infrastructure.
        
        Args:
            backup_dir: Directory for backups
        """
        self.backup = LocalizationBackup(backup_dir)
        self.validator = SyntaxValidator()
        self.detector = LanguageDetector()
    
    def safe_modify_file(self, file_path: str, modification_func, *args, **kwargs) -> Dict[str, any]:
        """Safely modify a file with backup and validation.
        
        Args:
            file_path: Path to file to modify
            modification_func: Function that modifies the file
            *args, **kwargs: Arguments for modification function
            
        Returns:
            Dictionary with operation results
        """
        result = {
            'file': file_path,
            'success': False,
            'backup_created': False,
            'validation_passed': False,
            'language_before': 'unknown',
            'language_after': 'unknown',
            'error': None
        }
        
        try:
            # Check if file exists
            if not Path(file_path).exists():
                result['error'] = 'File not found'
                return result
            
            # Detect language before modification
            lang_result = self.detector.detect_file_language(file_path)
            result['language_before'] = lang_result.get('language', 'unknown')
            
            # Create backup
            backup_path = self.backup.backup_file(file_path)
            result['backup_created'] = True
            result['backup_path'] = backup_path
            
            # Perform modification
            modification_func(file_path, *args, **kwargs)
            
            # Validate syntax after modification
            is_valid, error_msg = self.validator.validate_file(file_path)
            result['validation_passed'] = is_valid
            
            if not is_valid:
                # Restore from backup if validation fails
                self.backup.restore_file(file_path)
                result['error'] = f'Validation failed: {error_msg}. File restored from backup.'
                return result
            
            # Detect language after modification
            lang_result = self.detector.detect_file_language(file_path)
            result['language_after'] = lang_result.get('language', 'unknown')
            
            result['success'] = True
            
        except Exception as e:
            result['error'] = str(e)
            # Try to restore from backup if something went wrong
            if result['backup_created']:
                try:
                    self.backup.restore_file(file_path)
                    result['error'] += ' File restored from backup.'
                except:
                    result['error'] += ' Failed to restore from backup.'
        
        return result
    
    def safe_modify_files(self, file_paths: List[str], modification_func, *args, **kwargs) -> List[Dict[str, any]]:
        """Safely modify multiple files with backup and validation.
        
        Args:
            file_paths: List of file paths to modify
            modification_func: Function that modifies files
            *args, **kwargs: Arguments for modification function
            
        Returns:
            List of operation results for each file
        """
        results = []
        for file_path in file_paths:
            result = self.safe_modify_file(file_path, modification_func, *args, **kwargs)
            results.append(result)
        return results
    
    def analyze_localization_progress(self, directory: str, extensions: Optional[List[str]] = None) -> Dict[str, any]:
        """Analyze localization progress in a directory.
        
        Args:
            directory: Directory to analyze
            extensions: File extensions to include
            
        Returns:
            Dictionary with progress analysis
        """
        results = self.detector.analyze_directory(directory, extensions)
        
        # Calculate statistics
        total_files = len([r for r in results if 'error' not in r])
        russian_files = len([r for r in results if r.get('language') == 'russian'])
        english_files = len([r for r in results if r.get('language') == 'english'])
        mixed_files = len([r for r in results if r.get('language') == 'mixed'])
        unknown_files = len([r for r in results if r.get('language') == 'unknown'])
        
        progress = {
            'directory': directory,
            'total_files': total_files,
            'russian_files': russian_files,
            'english_files': english_files,
            'mixed_files': mixed_files,
            'unknown_files': unknown_files,
            'localization_progress': (english_files / total_files * 100) if total_files > 0 else 0,
            'files_needing_translation': russian_files + mixed_files,
            'detailed_results': results
        }
        
        return progress
    
    def validate_project_syntax(self, project_root: str = ".") -> Dict[str, any]:
        """Validate syntax of all relevant files in project.
        
        Args:
            project_root: Root directory of project
            
        Returns:
            Dictionary with validation results
        """
        # Define file patterns to validate
        extensions = ['.py', '.json', '.yml', '.yaml', '.md', '.sh', '.ps1']
        
        # Find all files to validate
        files_to_validate = []
        for ext in extensions:
            pattern = f"**/*{ext}"
            files_to_validate.extend(Path(project_root).glob(pattern))
        
        # Convert to strings and filter out backup directories
        file_paths = []
        for file_path in files_to_validate:
            str_path = str(file_path)
            if 'localization_backups' not in str_path and '.git' not in str_path:
                file_paths.append(str_path)
        
        # Validate all files
        validation_results = self.validator.validate_files(file_paths)
        
        # Calculate statistics
        total_files = len(validation_results)
        valid_files = len([r for r in validation_results.values() if r[0]])
        invalid_files = total_files - valid_files
        
        return {
            'total_files': total_files,
            'valid_files': valid_files,
            'invalid_files': invalid_files,
            'validation_success_rate': (valid_files / total_files * 100) if total_files > 0 else 0,
            'detailed_results': validation_results
        }


def main():
    """Command line interface for localization infrastructure."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Localization infrastructure utilities")
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Progress analysis command
    progress_parser = subparsers.add_parser('progress', help='Analyze localization progress')
    progress_parser.add_argument('directory', help='Directory to analyze')
    progress_parser.add_argument('--extensions', nargs='+', help='File extensions to include')
    
    # Validation command
    validate_parser = subparsers.add_parser('validate', help='Validate project syntax')
    validate_parser.add_argument('--root', default='.', help='Project root directory')
    
    # Backup command
    backup_parser = subparsers.add_parser('backup', help='Create backups')
    backup_parser.add_argument('--file', help='Backup single file')
    backup_parser.add_argument('--dir', help='Backup directory')
    backup_parser.add_argument('--extensions', nargs='+', help='File extensions to backup')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    infra = LocalizationInfrastructure()
    
    if args.command == 'progress':
        progress = infra.analyze_localization_progress(args.directory, args.extensions)
        
        print(f"Localization Progress Analysis for: {progress['directory']}")
        print(f"Total files: {progress['total_files']}")
        print(f"English files: {progress['english_files']}")
        print(f"Russian files: {progress['russian_files']}")
        print(f"Mixed language files: {progress['mixed_files']}")
        print(f"Unknown language files: {progress['unknown_files']}")
        print(f"Localization progress: {progress['localization_progress']:.1f}%")
        print(f"Files needing translation: {progress['files_needing_translation']}")
        
        if progress['files_needing_translation'] > 0:
            print("\nFiles that need translation:")
            for result in progress['detailed_results']:
                if result.get('language') in ['russian', 'mixed']:
                    print(f"  {result['file']}: {result['language']}")
    
    elif args.command == 'validate':
        results = infra.validate_project_syntax(args.root)
        
        print(f"Project Syntax Validation Results")
        print(f"Total files: {results['total_files']}")
        print(f"Valid files: {results['valid_files']}")
        print(f"Invalid files: {results['invalid_files']}")
        print(f"Success rate: {results['validation_success_rate']:.1f}%")
        
        if results['invalid_files'] > 0:
            print("\nFiles with syntax errors:")
            for file_path, (is_valid, error_msg) in results['detailed_results'].items():
                if not is_valid:
                    print(f"  {file_path}: {error_msg}")
    
    elif args.command == 'backup':
        if args.file:
            infra.backup.backup_file(args.file)
        elif args.dir:
            infra.backup.backup_directory(args.dir, args.extensions)
        else:
            print("Please specify --file or --dir")


if __name__ == "__main__":
    main()