from email.message import EmailMessage
from colorama import Fore, init
from dotenv import load_dotenv
import psycopg2
from datetime import datetime
import smtplib, os
from core import functions

load_dotenv()

init(autoreset=True)

EMAIL = os.getenv('EMAIL')
EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')
EMAIL_HOST = os.getenv('EMAIL_HOST')


def send_email(to, subject, message):
    email = EmailMessage()
    email["from"] = EMAIL
    email["to"] = to
    email["subject"] = subject
    email.set_content(message)

    try:
        print("Enviando notificación por email a", Fore.BLUE + f"{to}")
        with smtplib.SMTP(EMAIL_HOST, port = 587) as smtp:
            smtp.starttls()
            smtp.login(EMAIL, EMAIL_PASSWORD)
            smtp.sendmail(EMAIL, to, email.as_string())
            print("Email enviado!")
            return True
            
    except Exception as exc:
        print(Fore.RED + f'Error enviando email: {exc}')
        return False


def send_email_list(subject, message):
    correos = pg_fetch (
        table_name = "app_correo",
        filter = ["activo", True],
        fields = "correo1, correo2, correo3, correo4, correo5, correo6, correo7, correo8, correo9, correo10"
    )
    if not correos:
        print(Fore.YELLOW + "No se encontraron correos en la BD")
        return False
    
    correos = correos[0]
    for correo in correos:
        if correo:
            send_email(correo, subject, message)


def pg_fetch(table_name, filter = False, fields = "*"):
    with psycopg2.connect(dbname="postgres", user="postgres", password="ofs", host="localhost", port="5432") as conn:
        if filter:
            with conn.cursor() as cur:
                cur.execute(f"SELECT {fields} FROM {table_name} WHERE {filter[0]} = %s", (filter[1],))
                return cur.fetchall()
        
        with conn.cursor() as cur:
            cur.execute(f"SELECT {fields} FROM {table_name}")
            return cur.fetchall()
        

def get_generales(user):
    generales =  pg_fetch (
        table_name = "app_generales",
        filter = ["usuario_id", user.id]
    )
    if not generales:
        print(Fore.YELLOW + f"El usuario {user.username} no tiene generales asociadas")
        return False
    
    return generales[0]


def get_service(service_name):
    servicio = pg_fetch("app_servicio", ["nombre", service_name], "id, nombre")
    if servicio:
        return servicio[0]
    else:
        print(Fore.YELLOW + f"Servicio {service_name} no encontrado")
        return False


def get_or_create_chat(user):
    conv = pg_fetch (
        table_name = "app_conversacion",
        filter = ["usuario_id", user.id],
    )
    if conv:
        print("Conversacion encontrada")
        return conv[0]

    try:
        with psycopg2.connect(dbname="postgres", user="postgres", password="ofs", host="localhost", port="5432") as conn:
            with conn.cursor() as cur:
                cur.execute (
                    "INSERT INTO app_conversacion (fecha_inicio, usuario_id) VALUES (%s, %s)",
                    (datetime.now(), user.id)
                )

        print(Fore.BLUE + "Conversacion creada")
        return conv
    
    except psycopg2.Error as exc:
        print(f"Error occurred: {exc}")
        return False


def get_functions():
    return {
        "crear_generales": functions.crear_generales,
        "get_generales_tool": functions.get_generales_tool,
        "cuestionario": functions.cuestionario,
        "Energux": functions.Energux,
        "Myros": functions.Myros,
        "Servidores": functions.Servidores,
        "clean_chat": functions.clean_chat,
        "redes_sociales": functions.redes_sociales,
        "info_contacto": functions.info_contacto,
        "get_datetime": functions.get_datetime,
    }


def preparar_email(cuestionario, generales, servicio, user):
    ans = "Generales:\n"
    ans += f"Usuario: {user.username}\n"
    ans += f"Empresa: {generales[1]}\n"
    ans += f"Dirección: {generales[2]}\n"
    ans += f"Municipio: {generales[3]}\n"
    ans += f"Provincia: {generales[4]}\n"
    ans += f"Email: {generales[5]}\n"
    ans += f"Teléfono: {generales[6]}\n"
    ans += f"Nombre del representante: {generales[7]}\n"
    ans += f"Apellidos del representante: {generales[8]}\n"
    ans += f"Cargo del representante: {generales[9]}\n"
    
    ans += "="*50
    ans += f"\nCuestionario de {servicio}\n"
    
    for key, value in cuestionario.items():
        ans += f"{key}: {value}\n"
        
    return ans


def get_sys_prompt():
    chatbot_data = pg_fetch("app_chatbot", filter=("activo", True), fields="sys_prompt")
    if not chatbot_data:
        return "No active chatbot found."
    
    sys_prompt = chatbot_data[0][0]
    
    # Información de la empresa
    sobre_nosotros_data = pg_fetch("app_sobrenosotros", filter=("activo", True), fields="parrafo, parrafo2")
    if sobre_nosotros_data:
        sn = sobre_nosotros_data[0]
        sys_prompt += "A continuación se muestra información detallada de la empresa: \n"
        sys_prompt += f"{sn[0]} \n {sn[1]} \n"
    
    # Servicios de SOLUCIONES DTEAM
    servicios_data = pg_fetch("app_servicio", filter=("activo", True), fields="nombre, categoria_id, descripcion, votos, puntos_promedio")
    if servicios_data:
        sys_prompt += "A continuación se listan los nombres, categorías, descripciones, cantidad de votos y puntuación promedio de los servicios que ofrece SOLUCIONES DTEAM:\n"
        for s in servicios_data:
            sys_prompt += f"- Nombre: {s[0]}, Categoria: {s[1]}, Descripción: {s[2]}, Votos: {s[3]}, Rating: {s[4]} \n"
    
    # Preguntas frecuentes
    preguntas_data = pg_fetch("app_preguntafrecuente", filter=("activo", True), fields="pregunta, respuesta")
    if preguntas_data:
        sys_prompt += "A continuación se listan las preguntas frecuentes con sus respuestas: \n"
        for pf in preguntas_data:
            sys_prompt += f"Pregunta: {pf[0]} Respuesta: {pf[1]} \n"
    
    return sys_prompt


if __name__ == "__main__":
    class UserDummy:
        def __init__(self, id, username):
            self.id = id
            self.username = username


    user = UserDummy(1, "yo")

    print(get_or_create_chat(user))
