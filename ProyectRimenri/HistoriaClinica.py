import pyodbc
from faker import Faker

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

# Obtener los IDPaciente y FechaRegistro de la tabla PACIENTE
cursor.execute("SELECT IDPaciente, FechaRegistro FROM PACIENTE")
pacientes_data = cursor.fetchall()

# Función para insertar historias clínicas en lotes
def insert_fake_historias_clinicas():
    batch_size = 10000  # Tamaño del lote
    total_pacientes = len(pacientes_data)
    
    for i in range(0, total_pacientes, batch_size):
        historias_batch = []
        for paciente in pacientes_data[i:i + batch_size]:
            id_paciente = paciente[0]
            fecha_registro = paciente[1]  # Usar la fecha de registro como fecha de creación
            
            # Añadir a la lista de historias clínicas sin observaciones
            historias_batch.append((fecha_registro, id_paciente))
        
        # Insertar el lote de historias clínicas en la base de datos
        try:
            cursor.executemany("""
                INSERT INTO HISTORIA_CLINICA (FechaCreacion, IDPaciente)
                VALUES (?, ?)
            """, historias_batch)
        except pyodbc.DataError as e:
            print("Error al insertar en la base de datos:", e)
            continue  # Continuar con el siguiente lote
        
        # Guardar los cambios en la base de datos
        conn.commit()

        print(f'{i + batch_size} registros de historias clínicas insertados...')

    print("Inserción de datos de historias clínicas completada.")

# Ejecutar la inserción de datos
insert_fake_historias_clinicas()

# Cerrar la conexión
cursor.close()
conn.close()
