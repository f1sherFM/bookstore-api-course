#!/usr/bin/env python3
"""
Backup utility for localization process.
Creates backups of files before modification to enable rollback if needed.
"""

import os
import shutil
import datetime
from pathlib import Path
from typing import List, Optional


class LocalizationBackup:
    """Handles backup operations for localization process."""
    
    def __init__(self, backup_dir: str = "localization_backups"):
        """Initialize backup utility.
        
        Args:
            backup_dir: Directory to store backups
        """
        self.backup_dir = Path(backup_dir)
        self.backup_dir.mkdir(exist_ok=True)
        self.timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        self.session_dir = self.backup_dir / f"session_{self.timestamp}"
        self.session_dir.mkdir(exist_ok=True)
    
    def backup_file(self, file_path: str) -> str:
        """Create backup of a single file.
        
        Args:
            file_path: Path to file to backup
            
        Returns:
            Path to backup file
        """
        source_path = Path(file_path).resolve()
        if not source_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        
        # Create relative path structure in backup
        try:
            relative_path = source_path.relative_to(Path.cwd().resolve())
        except ValueError:
            # If file is not in current directory tree, use absolute path structure
            relative_path = Path(*source_path.parts[1:]) if source_path.is_absolute() else source_path
        
        backup_path = self.session_dir / relative_path
        
        # Create parent directories
        backup_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Copy file
        shutil.copy2(source_path, backup_path)
        print(f"Backed up: {file_path} -> {backup_path}")
        
        return str(backup_path)
    
    def backup_files(self, file_paths: List[str]) -> List[str]:
        """Create backups of multiple files.
        
        Args:
            file_paths: List of file paths to backup
            
        Returns:
            List of backup file paths
        """
        backup_paths = []
        for file_path in file_paths:
            try:
                backup_path = self.backup_file(file_path)
                backup_paths.append(backup_path)
            except Exception as e:
                print(f"Failed to backup {file_path}: {e}")
        
        return backup_paths
    
    def backup_directory(self, dir_path: str, extensions: Optional[List[str]] = None) -> List[str]:
        """Backup all files in directory with specified extensions.
        
        Args:
            dir_path: Directory path to backup
            extensions: List of file extensions to backup (e.g., ['.py', '.md'])
            
        Returns:
            List of backup file paths
        """
        source_dir = Path(dir_path)
        if not source_dir.exists():
            raise FileNotFoundError(f"Directory not found: {dir_path}")
        
        backup_paths = []
        for file_path in source_dir.rglob("*"):
            if file_path.is_file():
                if extensions is None or file_path.suffix in extensions:
                    try:
                        backup_path = self.backup_file(str(file_path))
                        backup_paths.append(backup_path)
                    except Exception as e:
                        print(f"Failed to backup {file_path}: {e}")
        
        return backup_paths
    
    def restore_file(self, original_path: str) -> bool:
        """Restore file from backup.
        
        Args:
            original_path: Original file path to restore
            
        Returns:
            True if restored successfully
        """
        source_path = Path(original_path).resolve()
        try:
            relative_path = source_path.relative_to(Path.cwd().resolve())
        except ValueError:
            # If file is not in current directory tree, use absolute path structure
            relative_path = Path(*source_path.parts[1:]) if source_path.is_absolute() else Path(original_path)
        
        backup_path = self.session_dir / relative_path
        
        if not backup_path.exists():
            print(f"Backup not found: {backup_path}")
            return False
        
        try:
            shutil.copy2(backup_path, source_path)
            print(f"Restored: {backup_path} -> {original_path}")
            return True
        except Exception as e:
            print(f"Failed to restore {original_path}: {e}")
            return False
    
    def list_backups(self) -> List[str]:
        """List all backed up files in current session.
        
        Returns:
            List of backed up file paths
        """
        backup_files = []
        for file_path in self.session_dir.rglob("*"):
            if file_path.is_file():
                # Convert back to original path
                relative_path = file_path.relative_to(self.session_dir)
                original_path = Path.cwd() / relative_path
                backup_files.append(str(original_path))
        
        return backup_files


def main():
    """Command line interface for backup utility."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Backup utility for localization")
    parser.add_argument("--backup-file", help="Backup single file")
    parser.add_argument("--backup-dir", help="Backup directory")
    parser.add_argument("--extensions", nargs="+", help="File extensions to backup")
    parser.add_argument("--restore", help="Restore file from backup")
    parser.add_argument("--list", action="store_true", help="List backed up files")
    
    args = parser.parse_args()
    
    backup = LocalizationBackup()
    
    if args.backup_file:
        backup.backup_file(args.backup_file)
    elif args.backup_dir:
        backup.backup_directory(args.backup_dir, args.extensions)
    elif args.restore:
        backup.restore_file(args.restore)
    elif args.list:
        files = backup.list_backups()
        print("Backed up files:")
        for file_path in files:
            print(f"  {file_path}")
    else:
        parser.print_help()


if __name__ == "__main__":
    main()