import pyodbc
from faker import Faker
import random
from datetime import datetime, timedelta

# Configuración de conexión a SQL Server
conn = pyodbc.connect(
    'DRIVER={SQL Server};'
    'SERVER=.;'
    'DATABASE=BDLazarte;'
    'Trusted_Connection=yes;'
)
cursor = conn.cursor()

# Crear una instancia de Faker
fake = Faker('es_ES')  # Usar español de España para generar datos en español

# Obtener los IDs de la tabla SEGURO
cursor.execute("SELECT IDSeguro FROM SEGURO")
seguros = [row[0] for row in cursor.fetchall()]

# Obtener los IDs de la tabla GRUPO_SANGUINEO
cursor.execute("SELECT IDGrupoSanguineo FROM GRUPO_SANGUINEO")
grupos_sanguineos = [row[0] for row in cursor.fetchall()]

# Obtener DNI, Telefono y Email de la tabla DOCTOR
cursor.execute("SELECT DNI, Telefono, Email FROM DOCTOR")
doctores_data = cursor.fetchall()

# Crear conjuntos con los datos existentes en la tabla DOCTOR
doctores_dnis = set(row[0] for row in doctores_data)
doctores_telefonos = set(row[1] for row in doctores_data)
doctores_emails = set(row[2] for row in doctores_data)

# Generar conjuntos únicos para DNI, Telefono y Email
unique_dnis = doctores_dnis.copy()
unique_telefonos = doctores_telefonos.copy()
unique_emails = doctores_emails.copy()

# Definir la fecha mínima de registro (1 de enero de 1952) y la fecha actual (hoy)
min_fecha_registro = datetime(1952, 1, 1).date()  # Convertir a 'date'
fecha_actual = datetime.now().date()  # Convertir a 'date' para comparación

# Opciones para el estado civil
estados_civiles = ['Soltero', 'Casado', 'Divorciado', 'Viudo']

# Función para calcular la fecha de registro en función de la fecha de nacimiento
def generar_fecha_registro(fecha_nac):
    min_fecha_registro_paciente = min_fecha_registro
    max_fecha_registro = min(fecha_nac + timedelta(days=40 * 365), fecha_actual)
    
    if max_fecha_registro <= fecha_nac:
        raise ValueError("La fecha de registro no puede ser anterior a la fecha de nacimiento.")
    
    return fake.date_between_dates(max(min_fecha_registro_paciente, fecha_nac + timedelta(days=1)), max_fecha_registro)

# Función para insertar pacientes en lotes
def insert_fake_pacientes(num):
    batch_size = 10000  # Tamaño del lote
    for i in range(0, num, batch_size):
        patients_batch = []
        for _ in range(batch_size):
            while True:
                dni = fake.random_int(min=10000000, max=99999999)
                if dni not in unique_dnis:
                    unique_dnis.add(dni)
                    break

            while True:
                telefono = fake.random_int(min=900000000, max=999999999)
                telefono_str = str(telefono)
                if telefono_str not in unique_telefonos and len(telefono_str) == 9:
                    unique_telefonos.add(telefono_str)
                    break

            while True:
                email = f"{fake.user_name()}@{random.choice(['gmail.com', 'hotmail.com'])}"
                if email not in unique_emails:
                    unique_emails.add(email)
                    break

            sexo = random.choice(['M', 'F'])
            nombre = fake.first_name_male()[:50] if sexo == 'M' else fake.first_name_female()[:50]
            apellido = (fake.last_name() + ' ' + fake.last_name())[:100]

            fecha_nac = fake.date_of_birth(minimum_age=18, maximum_age=90)
            fecha_nac_str = fecha_nac.strftime('%Y-%m-%d')

            direccion = fake.address().replace("\n", ", ")[:50]

            fecha_registro = generar_fecha_registro(fecha_nac)
            fecha_registro_str = fecha_registro.strftime('%Y-%m-%d %H:%M:%S')

            id_seguro = random.choice(seguros)
            id_grupo_sanguineo = random.choice(grupos_sanguineos)

            # Seleccionar un estado civil aleatorio
            estado_civil = random.choice(estados_civiles)

            # Añadir a la lista de pacientes
            patients_batch.append((nombre, apellido, str(dni), fecha_nac_str, sexo, direccion, telefono_str, email, fecha_registro_str, id_seguro, id_grupo_sanguineo, estado_civil))

        # Insertar el lote de pacientes en la base de datos
        try:
            cursor.executemany("""
                INSERT INTO PACIENTE (Nombre, Apellido, DNI, FechaNac, Sexo, Direccion, Telefono, Email, FechaRegistro, IDSeguro, IDGrupoSanguineo, EstadoCivil)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, patients_batch)
        except pyodbc.DataError as e:
            print("Error al insertar en la base de datos:", e)
            continue  # O puedes usar `break` si prefieres detener la ejecución

        conn.commit()
        print(f'{i + batch_size} registros de pacientes insertados...')

    print("Inserción de datos de pacientes completada.")

# Ejecutar la inserción de datos
insert_fake_pacientes(1000000)  # Insertar 1 millón de registros en la tabla PACIENTE

# Cerrar la conexión
cursor.close()
conn.close()
