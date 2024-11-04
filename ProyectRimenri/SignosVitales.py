import pyodbc
from faker import Faker
import random

# Configuración de conexión a SQL Server
conn = pyodbc.connect(
    'DRIVER={SQL Server};'
    'SERVER=.;'
    'DATABASE=BDLazarte;'
    'Trusted_Connection=yes;'  # Usar autenticación de Windows
)
cursor = conn.cursor()

# Crear una instancia de Faker
fake = Faker()

# Función para insertar datos falsos en la tabla SIGNOS_VITALES
def insert_fake_signos_vitales(num):
    for _ in range(num):
        # Generación de datos falsos
        presion_arterial = f"{random.randint(90, 180)}/{random.randint(60, 120)}"  # Por ejemplo, 120/80
        presion_venosa = f"{random.uniform(1.0, 20.0):.2f} mmHg" if random.random() > 0.2 else None  # A veces NULL
        temperatura = f"{random.uniform(36.0, 41.0):.1f}"  # Ej. 37.5 grados
        frecuencia_cardiaca = f"{random.randint(60, 120)} bpm"  # Latidos por minuto
        frecuencia_respiratoria = f"{random.randint(12, 25)} rpm"  # Respiraciones por minuto
        saturacion_o2 = f"{random.randint(85, 100)}%" if random.random() > 0.1 else None  # A veces NULL
        fio2 = f"{random.randint(21, 100)}%" if random.random() > 0.3 else None  # A veces NULL

        # SQL para insertar los signos vitales
        cursor.execute("""
            INSERT INTO SIGNOS_VITALES (PresionArterial, PresionVenosaCentral, TemperaturaCorporal, FrecuenciaCardiaca, FrecuenciaRespiratoria, SaturacionO2, FiO2)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (presion_arterial, presion_venosa, temperatura, frecuencia_cardiaca, frecuencia_respiratoria, saturacion_o2, fio2))

        # Guardar los cambios en la base de datos cada 10000 inserciones
        if _ % 10000 == 0:
            conn.commit()
            print(f'{_} signos vitales insertados...')

    conn.commit()
    print("Inserción de signos vitales completada.")

# Ejecutar la inserción de datos
insert_fake_signos_vitales(1000000)  # Insertar 1 millon de registros de signos vitales

# Cerrar la conexión
cursor.close()
conn.close()
