import random
import pyodbc
from datetime import datetime, timedelta
from faker import Faker

# Inicializar Faker
fake = Faker()

# Establecer conexión a la base de datos
conn = pyodbc.connect(
    'DRIVER={SQL Server};'
    'SERVER=.;'
    'DATABASE=BDLazarte;'
    'Trusted_Connection=yes;'
)
cursor = conn.cursor()

def generar_hora():
    return fake.time()

def obtener_id_historia():
    cursor.execute("SELECT IDHistoria FROM HISTORIA_CLINICA")
    historias = cursor.fetchall()
    return [historia[0] for historia in historias]  # Devuelve una lista de IDs

def insert_fake_data():
    anamnesis_words = [
        "Dolor", "Fiebre", "Náuseas", "Tos", "Fatiga", "Vómitos", 
        "Mareos", "Cefalea", "Dolor abdominal", "Pérdida de apetito",
        "Cansancio", "Dolor lumbar", "Dolor pélvico", "Sangrado vaginal", 
        "Calambres", "Hinchazón", "Dificultad para respirar", "Palpitaciones", 
        "Pérdida de peso", "Aumento de peso", "Ansiedad", "Insomnio",
        "Amenorrea", "Dismenorrea", "Metrorragia", "Prurito", "Flujo vaginal anormal",
        "Micción frecuente", "Dolor en los senos", "Sensibilidad mamaria", 
        "Dolor articular", "Sudores nocturnos"
    ]

    plan_trabajo_words = [
        "Control prenatal", "Ecografía", "Anticonceptivos", "Examen pélvico", 
        "Papanicolaou", "Mamografía", "Control menstrual", "Suplementos de hierro", 
        "Planificación familiar", "Seguimiento postparto", "Cirugía ginecológica",
        "Tratamiento hormonal", "Control de fertilidad", "Terapia hormonal",
        "Biopsia endometrial"
    ]

    resultado_atencion_words = [
        "Mejoría", "Estable", "Empeoramiento", "Sin cambios", 
        "Alta médica", "Requiere seguimiento", "Crítico", 
        "Controlado", "Complicaciones", "Recuperación parcial", 
        "Sin complicaciones", "Recuperación completa", 
        "En observación", "Derivado a especialista", "Condición grave",
        "Requiere intervención quirúrgica", "Recuperación lenta", 
        "Respuesta favorable al tratamiento", "Sin respuesta al tratamiento"
    ]

    indicaciones_words = [
        "Tomar medicación cada 8 horas", "Reposo absoluto por 5 días", 
        "Mantener una dieta baja en grasas", "Evitar esfuerzos físicos", 
        "Hidratación adecuada", "Asistir a control en una semana", 
        "Aplicar compresas frías", "Evitar exposición al sol", 
        "Tomar analgésicos según sea necesario", "Seguir con fisioterapia", 
        "Monitorear la presión arterial", "Realizar ejercicios respiratorios", 
        "Evitar alimentos con alto contenido de sodio", "Mantener la herida limpia y seca",
        "Usar protector solar", "Evitar consumo de alcohol", 
        "Reducir el consumo de azúcar", "Controlar los niveles de glucosa", 
        "Descanso de al menos 8 horas", "Seguir tratamiento con antibióticos"
    ]

    # Obtener todos los IDHistoria de la tabla HISTORIA_CLINICA
    lista_id_historias = obtener_id_historia()
    if not lista_id_historias:
        print("No hay historias clínicas disponibles.")
        return

    # Iterar sobre la lista de IDs, comenzando desde el primero
    for IDHistoria in lista_id_historias:
        # Determinar cuántas veces se repetirá la historia clínica (entre 1 y 3)
        num_repeticiones = random.randint(1, 3)  

        for _ in range(num_repeticiones):
            Indicaciones = random.choice(indicaciones_words)
            IDReceta = random.randint(1, 1000000)
            HoraInicio = generar_hora()
            
            # Asegurar que HoraFin sea posterior a HoraInicio (agregando entre 1 y 3 horas)
            hora_inicio_dt = datetime.strptime(HoraInicio, "%H:%M:%S")
            HoraFin = (hora_inicio_dt + timedelta(hours=random.randint(1, 3))).time().strftime("%H:%M:%S")

            # Generar FechaAtencion entre un rango de fechas
            start_date = datetime(2020, 1, 1)
            end_date = datetime(2024, 9, 30)
            FechaAtencion = fake.date_time_between(start_date=start_date, end_date=end_date)

            Anammesis = random.choice(anamnesis_words)
            IDExamenClinico = random.randint(1, 1000000)
            ResultadoAtencion = random.choice(resultado_atencion_words)
            IDExamenAuxiliar = random.randint(1, 1000000)
            PlanTrabajo = random.choice(plan_trabajo_words)
            IDDoctor = random.randint(1, 250)
            IDPaciente = random.randint(1, 1000000)
            IDHospital = random.randint(1, 30)
            IDArea = random.randint(1, 3)
            IDServicio = random.randint(1, 30)

            # Insertar los datos en la tabla EXPEDIENTE_CLINICO
            try:
                cursor.execute(""" 
                    INSERT INTO EXPEDIENTE_CLINICO
                    (IDHistoria, Indicaciones, IDReceta, HoraInicio, HoraFin, FechaAtencion,
                     Anammesis, IDExamenClinico, ResultadoAtencion, IDExamenAuxiliar, PlanTrabajo, 
                     IDDoctor, IDPaciente, IDHospital, IDArea, IDServicio)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """, (IDHistoria, Indicaciones, IDReceta, HoraInicio, HoraFin, 
                          FechaAtencion, Anammesis, IDExamenClinico, ResultadoAtencion, IDExamenAuxiliar, 
                          PlanTrabajo, IDDoctor, IDPaciente, IDHospital, IDArea, IDServicio))
                
                # Confirmar cambios
                conn.commit()
                print("Registro insertado exitosamente.")
                
            except Exception as e:
                print("Error al insertar registro:", e)

# Generar registros
insert_fake_data()

# Cerrar conexión
cursor.close()
conn.close()
