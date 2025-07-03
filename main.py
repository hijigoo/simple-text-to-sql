"""
CSV to SQL/DB Converter Main Script

This script serves as the main entry point for converting CSV files
to SQL and SQLite database files, and extracting schema information.
It uses the functions from convert.py module.
"""
import os
import argparse
from src.sql_generator import generate_sql
from src.csv_converter import convert_csv_to_sql_and_db
from src.schema_extractor import get_schema_native, get_schema_langchain
from src.execute_query import execute_and_display
from src.response_generator import generate_response

def parse_args():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(
        description='Convert CSV to SQL/DB and extract schema information.'
    )
    parser.add_argument('--csv', default='./data/products_test_data.csv',
                        help='Path to the CSV file (default: products_test_data.csv)')
    
    parser.add_argument('--db', default='./data/products_test_data.db',
                        help='Path to the CSV file (default: products_test_data.db)')
    return parser.parse_args()


def main():
    # Parse command line arguments
    args = parse_args()
    
    # Define file paths
    current_dir = os.path.dirname(os.path.abspath(__file__))
    csv_file = os.path.join(current_dir, args.csv)
    sql_file = os.path.splitext(csv_file)[0] + '.sql'
    db_file = os.path.splitext(csv_file)[0] + '.db'
    
    # Convert CSV to SQL and DB files using the function from convert.py
    print("\n\n## Convert CSV to SQL and DB files ----------------------\n")
    convert_csv_to_sql_and_db(csv_file, sql_file, db_file)

    db_file_path = args.db
    db_file_full_path = os.path.join(current_dir, args.db)
    
    # Convert CSV to SQL and DB files using the function from convert.py
    print("\n\n## SCHEMA FROM NATIVE ----------------------\n")
    schema_from_native = get_schema_native(db_file_full_path)
    print(schema_from_native)

    # For LangChain, use the path relative to the project root
    # This ensures the URI will be in the format "sqlite:///db/Chinook.db"
    print("\n\n## SCHEMA FROM LANGCHAIN ----------------------\n")
    dialect, schema_from_langchain = get_schema_langchain(db_file_path)
    print(dialect)
    print(schema_from_langchain)
    
    # Make SQL Query
    print("\n\n## MAKE SQL QUERY ----------------------\n")
    query = "재고가 가장 많이 남은 제품 이름 10개 알려줘"
    sql_query = generate_sql(query, schema_from_langchain, dialect=dialect,
                             model_id='apac.anthropic.claude-3-7-sonnet-20250219-v1:0',
                             region_name='ap-northeast-2')
    print(sql_query)

    # Execute SQL Query
    print("\n\n## EXECUTE SQL QUERY ----------------------\n")
    query_result = execute_and_display(db_file_full_path, sql_query)
    
    # Generate natural language response
    print("\n\n## GENERATE RESPONSE ----------------------\n")
    response = generate_response(
        question=query,
        sql_query=sql_query,
        query_result=query_result,
        model_id='apac.anthropic.claude-3-7-sonnet-20250219-v1:0',
        region_name='ap-northeast-2'
    )
    print("\nResponse to user:")
    print(response)


if __name__ == "__main__":
    main()
