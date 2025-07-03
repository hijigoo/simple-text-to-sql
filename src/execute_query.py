import logging
import sqlite3
import pandas as pd

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def execute_sql_query(db_path, sql_query):
    """Execute SQL query on SQLite database and return results"""

    cleaned_path = db_path.lstrip('./\\')
    
    # Log the path we're connecting to
    logger.info(f"Connecting to database: {db_path}")
    conn = sqlite3.connect(db_path)
    try:
        df = pd.read_sql_query(sql_query, conn)
        return df
    except Exception as e:
        return f"Error executing query: {str(e)}"
    finally:
        conn.close()

def execute_and_display(db_path, sql_query):
    """Execute SQL query and display results in a formatted way"""
    result = execute_sql_query(db_path, sql_query)
    
    if isinstance(result, str):  # Error case
        print(result)
        return None
    
    print(f"Query executed successfully. Found {len(result)} rows.")
    print("\nResults:")
    print(result.to_string(index=False))
    return result
