import pyodbc
import random

# Conectar a la base de datos de SQL Server
conn = pyodbc.connect('DRIVER={SQL Server};'
                      'SERVER=.;'
                      'DATABASE=BDLazarte;'
                      'Trusted_Connection=yes;')
cursor = conn.cursor()

# Obtener los IDs de las recetas
cursor.execute("SELECT IDReceta FROM RECETA")
recetas = cursor.fetchall()
receta_ids = [receta[0] for receta in recetas]

# Obtener los IDs de los medicamentos
cursor.execute("SELECT IDMedicamento FROM MEDICAMENTO")
medicamentos = cursor.fetchall()
medicamento_ids = [medicamento[0] for medicamento in medicamentos]

# Verificar si hay datos en las tablas
if not receta_ids:
    print("La tabla RECETA está vacía. Asegúrate de insertar datos primero.")
    cursor.close()
    conn.close()
    exit()

if not medicamento_ids:
    print("La tabla MEDICAMENTO está vacía. Asegúrate de insertar datos primero.")
    cursor.close()
    conn.close()
    exit()

# Usar un conjunto para llevar un registro de las combinaciones ya insertadas
inserted_pairs = set()

# Iterar sobre cada IDReceta
for id_receta in receta_ids:
    # Elegir un número aleatorio de medicamentos entre 1 y 3
    num_medicamentos = random.randint(1, 3)

    # Elegir medicamentos aleatorios, asegurando que no se repitan para la misma receta
    selected_medicamentos = random.sample(medicamento_ids, k=num_medicamentos)

    for id_medicamento in selected_medicamentos:
        # Generar valores aleatorios para Cantidad, Dosis, Frecuencia y Duración
        cantidad = str(random.randint(1, 10)) + ' unidades'  # Ejemplo: "3 unidades"
        dosis = random.choice(['200 mg', '400 mg', '500 mg', '10 UI'])  # Ejemplo: elegir de opciones predefinidas
        frecuencia = random.choice(['Diaria', 'Cada 8 horas', 'Cada 12 horas', 'Cada 6 horas', 'Según necesidad'])
        duracion = str(random.randint(1, 30)) + ' días'  # Ejemplo: "7 días"

        # Insertar en la tabla RECETA_MEDICAMENTO
        cursor.execute("""
            INSERT INTO RECETA_MEDICAMENTO (IDReceta, IDMedicamento, Cantidad, Dosis, Frecuencia, Duracion)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (id_receta, id_medicamento, cantidad, dosis, frecuencia, duracion))

        # Añadir la combinación a los pares insertados
        inserted_pairs.add((id_receta, id_medicamento))

# Confirmar la transacción
conn.commit()

# Cerrar la conexión
cursor.close()
conn.close()

print("Inserción completada: cada IDReceta tiene entre 1 y 3 IDMedicamento.")