# Localization Infrastructure

This directory contains utilities for safely localizing the project from Russian to English. The infrastructure provides backup, validation, and language detection capabilities to ensure safe and reliable localization.

## Components

### 1. Backup Utility (`localization_backup.py`)

Creates backups of files before modification to enable rollback if needed.

**Features:**
- Backup individual files or entire directories
- Timestamped backup sessions
- Restore files from backup
- List backed up files

**Usage:**
```bash
# Backup single file
python scripts/localization_backup.py --backup-file path/to/file.py

# Backup directory with specific extensions
python scripts/localization_backup.py --backup-dir bookstore --extensions .py .md

# Restore file from backup
python scripts/localization_backup.py --restore path/to/file.py

# List backed up files
python scripts/localization_backup.py --list
```

### 2. Syntax Validator (`syntax_validator.py`)

Validates file syntax after modifications to ensure no syntax errors were introduced.

**Supported file types:**
- Python (`.py`) - AST parsing
- JSON (`.json`) - JSON parsing
- YAML (`.yml`, `.yaml`) - YAML parsing (supports multi-document)
- Markdown (`.md`) - UTF-8 encoding check
- Shell scripts (`.sh`) - bash syntax check
- PowerShell (`.ps1`) - PowerShell syntax check

**Usage:**
```bash
# Validate single file
python scripts/syntax_validator.py file.py

# Validate multiple files
python scripts/syntax_validator.py file1.py file2.json file3.yaml

# Quiet mode (only show errors)
python scripts/syntax_validator.py -q file.py
```

### 3. Language Detector (`language_detector.py`)

Detects the language of text content to verify localization progress.

**Features:**
- Detects Russian, English, mixed, or unknown language
- Analyzes character patterns and common words
- Extracts text content from various file types
- Provides confidence scores

**Usage:**
```bash
# Analyze text directly
python scripts/language_detector.py --text "Это русский текст"

# Analyze single file
python scripts/language_detector.py --file bookstore/models.py

# Analyze directory
python scripts/language_detector.py --dir bookstore --extensions .py .md

# Show summary statistics
python scripts/language_detector.py --dir bookstore --extensions .py --summary
```

### 4. Main Orchestration (`localization_utils.py`)

Unified interface that combines all utilities for safe file modification.

**Features:**
- Safe file modification with automatic backup and validation
- Progress analysis for localization projects
- Project-wide syntax validation
- Rollback on validation failures

**Usage:**
```bash
# Analyze localization progress
python scripts/localization_utils.py progress bookstore --extensions .py .md

# Validate project syntax
python scripts/localization_utils.py validate --root .

# Create backups
python scripts/localization_utils.py backup --dir bookstore --extensions .py
```

### 5. Demo Script (`demo_localization_infrastructure.py`)

Demonstrates how all utilities work together for safe localization.

**Usage:**
```bash
python scripts/demo_localization_infrastructure.py
```

## Safe Modification Workflow

The infrastructure follows this workflow for safe file modification:

1. **Language Detection**: Analyze current language of file content
2. **Backup Creation**: Create timestamped backup of original file
3. **Modification**: Apply localization changes
4. **Syntax Validation**: Verify file syntax is still valid
5. **Language Verification**: Confirm language has changed as expected
6. **Rollback**: Restore from backup if validation fails

## Example: Safe File Modification

```python
from localization_utils import LocalizationInfrastructure

# Initialize infrastructure
infra = LocalizationInfrastructure()

# Define modification function
def translate_comments(file_path: str):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Apply translations
    content = content.replace('# Комментарий', '# Comment')
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

# Safely modify file
result = infra.safe_modify_file('bookstore/models.py', translate_comments)

if result['success']:
    print(f"Successfully localized {result['file']}")
    print(f"Language changed from {result['language_before']} to {result['language_after']}")
else:
    print(f"Localization failed: {result['error']}")
```

## Progress Tracking

Monitor localization progress across the project:

```python
# Analyze progress
progress = infra.analyze_localization_progress('bookstore', ['.py'])

print(f"Localization progress: {progress['localization_progress']:.1f}%")
print(f"Files needing translation: {progress['files_needing_translation']}")
```

## Error Handling

The infrastructure handles various error conditions:

- **Syntax Errors**: Automatic rollback if validation fails
- **Encoding Issues**: UTF-8 encoding validation
- **File Access**: Graceful handling of permission issues
- **Backup Failures**: Error reporting and recovery options

## Requirements

The infrastructure requires the following Python packages:
- `pyyaml` - for YAML file validation
- Standard library modules: `ast`, `json`, `subprocess`, `pathlib`, `shutil`

## Integration with Localization Tasks

This infrastructure supports the localization tasks defined in the project specification:

- **Task 1**: Infrastructure setup (this implementation)
- **Task 2-7**: Safe modification of source code, tests, documentation, and configuration files
- **Task 8**: Final validation and testing

Each localization task can use these utilities to ensure safe and reliable translation of project files.