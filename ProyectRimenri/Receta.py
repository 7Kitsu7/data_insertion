import pyodbc
from faker import Faker
import random

# Conectar a la base de datos de SQL Server
conn = pyodbc.connect(
    'DRIVER={SQL Server};'
    'SERVER=.;'
    'DATABASE=BDLazarte;'
    'Trusted_Connection=yes;'
)
cursor = conn.cursor()

# Crear instancia de Faker
fake = Faker()

# Lista ampliada de recomendaciones ginecológicas
recomendaciones_medicas = [
    # Cuidados prenatales
    "Tomar ácido fólico diariamente durante el embarazo",
    "Realizar ultrasonido de control cada trimestre",
    "Controlar los niveles de glucosa mensualmente",
    "Realizar ecografía morfológica en la semana 20",
    "Iniciar clases de preparación para el parto",
    "Evitar el consumo de café y bebidas energéticas",
    "Realizar análisis de sangre y orina mensuales",
    "Asistir a control prenatal cada 4 semanas",
    "Mantener una dieta rica en hierro y calcio",
    "Evitar viajar durante el tercer trimestre de embarazo",
    
    # Cuidados postnatales
    "Iniciar ejercicios de suelo pélvico tras el parto",
    "Realizar chequeo postnatal a las 6 semanas del parto",
    "Tomar vitamina D si se opta por lactancia materna",
    "Evitar relaciones sexuales durante las primeras 6 semanas postparto",
    "Realizar masajes perineales para evitar dolor postparto",
    "Asistir a consultas de control postnatal para evaluar cicatrización",
    "Mantener una adecuada higiene vaginal postparto",
    
    # Terapias hormonales y menopausia
    "Consultar sobre la terapia de reemplazo hormonal",
    "Tomar calcio y vitamina D para prevenir osteoporosis",
    "Realizar ejercicios de bajo impacto para mantener la movilidad",
    "Evitar el consumo de tabaco durante la menopausia",
    "Mantener hidratación adecuada para evitar resequedad vaginal",
    
    # Medicación y tratamientos
    "Tomar la dosis de hierro prescrita por el médico",
    "Aplicar crema vaginal según indicación médica",
    "Seguir la terapia hormonal sin interrupciones",
    "Tomar multivitamínicos prenatales cada mañana",
    "Aplicar pomada de progesterona en caso de recomendación médica",
    "Administrar oxitocina según indicaciones en el trabajo de parto",
    "Evitar automedicarse sin consulta médica previa",
    
    # Hábitos saludables
    "Evitar el consumo de alcohol y tabaco durante el embarazo",
    "Hacer caminatas diarias de 30 minutos",
    "Realizar ejercicios de Kegel para fortalecer el suelo pélvico",
    "Mantener una alimentación rica en fibra para evitar estreñimiento",
    "Consumir al menos 2 litros de agua al día",
    "Dormir al menos 8 horas diarias para una buena recuperación",
    
    # Otras recomendaciones ginecológicas
    "Realizar una citología vaginal cada año",
    "Mantener una higiene adecuada para evitar infecciones vaginales",
    "Evitar el uso excesivo de productos de higiene íntima",
    "Realizar un examen de mamas cada mes",
    "Realizar una mamografía cada dos años a partir de los 40 años",
    "Evitar el uso de ropa interior ajustada",
    "Asistir a control ginecológico anual para detección de patologías"
]

# Generar e insertar 1 millón de datos con recomendaciones más amplias y coherentes
for _ in range(1000000):
    recomendacion = random.choice(recomendaciones_medicas)
    cursor.execute("""
        INSERT INTO RECETA (Recomendacion)
        VALUES (?)
    """, recomendacion)

# Confirmar la transacción
conn.commit()

# Cerrar la conexión
cursor.close()
conn.close()

print("Inserción completada RECETA.")
