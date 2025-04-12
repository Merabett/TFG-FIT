import snowflake.connector
import os

# Datos de conexión a Snowflake
SF_ACCOUNT = "IWUQOAY-EE75910"
SF_USER = "api_user"
SF_PASSWORD = "P@8xM9!zQ4vK#2dT"
SF_DATABASE = "NUTRIAPP_BBDD"
SF_SCHEMA = "PROCESSED_DATA"
SF_WAREHOUSE = "COMPUTE_WH"

def get_connection():
    """
    Establece y retorna la conexión a Snowflake.
    """
    try:
        conn = snowflake.connector.connect(
            user=SF_USER,
            password=SF_PASSWORD,
            account=SF_ACCOUNT,
            warehouse=SF_WAREHOUSE,
            database=SF_DATABASE,
            schema=SF_SCHEMA
        )
        return conn
    except Exception as e:
        print(f"Error al conectar a Snowflake: {e}")
        return None



def execute_query(query):
    """
    Ejecuta una consulta SQL en Snowflake y devuelve los resultados.
    """
    conn = get_connection()
    if conn is not None:
        try:
            cursor = conn.cursor()
            cursor.execute(query)
            results = cursor.fetchall()
            cursor.close()
            return results
        except Exception as e:
            print(f"Error al ejecutar la consulta: {e}")
            return None
        finally:
            conn.close()
    else:
        return None

def insert_data(query, data):
    """
    Inserta datos en la base de datos de Snowflake.
    """
    conn = get_connection()
    if conn is not None:
        try:
            cursor = conn.cursor()
            cursor.executemany(query, data)
            conn.commit()
            cursor.close()
            return True
        except Exception as e:
            print(f"Error al insertar datos: {e}")
            return False
        finally:
            conn.close()
    else:
        return False
