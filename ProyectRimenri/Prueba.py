import pyodbc
from faker import Faker
import random

# Configuración de Faker
fake = Faker('es_ES')  # Faker en español

# Conexión a SQL Server
conn = pyodbc.connect(
    'DRIVER={SQL Server};'
    'SERVER=.;'
    'DATABASE=BDLazarte;'
    'Trusted_Connection=yes;'
)
cursor = conn.cursor()

# Lista de nombres de prueba relacionados con ginecología y obstetricia
nombres_prueba = [
    "Evaluación Hormonal Integral", "Examen de Salud Fetal", "Estudio de Bienestar Embrionario",
    "Test de Perfil Materno", "Evaluación de Riesgo Obstétrico", "Monitoreo de Salud Prenatal",
    "Detección de Anomalías Gestacionales", "Perfil Fisiológico Femenino", "Screening Preconcepcional",
    "Prueba de Compatibilidad Genética", "Evaluación del Estado Gestacional", "Control de Desarrollo Embrionario",
    "Estudio de Salud Femenina Integral", "Detección de Marcadores Obstétricos", "Análisis de Metabolismo Prenatal",
    "Evaluación de Salud Genital", "Monitoreo de Salud Embrionaria", "Test de Viabilidad Embrionaria",
    "Evaluación de Flujo Placentario", "Prueba de Seguimiento Fetal"
]

# Inserción masiva de registros
batch_size = 10000  # Tamaño de lote para insertar en bloques
records = []

for _ in range(1000000):
    nombre_prueba = random.choice(nombres_prueba)  # Escoger un nombre de prueba aleatorio
    id_tipo_prueba = random.randint(1, 56)
    id_laboratorio = random.randint(1, 10)
    records.append((nombre_prueba, id_tipo_prueba, id_laboratorio))

    # Insertar en lotes para optimizar la inserción
    if len(records) == batch_size:
        cursor.executemany('''
            INSERT INTO PRUEBA (NombrePrueba, IDTipoPrueba, IDLaboratorio)
            VALUES (?, ?, ?)
        ''', records)
        conn.commit()
        records = []  # Limpiar el lote después de cada inserción

# Insertar los registros restantes
if records:
    cursor.executemany('''
        INSERT INTO PRUEBA (NombrePrueba, IDTipoPrueba, IDLaboratorio)
        VALUES (?, ?, ?)
    ''', records)
    conn.commit()

print("Inserción completada.")
conn.close()
