from sqlalchemy import create_engine, text
import logging
import pandas as pd

"""
Module: Data Ingestion

This module handles the ingestion of data into the Maji Ndogo farm survey database

Import Statements: The code imports necessary modules such as create engine and text from SQLAlchemy, logging, and pandas for data manipulation.

Logger Configuration: It configures a logger named 'data_ingestion' using the Python logging module.
The logger will output log messages of level INFO and above to the console with a specific format including a timestamp, logger name, and log level

Database Path: It defines the path to a SQLite database file named 'Maji Ndogo_farm survey_small.db'

Import Statements: The code imports necessary modules such as create engine and text from SQLAlchemy, logging, and pandas for data manipulation. 

Logger Configuration: It configures a logger named 'data_ingestion' using the Python logging module. The logger will output log messages of level 

Database Path: It defines the path to a SQLite database file named 'Maji Ndogo_farm_survey_small.db'.


It performs the following tasks:
1. Sets up logging configuration to log messages with a timestamp, logger name, and message level.
2. Defines a SQLite database path.
3. Constructs an SQL query to select data from multiple tables using various joins.
4. Defines URLs for weather data and weather data field mapping.
5. Imports necessary libraries such as SQLAlchemy, pandas, and logging.

"""

# Name our logger so we know that logs from this module come from the data_ingestion module
logger = logging.getLogger('data_ingestion')
# Set a basic logging message up that prints out a timestamp, the name of our logger, and the message
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
db_path = 'sqlite:///Maji_Ndogo_farm_survey_small.db'

sql_query = """
SELECT *
FROM geographic_features
LEFT JOIN weather_features USING (Field_ID)
LEFT JOIN soil_and_crop_features USING (Field_ID)
LEFT JOIN farm_management_features USING (Field_ID)
"""

weather_data_URL = "https://raw.githubusercontent.com/Explore-AI/Public-Data/master/Maji_Ndogo/Weather_station_data.csv"
weather_mapping_data_URL = "https://raw.githubusercontent.com/Explore-AI/Public-Data/master/Maji_Ndogo/Weather_data_field_mapping.csv"


### START FUNCTION

def create_db_engine(db_path):
    """
    Create a SQLAlchemy database engine.

    Args:
        db_path (str): The path to the database.

    Returns:
        sqlalchemy.engine.base.Engine: The SQLAlchemy engine object.
    """
    try:
        engine = create_engine(db_path)
        # Test connection
        with engine.connect() as conn:
            pass
        # test if the database engine was created successfully
        logger.info("Database engine created successfully.")
        return engine  # Return the engine object if it all works well
    except ImportError:  # If we get an ImportError, inform the user SQLAlchemy is not installed
        logger.error("SQLAlchemy is required to use this function. Please install it first.")
        raise e
    except Exception as e:  # If we fail to create an engine inform the user
        logger.error(f"Failed to create database engine. Error: {e}")
        raise e

def query_data(engine, sql_query):
    """
    Execute a SQL query on a database engine and return the result as a DataFrame.

    Args:
        engine (sqlalchemy.engine.base.Engine): The SQLAlchemy engine object.
        sql_query (str): The SQL query to execute.

    Returns:
        pandas.DataFrame: The result of the SQL query as a DataFrame.
    """
    try:
        with engine.connect() as connection:
            df = pd.read_sql_query(text(sql_query), connection)
        if df.empty:
            # Log a message or handle the empty DataFrame scenario as needed
            msg = "The query returned an empty DataFrame."
            logger.error(msg)
            raise ValueError(msg)
        logger.info("Query executed successfully.")
        return df
    except ValueError as e:
        logger.error(f"SQL query failed. Error: {e}")
        raise e
    except Exception as e:
        logger.error(f"An error occurred while querying the database. Error: {e}")
        raise e

def read_from_web_CSV(URL):
    """
    Read a CSV file from a web URL and return it as a DataFrame.

    Args:
        URL (str): The URL of the CSV file.

    Returns:
        pandas.DataFrame: The CSV file contents as a DataFrame.
    """
    try:
        df = pd.read_csv(URL)
        logger.info("CSV file read successfully from the web.")
        return df
    except pd.errors.EmptyDataError as e:
        logger.error("The URL does not point to a valid CSV file. Please check the URL and try again.")
        raise e
    except Exception as e:
        logger.error(f"Failed to read CSV from the web. Error: {e}")
        raise e

### END FUNCTION




