"""
CSV Converter Module

This module provides functions for CSV file conversion and schema extraction.
"""
import os
import csv
import sqlite3
import argparse
import pandas as pd
from sqlalchemy import create_engine


def csv_to_sql_file(csv_file, sql_file):
    """
    Convert a CSV file to SQL statements and save them to a file.
    
    Args:
        csv_file (str): Path to the CSV file
        sql_file (str): Path to the SQL file to be created
    
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        with open(csv_file, 'r', encoding='utf-8') as file:
            csv_reader = csv.reader(file)
            headers = next(csv_reader)
            
            # Create SQL file and write the CREATE TABLE statement
            with open(sql_file, 'w', encoding='utf-8') as sql:
                # Write CREATE TABLE statement
                table_name = os.path.splitext(os.path.basename(csv_file))[0]
                sql.write(f"CREATE TABLE IF NOT EXISTS {table_name} (\n")
                
                # Determine column types based on the first row of data
                first_row = next(csv_reader)
                column_types = []
                
                for value in first_row:
                    if value.isdigit():
                        if len(value) > 9:  # Large numbers might be IDs
                            column_types.append("INTEGER")
                        else:
                            column_types.append("INTEGER")
                    elif value.replace(".", "", 1).isdigit():
                        column_types.append("REAL")
                    else:
                        # Don't try to parse as date, just use TEXT for non-numeric values
                        column_types.append("TEXT")
                
                # Write column definitions
                for i, header in enumerate(headers):
                    sql.write(f"    {header} {column_types[i]}")
                    if header == headers[0]:  # Assume first column is the primary key
                        sql.write(" PRIMARY KEY")
                    
                    if i < len(headers) - 1:
                        sql.write(",\n")
                    else:
                        sql.write("\n")
                
                sql.write(");\n\n")
                
                # Write INSERT statements for the first row
                sql.write(f"INSERT INTO {table_name} ({', '.join(headers)}) VALUES\n")
                values = [f"'{value}'" if col_type == "TEXT" or col_type == "DATE" else value 
                          for value, col_type in zip(first_row, column_types)]
                sql.write(f"({', '.join(values)})")
                
                # Reset file pointer and skip headers
                file.seek(0)
                next(csv_reader)
                
                # Skip the first row which we already processed
                next(csv_reader)
                
                # Write INSERT statements for the remaining rows
                for row in csv_reader:
                    values = [f"'{value}'" if col_type == "TEXT" or col_type == "DATE" else value 
                              for value, col_type in zip(row, column_types)]
                    sql.write(f",\n({', '.join(values)})")
                
                sql.write(";\n")
        
        print(f"- SQL file created successfully: {sql_file}")
        return True
        
    except Exception as e:
        print(f"- Error creating SQL file: {e}")
        return False


def csv_to_db_file(csv_file, db_file):
    """
    Convert a CSV file to SQLite database file using pandas and to_sql.
    
    Args:
        csv_file (str): Path to the CSV file
        db_file (str): Path to the SQLite database file to be created
    
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        df = pd.read_csv(csv_file)
        table_name = os.path.splitext(os.path.basename(csv_file))[0]
        engine = create_engine(f'sqlite:///{db_file}')
        df.to_sql(table_name, engine, if_exists='replace', index=False)
        
        print(f"- SQLite database created successfully: {db_file}")
        return True
        
    except Exception as e:
        print(f"- Error creating database: {e}")
        return False


def convert_csv_to_sql_and_db(csv_file, sql_file=None, db_file=None):
    """
    Convert CSV file to both SQL and SQLite database files.
    
    Args:
        csv_file (str): Path to the CSV file
        sql_file (str, optional): Path for the output SQL file. If None, uses the CSV filename with .sql extension.
        db_file (str, optional): Path for the output DB file. If None, uses the CSV filename with .db extension.
    
    Returns:
        tuple: (sql_result, db_result) - Boolean values indicating success of each conversion
    """
    # Generate default filenames if not provided
    if sql_file is None:
        sql_file = os.path.splitext(csv_file)[0] + '.sql'
    if db_file is None:
        db_file = os.path.splitext(csv_file)[0] + '.db'
    
    # Check if the CSV file exists
    if not os.path.isfile(csv_file):
        print(f"- Error: CSV file not found at {csv_file}")
        return False, False
    
    print(f"- Converting {csv_file} to SQL and DB files...")
    
    # Convert CSV to SQL file
    sql_result = csv_to_sql_file(csv_file, sql_file)
    if sql_result:
        print(f"- SQL conversion completed: {sql_file}")
    else:
        print("- SQL conversion failed.")
    
    # Convert CSV to DB file
    db_result = csv_to_db_file(csv_file, db_file)
    if db_result:
        print(f"- DB conversion completed: {db_file}")
    else:
        print("- DB conversion failed.")
    
    # Summary
    if sql_result and db_result:
        print("- All conversions completed successfully!")
    elif sql_result:
        print("- Only SQL conversion completed successfully.")
    elif db_result:
        print("- Only DB conversion completed successfully.")
    else:
        print("- All conversions failed.")
    
    return sql_result, db_result



