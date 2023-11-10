import psycopg2

def get_connection():
    connection = psycopg2.connect(
        user= 'postgres',
        host= 'localhost',
        dbname= 'Hermes',
        password= 'hermest4',
        port= '5432'
    )
    return connection