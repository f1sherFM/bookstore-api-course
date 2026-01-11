#!/usr/bin/env python3
"""
Demonstration script for localization infrastructure.
Shows how to use the backup, validation, and language detection utilities together.
"""

import sys
from pathlib import Path

# Add scripts directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from localization_utils import LocalizationInfrastructure


def demo_safe_modification():
    """Demonstrate safe file modification with backup and validation."""
    print("=== Localization Infrastructure Demo ===\n")
    
    # Initialize infrastructure
    infra = LocalizationInfrastructure()
    
    # Demo file modification function
    def translate_comment(file_path: str):
        """Simple demo function that translates a Russian comment to English."""
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Simple translation (for demo purposes)
        content = content.replace('# Пакет роутеров', '# Routers package')
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
    
    # Test file
    test_file = 'bookstore/routers/__init__.py'
    
    print(f"1. Analyzing file before modification: {test_file}")
    
    # Check current language
    lang_result = infra.detector.detect_file_language(test_file)
    print(f"   Language: {lang_result.get('language', 'unknown')}")
    print(f"   Confidence: {lang_result.get('confidence', 0):.2f}")
    
    print(f"\n2. Performing safe modification...")
    
    # Safely modify the file
    result = infra.safe_modify_file(test_file, translate_comment)
    
    print(f"   Success: {result['success']}")
    print(f"   Backup created: {result['backup_created']}")
    print(f"   Validation passed: {result['validation_passed']}")
    print(f"   Language before: {result['language_before']}")
    print(f"   Language after: {result['language_after']}")
    
    if result['error']:
        print(f"   Error: {result['error']}")
    
    print(f"\n3. Analyzing project progress...")
    
    # Analyze overall progress
    progress = infra.analyze_localization_progress('bookstore', ['.py'])
    
    print(f"   Total Python files: {progress['total_files']}")
    print(f"   English files: {progress['english_files']}")
    print(f"   Russian files: {progress['russian_files']}")
    print(f"   Mixed files: {progress['mixed_files']}")
    print(f"   Localization progress: {progress['localization_progress']:.1f}%")
    
    print(f"\n4. Validating project syntax...")
    
    # Validate project syntax
    validation = infra.validate_project_syntax('.')
    
    print(f"   Total files validated: {validation['total_files']}")
    print(f"   Valid files: {validation['valid_files']}")
    print(f"   Success rate: {validation['validation_success_rate']:.1f}%")
    
    print(f"\nDemo completed successfully!")
    
    # Show backup information
    backups = infra.backup.list_backups()
    if backups:
        print(f"\nBackup files created:")
        for backup_file in backups:
            print(f"   {backup_file}")


if __name__ == "__main__":
    demo_safe_modification()