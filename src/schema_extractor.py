"""
Database Schema Extractor

This module provides functions to extract schema information from a SQLite database
using both native SQLite approach and LangChain's SQLDatabase utility.
"""

import os
import sqlite3
import argparse
import logging
from typing import Dict, Any
from langchain_community.utilities import SQLDatabase

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def get_schema_native(db_path: str) -> Dict[str, Any]:
    """
    Extracts schema information from a SQLite database using the native SQLite approach.
    
    Args:
        db_path (str): Path to the SQLite database file
    
    Returns:
        Dict[str, Any]: A dictionary containing the database schema information
    """
    if not os.path.exists(db_path):
        raise FileNotFoundError(f"Database file not found: {db_path}")
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Get all table names excluding SQLite internal tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%';")
        table_names = [table[0] for table in cursor.fetchall()]
        
        schema_info = {"tables": []}
        
        for table_name in table_names:
            # Get table info
            cursor.execute(f"PRAGMA table_info({table_name});")
            columns_info = cursor.fetchall()
            
            table_schema = {
                "name": table_name,
                "columns": []
            }
            
            for col in columns_info:
                # PRAGMA table_info returns: (cid, name, type, notnull, dflt_value, pk)
                column_info = {
                    "name": col[1],
                    "type": col[2],
                    "is_nullable": not bool(col[3]),
                    "is_primary_key": bool(col[5])
                }
                table_schema["columns"].append(column_info)
            
            # Get foreign key info
            cursor.execute(f"PRAGMA foreign_key_list({table_name});")
            fk_info = cursor.fetchall()
            
            foreign_keys = []
            for fk in fk_info:
                # fk columns: id, seq, table, from, to, on_update, on_delete, match
                foreign_keys.append({
                    "column": fk[3],
                    "referenced_table": fk[2],
                    "referenced_column": fk[4]
                })
            
            if foreign_keys:
                table_schema["foreign_keys"] = foreign_keys
            
            schema_info["tables"].append(table_schema)
        
        conn.close()
        return schema_info
    
    except sqlite3.Error as e:
        logger.error(f"SQLite error: {e}")
        raise Exception(f"SQLite error: {e}")


def get_schema_langchain(db_path: str) -> Dict[str, Any]:
    """
    Extracts schema information from a database using LangChain's SQLDatabase utility.
    
    Args:
        db_path (str): Path to the database file
    
    Returns:
        Dict[str, Any]: A dictionary containing the database schema information
    """

    cleaned_path = db_path.lstrip('./\\')
    
    # Connect to the database using LangChain with the correct URI format
    db_uri = f"sqlite:///{cleaned_path}"
    logger.info(f"Connecting to database with URI: {db_uri}")
    
    # Set sample_rows_in_table_info to 0 to avoid type conversion errors
    db = SQLDatabase.from_uri(db_uri, sample_rows_in_table_info=2)
    dialect = db.dialect
    table_info = db.table_info
    
    return dialect, table_info

