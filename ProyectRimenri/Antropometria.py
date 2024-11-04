import pyodbc
from faker import Faker
import random

# Configuración de conexión a SQL Server
conn = pyodbc.connect(
    'DRIVER={SQL Server};'
    'SERVER=.;'
    'DATABASE=BDLazarte;'
    'Trusted_Connection=yes;'
)
cursor = conn.cursor()

# Crear una instancia de Faker
fake = Faker()

# Función para insertar datos falsos en la tabla ANTROPOMETRIA
def insert_fake_anthropometry(num):
    for _ in range(num):
        peso = round(random.uniform(50.0, 120.0), 2)  # Generar peso entre 50kg y 120kg
        talla = round(random.uniform(1.5, 2.0), 2)  # Generar talla entre 1.5m y 2.0m
        perimetro_abdominal = f"{random.randint(60, 120)} cm"  # Perímetro abdominal en cm

        # SQL para insertar en la tabla ANTROPOMETRIA
        cursor.execute("""
            INSERT INTO ANTROPOMETRIA (Peso, Talla, PerimetroAbdominal)
            VALUES (?, ?, ?)
        """, (peso, talla, perimetro_abdominal))

        # Guardar los cambios en la base de datos cada 10000 inserciones
        if _ % 10000 == 0:
            conn.commit()
            print(f'{_} registros de antropometría insertados...')

    conn.commit()
    print("Inserción de datos de antropometría completada.")

# Ejecutar la inserción de datos
insert_fake_anthropometry(1000000)  # Insertar 1 millon de registros en la tabla ANTROPOMETRIA

# Cerrar la conexión
cursor.close()
conn.close()
