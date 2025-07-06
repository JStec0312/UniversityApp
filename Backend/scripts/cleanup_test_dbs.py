"""
Script to clean up all test database files in the workspace.

This script can be run manually to clean up any test database files
that might have been left behind.
"""

import os
import glob
import sys

def clean_test_databases():
    """
    Find and remove all test database files in the current directory.
    """
    # Define patterns for test database files
    db_patterns = [
        "./test_*.db",                  # Matches test_admin_api_uuid.db, etc.
        "./test.db",                    # Matches test.db
        "./*test*.db",                  # Catches any db with 'test' in the name
        "./test_group_register_*.db"    # Specific pattern for group register test dbs
    ]
    
    # Find all test database files
    test_db_files = []
    for pattern in db_patterns:
        test_db_files.extend(glob.glob(pattern))
    
    if not test_db_files:
        print("No test database files found.")
        return
    
    # Display found database files
    print(f"Found {len(test_db_files)} test database files:")
    for db_file in test_db_files:
        print(f"  - {db_file}")
    
    # Confirm deletion
    confirmation = input("\nAre you sure you want to delete these files? (y/n): ")
    if confirmation.lower() != 'y':
        print("Operation cancelled.")
        return
    
    # Delete the files
    deleted_count = 0
    for db_file in test_db_files:
        try:
            os.remove(db_file)
            print(f"Deleted: {db_file}")
            deleted_count += 1
        except Exception as e:
            print(f"Failed to delete {db_file}: {e}")
    
    print(f"\nCleanup complete. Deleted {deleted_count} test database files.")

if __name__ == "__main__":
    print("Test Database Cleanup Utility")
    print("============================\n")
    clean_test_databases()
