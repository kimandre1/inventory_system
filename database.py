import mysql.connector, yaml
from mysql.connector import MySQLConnection, Error
import mysql.connector

def connect_info():
    with open("config.yml", "r") as yaml_file:
        config = yaml.safe_load(yaml_file)

    return (
        config["database"]["user"],
        config["database"]["password"],
        config["database"]["host"],
        config["database"]["port"],
        config["database"]["name"]
    )

# Call the function to get the connection information
DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME = connect_info()

# Print the values
print(DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME, sep="\n")

def connect_to_database():
    with open("config.yml", "r") as yaml_file:
        config = yaml.safe_load(yaml_file)

    return {
        'host': config["database"]["host"],
        'user': config["database"]["user"],
        'password': config["database"]["password"],
        'database': config["database"]["name"],
        'port': config["database"]["port"],
    }

def execute_stored_procedure(procedure_name):
    try:
        # Read database configuration from the config file using function
        config = connect_to_database()

        # Establish a connection to the MySQL database
        conn = mysql.connector.connect(**config)

        # Create a cursor to execute SQL queries
        cursor = conn.cursor()

        try:
            # Call the stored procedure specified by procedure_name
            cursor.callproc(procedure_name)

            # Process the results of the stored procedure
            results = []
            for result in cursor.stored_results():
                results.extend(result.fetchall())

            return results

        finally:
            # Close the cursor
            cursor.close()

    except Error as e:
        raise e
    finally:
        # Close the connection
        if conn.is_connected():
            conn.close()

if __name__ == '__main__':
    try:
        # Example: Call the stored procedure 'GetVareinfo'
        result = execute_stored_procedure('GetVareinfo')
        print(result)
    except Error as e:
        print(e)








