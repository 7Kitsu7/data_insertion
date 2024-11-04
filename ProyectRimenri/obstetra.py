import random
import pyodbc
from faker import Faker
from time import time

# Inicializar Faker con nombres y apellidos comunes de Perú
fake = Faker()

# Conectar a la base de datos SQL Server
conn = pyodbc.connect(
    'DRIVER={SQL Server};'
    'SERVER=.;'
    'DATABASE=BDLazarte;'
    'Trusted_Connection=yes;'
)
cursor = conn.cursor()

# Obtener todos los DNIs existentes en las tablas Paciente y Medico para evitar duplicados
def obtener_dnis_existentes():
    dnis_existentes = set()

    # Obtener DNIs de la tabla Paciente
    cursor.execute("SELECT DNI FROM PACIENTE")
    dnis_existentes.update([row[0] for row in cursor.fetchall()])

    # Obtener DNIs de la tabla Medico
    cursor.execute("SELECT DNI FROM DOCTOR")
    dnis_existentes.update([row[0] for row in cursor.fetchall()])

    return dnis_existentes

# Generar DNI único que no esté en la lista de DNIs existentes
def generar_dni_unico(dnis_existentes):
    while True:
        dni = fake.random_number(digits=8, fix_len=True)
        if dni not in dnis_existentes:
            dnis_existentes.add(dni)
            return dni

# Generar datos para la tabla OBSTETRA en lotes
def poblar_obstetra(total_registros, batch_size=100):
    dnis_existentes = obtener_dnis_existentes()
    start_time = time()

    for i in range(0, total_registros, batch_size):
        obstetras = []
        
        for _ in range(batch_size):
            nombre = fake.first_name()
            apellido = fake.last_name()
            dni = generar_dni_unico(dnis_existentes)
            obstetras.append((nombre, apellido, dni))
        
        # Insertar el lote en la tabla OBSTETRA
        cursor.executemany('''
            INSERT INTO OBSTETRA (Nombre, Apellido, DNI)
            VALUES (?, ?, ?)
        ''', obstetras)
        
        # Guardar el lote en la base de datos
        conn.commit()
        
        # Progreso
        print(f"{i + batch_size}/{total_registros} registros insertados ({(i + batch_size) / total_registros * 100:.2f}%)")

    # Tiempo total
    end_time = time()
    print(f"Poblamiento completado en {end_time - start_time:.2f} segundos.")

# Llamada a la función para poblar la tabla OBSTETRA con 1 millón de registros
poblar_obstetra(300)

# Cerrar la conexión
conn.close()
