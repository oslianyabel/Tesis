from email.message import EmailMessage
from colorama import Fore, init
from dotenv import load_dotenv
import psycopg2
from datetime import datetime
import smtplib, os
from core import tools2

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
        return conv

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
        "crear_generales": tools2.crear_generales,
        "get_generales_tool": tools2.get_generales_tool,
        "cuestionario": tools2.cuestionario,
        "Energux": tools2.Energux,
        "Myros": tools2.Myros,
        "Servidores": tools2.Servidores,
        "clean_chat": tools2.clean_chat,
        "redes_sociales": tools2.redes_sociales,
        "info_contacto": tools2.info_contacto,
        "get_datetime": tools2.get_datetime,
    }


def get_tools(user):
    if not user:
        generales = False
    else:
        generales = get_generales(user)
        
    chatbot = pg_fetch(
        table_name = "app_chatbot",
        filter = ["activo", True],
        fields = "*",
    )[0]

    id = chatbot[0]
    sys_prompt = chatbot[1]
    energux_prompt = chatbot[2]
    myros_prompt = chatbot[3]
    servidores_prompt = chatbot[4]
    fastos_pagus_prompt = chatbot[5]
    nombre = chatbot[6]
    activo = chatbot[7]
    X = chatbot[8]
    facebook = chatbot[9]
    instagram = chatbot[10]
    telegram = chatbot[11]
    whatsapp = chatbot[12]
    generales_prompt = chatbot[13]
    cuestionarios_prompt = chatbot[14]

    get_datetime = {
        "type": "function",
        "function": {
            "name": "get_datetime",
            "description": "Consulta la fecha actual",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": [],
            },
        },
    }
    redes_sociales = {
        "type": "function",
        "function": {
            "name": "redes_sociales",
            "description": "Consulta las redes sociales de la empresa",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": [],
            },
        },
    }
    get_generales_tool = {
        "type": "function",
        "function": {
            "name": "get_generales_tool",
            "description": "Consulta las generales asociadas a un usuario",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": [],
            },
        },
    }
    crear_generales = {
        "type": "function",
        "function": {
            "name": "crear_generales",
            "description": generales_prompt,
            "parameters": {
                "type": "object",
                "properties": {
                    "nombre_empresa": {
                        "type": "string",
                        "description": "Nombre de la empresa a la que pertenece el usuario."
                    },
                    "dir": {
                        "type": "string",
                        "description": "Dirección de la empresa a la que pertenece el usuario."
                    },
                    "mun": {
                        "type": "string",
                        "description": "Municipio al que pertenece la empresa del usuario."
                    },
                    "prov": {
                        "type": "string",
                        "description": "Provincia a la que pertenece la empresa del usuario."
                    },
                    "email": {
                        "type": "string",
                        "description": "Correo electrónico de la empresa del usuario."
                    },
                    "tel": {
                        "type": "string",
                        "description": "Teléfono de la empresa del usuario."
                    },
                    "nombre": {
                        "type": "string",
                        "description": "Nombre del usuario."
                    },
                    "apellidos": {
                        "type": "string",
                        "description": "Apellidos del usuario."
                    },
                    "cargo": {
                        "type": "string",
                        "description": "Cargo del usuario en su empresa."
                    }
                },
                "required": ["nombre_empresa", "dir", "mun", "prov", "email", "tel", "nombre", "apellidos", "cargo"]
            }
        }
    }
    info_contacto = {
        "type": "function",
        "function": {
            "name": "info_contacto",
            "description": "Consulta la información de contacto de Soluciones DTeam",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": [],
            },
        },
    }
    cuestionario = {
        "type": "function",
        "function": {
            "name": "cuestionario",
            "description": cuestionarios_prompt,
            "parameters": {
                "type": "object",
                "properties": {
                    "service_name": {
                        "type": "string",
                        "description": "Nombre del servicio solicitado por el usuario",
                    },
                },
                "required": ["service_name"],
            },
        },
    }
    clean_chat = {
        "type": "function",
        "function": {
            "name": "clean_chat",
            "description": "Borra la conversación actual. Se limpia el chat",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": [],
            },
        },
    }
    Energux = {
        "type": "function",
        "function": {
            "name": "Energux",
            "description": energux_prompt,
            "parameters": {
                "type": "object",
                "properties": {
                    "cantidad_usuarios": {"type": "integer", "description": "Cantidad de usuarios que trabajarán con el sistema."},
                    "entidad_consolidadora": {"type": "boolean", "description": "¿Su empresa funciona como una entidad que consolida los datos de otras entidades?"},
                    "entidad_subordinada": {"type": "boolean", "description": "¿Su empresa está subordinada a una entidad que consolida los datos de otras entidades?"},
                    "monedas_trabajo": {"type": "array", "items": {"type": "string"}, "description": "Tipos de moneda con que trabaja la Empresa"},
                    "centros_costo": {"type": "integer", "description": "Cantidad de centros de costo"},
                    "tarjetas_combustibles": {"type": "integer", "description": "Cantidad de tarjetas de combustible"},
                    "equipos": {"type": "integer", "description": "Cantidad de equipos"},
                    "choferes": {"type": "integer", "description": "Cantidad de choferes"},
                    "control_hojas_rutas": {"type": "boolean", "description": "¿Control de hojas de ruta?"},
                    "plan_consumo_vehiculos": {"type": "boolean", "description": "¿Plan de consumo de vehículos?"},
                    "modelo_portadores": {"type": "string", "description": "¿Utilización de los modelos para los Portadores(5073-CDA002)?"},
                    "sistema_contable_automatizado": {"type": "boolean", "description": "¿Sistema contable automatizado?"},
                    "sistema_contable_utilizado": {"type": "string", "description": "Sistema contable utilizado"},
                    "portadores": {"type": "string", "description": "Portadores que utilizan. ej: Diésel, Gasolinas"},
                    "plan_mensual_portador": {"type": "boolean", "description": "¿Hay definido un plan mensual para cada portador?"},
                    "registro_contadores_electricos": {"type": "boolean", "description": "¿Tienen registro de contadores eléctricos?"},
                    "registro_transformadores_electricos": {"type": "boolean", "description": "¿Tienen registro de transformadores eléctricos?"},
                    "plan_consumo_electrico": {"type": "boolean", "description": "¿Tienen definidos planes de consumo eléctrico?"},
                    "cuentas_control_combustible": {"type": "boolean", "description": "Descripción de las cuentas relacionadas con el control de combustible en la entidad"}
                },
                "required": ["cantidad_usuarios", "entidad_consolidadora", "entidad_subordinada", "monedas_trabajo", "centros_costo", "tarjetas_combustibles", "equipos", "choferes", "control_hojas_rutas", "plan_consumo_vehiculos", "modelo_portadores", "sistema_contable_automatizado", "sistema_contable_utilizado", "portadores", "plan_mensual_portador", "registro_contadores_electricos", "registro_transformadores_electricos", "plan_consumo_electrico", "cuentas_control_combustible"]
            }
        }
    }
    Myros = {
        "type": "function",
        "function": {
            "name": "Myros",
            "description": myros_prompt,
            "parameters": {
                "type": "object",
                "properties": {
                    "cantidad_usuarios": {
                        "type": "integer",
                        "description": "Cantidad de usuarios que trabajarán con el sistema (Especialista de Negocios, comercial, Asesor Jurídico)."
                    },
                    "cantidad_pc": {
                        "type": "integer",
                        "description": "Cantidad de PC en uso."
                    },
                    "entidad_consolidadora": {
                        "type": "boolean",
                        "description": "¿Su empresa funciona como una entidad que consolida los datos de otras entidades?"
                    },
                    "monedas_trabajo": {
                        "type": "array",
                        "items": {
                            "type": "string"
                        },
                        "description": "Tipos de moneda con que trabaja la Empresa (e.g., CUC, CUP)."
                    },
                    "contratos_a_personas_naturales": {
                        "type": "boolean",
                        "description": "¿Se emiten contratos a personas Naturales?"
                    },
                    "registro_contratos_actualizado": {
                        "type": "boolean",
                        "description": "¿Mantienen un registro de Contratos actualizado?"
                    },
                    "registro_clientes_proveedores_actualizado": {
                        "type": "boolean",
                        "description": "¿Mantienen un registro de clientes y proveedores actualizado?"
                    },
                    "registro_productos_servicios": {
                        "type": "boolean",
                        "description": "¿Mantienen un registro de los productos y servicios que ofertan y/o reciben?"
                    },
                    "sistema_contable_versat": {
                        "type": "boolean",
                        "description": "¿Cuentan con el Sistema Contable Versat Sarasola?"
                    },
                    "cuentas_gestion_contractual": {
                        "type": "object",
                        "properties": {
                            "cuenta_cup": {
                                "type": "string",
                                "description": "Cuenta CUP relacionada con la gestión contractual."
                            },
                            "cuenta_cuc": {
                                "type": "string",
                                "description": "Cuenta CUC relacionada con la gestión contractual."
                            }
                        },
                        "required": ["cuenta_cup", "cuenta_cuc"]
                    }
                },
                "required": [
                    "cantidad_usuarios",
                    "cantidad_pc",
                    "entidad_consolidadora",
                    "monedas_trabajo",
                    "contratos_a_personas_naturales",
                    "registro_contratos_actualizado",
                    "registro_clientes_proveedores_actualizado",
                    "registro_productos_servicios",
                    "sistema_contable_versat",
                    "cuentas_gestion_contractual"
                ]
            }
        }
    }
    Servidores = {
        "type": "function",
        "function": {
            "name": "Servidores",
            "description": servidores_prompt,
            "parameters": {
                "type": "object",
                "properties": {
                    "modo_conexion_red": {
                        "type": "string",
                        "enum": ["ADSL", "Modem", "Fibra óptica", "Otro"],
                        "description": "Modo de conexión a la red"
                    },
                    "nivel_conexion": {
                        "type": "object",
                        "properties": {
                            "intranet": {"type": "boolean", "description": "¿Conexión a Intranet?"},
                            "internet": {"type": "boolean", "description": "¿Conexión a Internet?"}
                        },
                        "description": "Nivel de conexión"
                    },
                    "cantidad_host_fisico": {
                        "type": "integer",
                        "description": "Cantidad de host físicos"
                    },
                    "cantidad_host_virtuales": {
                        "type": "integer",
                        "description": "Cantidad de host virtuales"
                    },
                    "servicios_a_instalar": {
                        "type": "object",
                        "properties": {
                            "controlador_dominio": {"type": "boolean", "description": "¿Instalar Controlador de Dominio?"},
                            "servidor_salvas": {"type": "boolean", "description": "¿Instalar Servidor de Salvas?"},
                            "proxy": {"type": "boolean", "description": "¿Instalar Proxy?"},
                            "servidor_correo": {"type": "boolean", "description": "¿Instalar Servidor de Correo?"},
                            "servidores_web": {"type": "boolean", "description": "¿Instalar Servidores Web?"},
                            "ftp": {"type": "boolean", "description": "¿Instalar FTP?"},
                            "jabber": {"type": "boolean", "description": "¿Instalar Jabber?"},
                            "servidor_nube": {"type": "boolean", "description": "¿Instalar Servidor Nube?"},
                            "wsus": {"type": "boolean", "description": "¿Instalar WSUS?"},
                            "cortafuego": {"type": "boolean", "description": "¿Instalar Cortafuego?"},
                            "smtp_relay": {"type": "boolean", "description": "¿Instalar SMTP Relay?"},
                            "otros": {"type": "boolean", "description": "¿Instalar otros servicios?"}
                        },
                        "description": "Servicios a instalar"
                    },
                    "ip_reservadas_dhcp": {
                        "type": "boolean",
                        "description": "¿IP reservadas en el DHCP?"
                    }
                },
                "required": [
                    "modo_conexion_red",
                    "nivel_conexion",
                    "cantidad_host_fisico",
                    "cantidad_host_virtuales",
                    "servicios_a_instalar",
                    "ip_reservadas_dhcp"
                ]
            }
        }
    }
    
    tools_con_generales = [get_datetime, redes_sociales, get_generales_tool, crear_generales, info_contacto, cuestionario, clean_chat, Energux, Myros, Servidores]

    tools_sin_generales = [get_datetime, crear_generales, get_generales_tool, cuestionario, clean_chat]
    
    return tools_con_generales if generales else tools_sin_generales


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
