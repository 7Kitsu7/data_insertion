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
fake = Faker('es_ES')  # Usar español de España

# Función para insertar datos falsos en la tabla DOCTOR
def insert_fake_doctors(num):
    unique_dnis = set()
    unique_telefonos = set()
    unique_emails = set()
    unique_colegiaturas = set()

    for _ in range(num):
        # Genera un DNI único
        while True:
            dni = fake.random_int(min=10000000, max=99999999)
            if dni not in unique_dnis:
                unique_dnis.add(dni)
                break
        
        # Genera un Teléfono único
        while True:
            telefono = fake.random_int(min=900000000, max=999999999)  # Rango de teléfonos móviles en Perú
            if telefono not in unique_telefonos:
                unique_telefonos.add(telefono)
                break
        
        # Genera un Email único con dominios específicos
        while True:
            # Genera un nombre de usuario aleatorio
            nombre_usuario = fake.user_name()
            # Elige un dominio aleatorio entre gmail y hotmail
            dominio = random.choice(['gmail.com', 'hotmail.com'])
            email = f"{nombre_usuario}@{dominio}"
            if email not in unique_emails:
                unique_emails.add(email)
                break
        
        # Genera un NrColegiatura único en el rango de 27000 - 150000
        while True:
            nr_colegiatura = fake.random_int(min=27000, max=150000)
            if nr_colegiatura not in unique_colegiaturas:
                unique_colegiaturas.add(nr_colegiatura)
                break
        
        # Genera Nombre y Apellidos (dos apellidos)
        nombre = fake.first_name()
        apellido = f"{fake.last_name()} {fake.last_name()}"  # Combina dos apellidos

        # SQL para insertar en la tabla DOCTOR
        cursor.execute("""
            INSERT INTO DOCTOR (Nombre, Apellido, DNI, Telefono, Email, NrColegiatura)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (nombre, apellido, str(dni), str(telefono), email, str(nr_colegiatura)))

        # Guardar los cambios en la base de datos cada 10 inserciones
        if _ % 10 == 0:
            conn.commit()
            print(f'{_} registros de doctores insertados...')

    conn.commit()  # Asegura que los últimos cambios se guarden
    print("Inserción de datos de doctores completada.")

# Ejecutar la inserción de datos
insert_fake_doctors(250)  # Insertar 250 registros en la tabla DOCTOR

# Cerrar la conexión
cursor.close()
conn.close()
