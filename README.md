# 🧪 Python Data Engineering learnig guide by @floripacodegurus

## Overview

This is a beginner-friendly Python project that demonstrates basic data engineering workflows:

- Reading data from a CSV file
- Performing aggregations using `pandas`
- Writing results into a local SQLite or PostgreSQL database

---

## Prerequisites

* A computer with a compatible operating system (Windows, macOS, or Linux).
* Basic understanding of command-line concepts.
* Python 3.x installed.

## 🚀 Getting Started

This is the steps for the basic part.

##  1️⃣ Installation

1.  **Install Python:**

    * Download the latest stable version from the official Python website (<https://www.python.org/downloads/>).
    * Follow the installation instructions for your operating system.
    * Ensure that Python is added to your system's PATH environment variable.
    * Verify the installation by opening a terminal or command prompt and typing:
        ```bash
        python3 --version
        ```

2.  **Create a Virtual Environment:**

    * Open a terminal or command prompt.
    * Navigate to your project directory:
        ```bash
        cd ~/projects
        ```
    * Create a virtual environment:
        ```bash
        python3 -m venv venv
        ```
    * Activate the virtual environment:
        * **Linux/macOS:**
            ```bash
            source venv/bin/activate
            ```
        * **Windows:**
            ```bash
            venv\Scripts\activate
            ```

3.  **Install Dependencies:**

    * With the virtual environment activated, install the required Python packages:
        ```bash
        pip install pandas Pydantic psycopg2-binary SQLAlchemy
        ```
    * or
        ```bash
        pip install -r requirements.txt
        ```

## 2️⃣ Usage

1.  **Prepare the CSV File:**

    * Create a CSV file named `data.csv` in your project directory with the following data:

        ```csv
        name,age,city,sales
        Alice,30,New York,120.50
        Bob,25,Los Angeles,85.00
        Charlie,35,New York,150.00
        David,28,Chicago,95.75
        Eve,40,Los Angeles,200.25
        Frank,32,Chicago,110.00
        ```

2.  **Run the Python Script:**

    * Ensure you are in the project directory with your virtual environment activated.
    * Execute the `data_engineering.py` script:
        ```bash
        python data_engineering.py
        ```

## 3️⃣ Functionality

The `data_engineering.py` script performs the following actions:

* Reads data from the `data.csv` file.
* Validates the data using a Pydantic model (`SalesData`). Invalid rows are dropped and logged.
* Performs aggregations on the valid data:
    * Groups data by city.
    * Calculates the total sales for each city.
    * Calculates the average age for each city.
* Prints the aggregation results to the console.
* Writes the aggregation results to a local SQLite database file named `sales_data.db` in a table named `sales_summary`.
* Prints the first 5 rows from the `sales_summary` table to the console.

## 📦 Project Structure

├── venv/                     # Virtual environment
├── data.csv                  # Sample input data
├── data_engineering.py       # Main ETL script
└── README.md                 # Documentation


## 4️⃣ Data Validation

The script uses a Pydantic model (`SalesData`) to validate the data from the CSV file. The model defines the expected data types for each column:

* `name`: string
* `age`: integer
* `city`: string
* `sales`: float

If a row in the CSV file does not conform to this model, it is considered invalid, logged, and dropped from the data before aggregation.

## 5️⃣ Output

The script produces two outputs:

1.  **Console Output:**
    * Prints the aggregation results (total sales and average age per city) to the console.
    * Prints the first 5 rows from the `sales_summary` table in the SQLite database.

2.  **SQLite Database:**
    * Creates a local SQLite database file named `sales_data.db`.
    * Creates a table named `sales_summary` in the database, containing the aggregation results.

## Dependencies

* [pandas](https://pandas.pydata.org/): Data analysis and manipulation tool.
* [Pydantic](https://pydantic-docs.github.io/): Data validation and settings management.
* [psycopg2-binary](https://pypi.org/project/psycopg2-binary/): PostgreSQL adapter for Python (used for database interaction, even with SQLite via SQLAlchemy).
* [SQLAlchemy](https://www.sqlalchemy.org/): Python SQL toolkit and Object-Relational Mapper.

## Error Handling

The script includes error handling for the following:

* File not found when reading the CSV file.
* Errors during CSV file reading.
* Key errors during data aggregation.
* Errors when writing to the SQLite database.
* Data validation errors using Pydantic.

## Logging

The script uses the `logging` module to provide informative messages about its progress and any errors that occur.  Logs are written to the console.


## 🔧 Built With

- Python 3.x
- pandas
- pydantic
- psycopg2
- SQLAlchemy