import pyodbc
import random
from datetime import timedelta

# Conectar a la base de datos de SQL Server
conn = pyodbc.connect(
    'DRIVER={SQL Server};'
    'SERVER=.;'
    'DATABASE=BDLazarte;'
    'Trusted_Connection=yes;'
)
cursor = conn.cursor()

# Obtener los IDDiagnostico de la tabla DIAGNOSTICO
cursor.execute("SELECT IDDiagnostico FROM DIAGNOSTICO")
diagnosticos = [row[0] for row in cursor.fetchall()]

# Obtener los datos de IDExpediente, IDHistoria y FechaAtencion de la tabla EXPEDIENTE_CLINICO
cursor.execute("SELECT IDExpediente, IDHistoria, FechaAtencion FROM EXPEDIENTE_CLINICO")
expedientes_clinicos = [(row[0], row[1], row[2]) for row in cursor.fetchall()]

# Verificar si hay datos en las tablas
if not diagnosticos:
    print("La tabla DIAGNOSTICO está vacía. Asegúrate de insertar datos primero.")
    cursor.close()
    conn.close()
    exit()

if not expedientes_clinicos:
    print("La tabla EXPEDIENTE_CLINICO está vacía. Asegúrate de insertar datos primero.")
    cursor.close()
    conn.close()
    exit()

# Set para almacenar combinaciones únicas de (IDExpediente, IDHistoria, IDDiagnostico)
inserted_combinations = set()

# Iterar sobre cada IDExpediente e IDHistoria
for id_expediente, id_historia, fecha_atencion in expedientes_clinicos:
    # Elegir un número aleatorio de diagnósticos entre 1 y 2
    num_diagnosticos = random.randint(1, 2)
    
    # Seleccionar diagnósticos aleatorios asegurando no repetir en la misma combinación
    selected_diagnosticos = random.sample(diagnosticos, k=num_diagnosticos)

    for id_diagnostico in selected_diagnosticos:
        # Evitar duplicados de (IDExpediente, IDHistoria, IDDiagnostico)
        if (id_expediente, id_historia, id_diagnostico) in inserted_combinations:
            continue

        # Generar valores para Tipo, Alta y Caso
        tipo = random.choice(['Presuntivo', 'Definitivo'])
        alta = 'SI' if random.random() > 0.5 else 'NO'
        caso = random.choice(['Nuevo', 'Recurrente', 'Crónico'])
        
        # Generar FechaDiagnostico dentro de los 2 días siguientes a FechaAtencion
        fecha_diagnostico = fecha_atencion + timedelta(days=random.randint(0, 2))

        # Insertar el registro en EXPEDIENTE_DIAGNOSTICO
        cursor.execute("""
            INSERT INTO EXPEDIENTE_DIAGNOSTICO (Tipo, Alta, Caso, FechaDiagnostico, IDExpediente, IDHistoria, IDDiagnostico)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (tipo, alta, caso, fecha_diagnostico, id_expediente, id_historia, id_diagnostico))

        # Añadir la combinación a los pares insertados
        inserted_combinations.add((id_expediente, id_historia, id_diagnostico))

# Confirmar la transacción
conn.commit()

# Cerrar la conexión
cursor.close()
conn.close()

print("Inserción completada: cada IDExpediente e IDHistoria tiene entre 1 y 2 diagnósticos.")
