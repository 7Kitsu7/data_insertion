import pyodbc
import random

# Configuración de conexión a SQL Server
conn = pyodbc.connect(
    'DRIVER={SQL Server};'
    'SERVER=.;'
    'DATABASE=BDLazarte;'
    'Trusted_Connection=yes;'
)
cursor = conn.cursor()

# Obtener todos los IDDoctor existentes de la tabla DOCTOR
cursor.execute("SELECT IDDoctor FROM DOCTOR")
doctors = cursor.fetchall()
doctor_ids = [doctor[0] for doctor in doctors]

# Obtener todos los IDEspecialidad existentes de la tabla ESPECIALIDAD
cursor.execute("SELECT IDEspecialidad FROM ESPECIALIDAD")
especialidades = cursor.fetchall()
especialidad_ids = [esp[0] for esp in especialidades]

# Función para asignar especialidades a doctores
def insert_fake_doctor_especialidad():
    for doctor_id in doctor_ids:
        # Asignar entre 1 y 2 especialidades a cada doctor
        num_especialidades = random.randint(1, 2)  # Máximo 2 especialidades por doctor
        especialidades_asignadas = random.sample(especialidad_ids, num_especialidades)

        for especialidad_id in especialidades_asignadas:
            # SQL para insertar en la tabla DOCTOR_ESPECIALIDAD
            cursor.execute("""
                INSERT INTO DOCTOR_ESPECIALIDAD (IDDoctor, IDEspecialidad)
                VALUES (?, ?)
            """, (doctor_id, especialidad_id))

    conn.commit()
    print("Asignación de especialidades completada.")

# Ejecutar la inserción de datos
insert_fake_doctor_especialidad()

# Cerrar la conexión
cursor.close()
conn.close()
