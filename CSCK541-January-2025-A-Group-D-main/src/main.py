"""
Main module for the Record Management System.
This module initializes and runs the application.
"""
import sys
import os

# Add the project root directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(__file__))))

from src.data_manager import DataManager


def main():
    """Main function to run the application"""
    
    # add frontend methods here

    data_manager = DataManager()

if __name__ == "__main__":
    main()