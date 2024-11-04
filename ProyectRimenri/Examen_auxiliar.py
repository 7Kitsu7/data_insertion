import pyodbc
from faker import Faker
import random
from datetime import datetime

# Configuración de Faker
fake = Faker('es_ES')  # Faker en español

# Conexión a SQL Server
conn = pyodbc.connect(
    'DRIVER={ODBC Driver 17 for SQL Server};'
    'SERVER=.;'
    'DATABASE=BDLazarte;'
    'Trusted_Connection=yes;'
)
cursor = conn.cursor()

# Lista de resultados y indicaciones comunes en ginecología y obstetricia
resultados = [
    "Normal", "Anomalía detectada", "Signos de infección", "Ecografía sin hallazgos", "Niveles hormonales bajos",
    "Positivo para infección", "Presencia de quistes", "Embarazo confirmado", "Desarrollo fetal adecuado",
    "Anomalía en líquido amniótico", "Resultados inconclusos", "Marcador tumoral negativo", 
    "Feto en posición correcta", "Gestación múltiple", "Positivo para ITS", "Niveles normales de glucosa"
]

indicaciones = [
    "Reposo absoluto", "Control en 1 mes", "Examen complementario", "Consulta con especialista",
    "Inicio de tratamiento hormonal", "Monitoreo continuo", "Prueba repetida en 2 semanas",
    "Cirugía recomendada", "Consulta ginecológica de seguimiento", "Control ecográfico cada 2 semanas",
    "Revisión obstétrica mensual", "Repetir pruebas en 1 mes", "Evaluación adicional necesaria", 
    "Análisis de laboratorio adicionales", "Iniciar tratamiento inmediato", "Suspender actividad física"
]

# Inserción masiva de registros
batch_size = 10000  # Tamaño de lote para insertar en bloques
records = []

for _ in range(1000000):
    resultado = random.choice(resultados)  # Escoger un resultado aleatorio
    fecha = fake.date_time_between(start_date='-60y', end_date='now')  # Fecha aleatoria dentro de los últimos 2 años
    indicacion = random.choice(indicaciones)  # Escoger una indicación médica aleatoria
    id_prueba = random.randint(1, 1000000)  # IDPrueba entre 1 y 1000000 (asumiendo que ya hay registros en la tabla PRUEBA)
    
    records.append((resultado, fecha, indicacion, id_prueba))

    # Insertar en lotes para optimizar la inserción
    if len(records) == batch_size:
        cursor.executemany('''
            INSERT INTO EXAMEN_AUXILIAR (Resultado, Fecha, Indicacion, IDPrueba)
            VALUES (?, ?, ?, ?)
        ''', records)
        conn.commit()
        records = []  # Limpiar el lote después de cada inserción

# Insertar los registros restantes
if records:
    cursor.executemany('''
        INSERT INTO EXAMEN_AUXILIAR (Resultado, Fecha, Indicacion, IDPrueba)
        VALUES (?, ?, ?, ?)
    ''', records)
    conn.commit()

print("Inserción completada.")
conn.close()
