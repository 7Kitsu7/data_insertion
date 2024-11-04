from faker import Faker
import pyodbc
import random

fake = Faker()

# Conexión a la base de datos
conn = pyodbc.connect(
    'DRIVER={SQL Server};'
    'SERVER=.;'
    'DATABASE=BDLazarte;'
    'Trusted_Connection=yes;'
)
cursor = conn.cursor()

# Consultar los IDs de Expediente e Historia filtrados
cursor.execute("""
    SELECT ec.IDExpediente, ec.IDHistoria
    FROM EXPEDIENTE_CLINICO ec
    JOIN AREA_HOSPITALARIA ah ON ec.IDArea = ah.IDArea
    JOIN SERVICIO_HOSPITALARIO sh ON ec.IDServicio = sh.IDServicio
    JOIN PACIENTE p ON ec.IDPaciente = p.IDPaciente
    WHERE ah.Nombre = 'Hospitalización'
      AND (sh.Nombre = 'Obstetricia' OR sh.Nombre = 'Ginecología')
      AND p.Sexo = 'F'
""")
expedientes_historia = cursor.fetchall()

# Verifica que haya datos en la tabla filtrada
if not expedientes_historia:
    print("No se encontraron registros en EXPEDIENTE_CLINICO con las condiciones especificadas.")
else:
    # La cantidad de registros a insertar será igual a la cantidad de pares disponibles
    num_registros = len(expedientes_historia)

    # Preparamos la lista de registros
    registros_partograma = []

    # Obtener todos los IDs de bebé disponibles
    cursor.execute("SELECT IDBebe FROM BEBE")
    bebes_disponibles = [row[0] for row in cursor.fetchall()]

    # Verifica que haya bebés disponibles
    if not bebes_disponibles:
        print("No hay bebés disponibles para insertar.")
    else:
        # Almacenar los ID de bebés que se han usado
        usados_bebes = set()

        for _ in range(num_registros):
            id_expediente, id_historia = random.choice(expedientes_historia)  # Selecciona un par aleatorio de IDs
            hora_inicio = fake.time()  # Hora aleatoria
            
            # Obtener un obstetra aleatorio
            cursor.execute("SELECT IDObstetra FROM OBSTETRA")
            obstetras = [row[0] for row in cursor.fetchall()]
            id_obstetra = random.choice(obstetras) if obstetras else None

            frecuencia_cardiaca_fetal = f"https://drive.google.com/drive/folders/1RmB2QY037JCOW5ONyLqe5D8n6X0YRvF6?usp=drive_link/{fake.uuid4()}"
            dilatacion_cervical = f"https://drive.google.com/drive/folders/1XT2MK_erUf51yLY4Vz8wsiEQRSGqztJI?usp=drive_link/{fake.uuid4()}"
            liquido_amniotico = f"https://drive.google.com/drive/folders/16T_pmfV0wqjOuZ8mG65hZw2dtfZ93e5R?usp=drive_link/{fake.uuid4()}"
            moldeamiento = f"https://drive.google.com/drive/folders/1EcAN06UWb06CGOmvFmhNZeHsHqg4z7D4?usp=drive_link/{fake.uuid4()}"
            variedad_posicion = f"https://drive.google.com/drive/folders/1bQhnVWUFzmiEE56A3ABf4d07xio2qyJe?usp=drive_link/{fake.uuid4()}"

            # Seleccionar un bebé único que no haya sido usado
            id_bebe = None
            while id_bebe is None or id_bebe in usados_bebes:
                id_bebe = random.choice(bebes_disponibles)

            # Agregar el ID de bebé a la lista de usados
            usados_bebes.add(id_bebe)

            # Agregamos el registro a la lista
            registros_partograma.append((id_expediente, id_historia, hora_inicio, id_obstetra, frecuencia_cardiaca_fetal,
                                          dilatacion_cervical, liquido_amniotico, moldeamiento, variedad_posicion, id_bebe))

        # Inserción masiva de registros
        insert_query = """
        INSERT INTO PARTOGRAMA (IDExpediente, IDHistoria, HoraInicio, IDObstetra, FrecuenciaCardiacaFetal, 
                                DilatacionCervical, LiquidoAmniotico, Moldeamiento, VariedadPosicion, IDBebe)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """

        try:
            cursor.executemany(insert_query, registros_partograma)
            conn.commit()  # Confirmamos la transacción
            print("Registros insertados con éxito.")
        except Exception as e:
            print("Error al insertar los registros:", e)
        finally:
            conn.close()
