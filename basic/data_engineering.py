import pandas as pd
from pydantic import BaseModel, ValidationError
from sqlalchemy import create_engine, text
from sqlalchemy.types import Float, Integer, String
import logging
import sys
import os

# Set up basic logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Define a Pydantic model for data validation
class SalesData(BaseModel):
    name: str
    age: int
    city: str
    sales: float

def read_csv_file(file_path: str) -> pd.DataFrame:
    """
    Reads a CSV file into a Pandas DataFrame.

    Args:
        file_path (str): The path to the CSV file.

    Returns:
        pd.DataFrame: The DataFrame containing the data from the CSV file.
    """
    try:
        df = pd.read_csv(file_path)
        logger.info(f"Successfully read CSV file: {file_path}")
        return df
    except FileNotFoundError:
        logger.error(f"Error: File not found at {file_path}")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Error reading CSV file: {e}")
        sys.exit(1)

def validate_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Validates the data in a Pandas DataFrame using the SalesData Pydantic model.
    Invalid rows are logged and dropped.

    Args:
        df (pd.DataFrame): The DataFrame to validate.

    Returns:
        pd.DataFrame: The validated DataFrame.
    """
    valid_rows = []
    invalid_rows = 0
    for index, row in df.iterrows():
        try:
            # Convert row to a dictionary, handling potential type issues.
            row_dict = {
                "name": str(row["name"]),
                "age": int(row["age"]),
                "city": str(row["city"]),
                "sales": float(row["sales"]),
            }
            SalesData(**row_dict)  # Validate the data against the Pydantic model.
            valid_rows.append(row)
        except (ValueError, ValidationError) as e:
            invalid_rows += 1
            logger.warning(f"Invalid data in row {index}: {row}. Error: {e}")
    if invalid_rows > 0:
        logger.warning(f"Dropped {invalid_rows} invalid rows.")
    validated_df = pd.DataFrame(valid_rows) # Create DataFrame from valid rows
    return validated_df

def perform_aggregations(df: pd.DataFrame) -> pd.DataFrame:
    """
    Performs aggregations on the validated DataFrame.

    Args:
        df (pd.DataFrame): The validated DataFrame.

    Returns:
        pd.DataFrame: The DataFrame containing the aggregation results.
    """
    try:
        # Group data by city and calculate total sales and average age
        aggregation_df = df.groupby('city').agg(
            total_sales=('sales', 'sum'),
            average_age=('age', 'mean')
        ).reset_index()
        logger.info("Successfully performed aggregations.")
        return aggregation_df
    except KeyError as e:
        logger.error(f"Error: Key not found during aggregation: {e}")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Error during aggregation: {e}")
        sys.exit(1)

def write_to_sqlite(df: pd.DataFrame, db_name: str = 'sales_data.db', table_name: str = 'sales_summary') -> None:
    """
    Writes the aggregation results to a local SQLite database.

    Args:
        df (pd.DataFrame): The DataFrame containing the aggregation results.
        db_name (str, optional): The name of the SQLite database file. Defaults to 'sales_data.db'.
        table_name (str, optional): The name of the table to create. Defaults to 'sales_summary'.
    """
    # Ensure the database name is safe for file systems.
    if not db_name.endswith('.db'):
        db_name += '.db'
    db_path = f"sqlite:///{db_name}" # Corrected path for in-file SQLite DB.
    try:
        engine = create_engine(db_path)
        # Define the data types for the columns in the database table.
        dtype_mapping = {
            'city': String,
            'total_sales': Float,
            'average_age': Float,
        }
        df.to_sql(table_name, engine, if_exists='replace', index=False, dtype=dtype_mapping)
        logger.info(f"Successfully wrote data to table '{table_name}' in SQLite database '{db_name}'.")

        # Test the connection and perform a simple query.
        with engine.connect() as connection:
            result = connection.execute(text(f"SELECT * FROM {table_name} LIMIT 5"))
            for row in result:
                logger.info(f"Sample data from {table_name}: {row}")

    except Exception as e:
        logger.error(f"Error writing to or reading from SQLite database: {e}")
        sys.exit(1)

def main():
    """
    Main function to orchestrate the data processing pipeline.
    """
    csv_file_path = 'basic/datsets/data.csv'
    df = read_csv_file(csv_file_path)
    print("\nData Preview:")
    print(df.head())
    print()
    
    print("Data validation steps")
    validated_df = validate_data(df) # added validation
    aggregation_df = perform_aggregations(validated_df) # use validated df
    print("\nAggregation Results:")
    print(aggregation_df)
    write_to_sqlite(aggregation_df)
    logger.info("Data processing complete.")

if __name__ == "__main__":
    main()