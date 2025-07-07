#!/usr/bin/env python3
"""
Test database cleanup script.

This script removes any test database files that may have been left behind
from previous test runs.
"""

import os
import glob

def cleanup_test_databases():
    """
    Clean up test database files from the current directory.
    """
    # Find all test database files
    test_db_patterns = [
        "./test_*.db",
        "./test_*.sqlite",
        "./test_*.sqlite3"
    ]
    
    removed_files = []
    
    for pattern in test_db_patterns:
        files = glob.glob(pattern)
        for db_file in files:
            try:
                os.remove(db_file)
                removed_files.append(db_file)
                print(f"Removed test database: {db_file}")
            except Exception as e:
                print(f"Failed to remove {db_file}: {e}")
    
    if not removed_files:
        print("No test database files found to clean up.")
    else:
        print(f"Successfully cleaned up {len(removed_files)} test database files.")

if __name__ == "__main__":
    cleanup_test_databases()
