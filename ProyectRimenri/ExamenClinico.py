import pyodbc

# Conexión a SQL Server
conn = pyodbc.connect(
    'DRIVER={SQL Server};'
    'SERVER=.;'
    'DATABASE=BDLazarte;'
    'Trusted_Connection=yes;'
)
cursor = conn.cursor()

# Obtener los IDSignosVitales y IDAntropometria de sus respectivas tablas
cursor.execute("SELECT IDSignosVitales FROM SIGNOS_VITALES")
signos_vitales = [row[0] for row in cursor.fetchall()]

cursor.execute("SELECT IDAntropometria FROM ANTROPOMETRIA")
antropometrias = [row[0] for row in cursor.fetchall()]

# Función para insertar datos en EXAMEN_CLINICO en lotes
def insert_fake_examen_clinico():
    total_registros = min(len(signos_vitales), len(antropometrias))  # Número total de registros será el menor entre los dos
    batch_size = 10000  # Tamaño del lote
    
    signos_vitales_index = 0
    antropometria_index = 0

    for i in range(0, total_registros, batch_size):
        examenes_batch = []

        # Crear lotes de EXAMEN_CLINICO
        while len(examenes_batch) < batch_size and signos_vitales_index < len(signos_vitales):
            # Usar los IDs en orden secuencial
            id_signos_vitales = signos_vitales[signos_vitales_index]
            id_antropometria = antropometrias[antropometria_index] if antropometria_index < len(antropometrias) else None
            
            # Incrementar los índices
            signos_vitales_index += 1
            antropometria_index += 1

            # Añadir a la lista de inserción
            examenes_batch.append((id_signos_vitales, id_antropometria))

        # Insertar el lote en la base de datos
        try:
            cursor.executemany("""
                INSERT INTO EXAMEN_CLINICO (IDSignosVitales, IDAntropometria)
                VALUES (?, ?)
            """, examenes_batch)
        except pyodbc.DataError as e:
            print("Error al insertar en la base de datos:", e)
            continue  # Continuar con el siguiente lote
        
        # Guardar los cambios en la base de datos
        conn.commit()
        print(f'{i + batch_size} registros de EXAMEN_CLINICO insertados...')

    print("Inserción de datos completada.")

# Ejecutar la inserción
insert_fake_examen_clinico()

# Cerrar la conexión
cursor.close()
conn.close()
