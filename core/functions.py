from colorama import Fore, init
import psycopg2
from datetime import datetime
import json
from core import utils

init(autoreset = True)


def crear_generales(user, nombre_empresa, dir, mun, prov, email, tel, nombre, apellidos, cargo):
    generales = utils.get_generales(user)
    if not generales:
        try:
            with psycopg2.connect(dbname="postgres", user="postgres", password="ofs", host="localhost", port="5432") as conn:
                with conn.cursor() as cur:
                    cur.execute(
                        "INSERT INTO app_generales (nombre_empresa, dir, mun, prov, email, tel, nombre, apellidos, cargo, usuario_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                        (nombre_empresa, dir, mun, prov, email, tel, nombre, apellidos, cargo, user.id)
                    )
            print(Fore.BLUE + f"Generales de {user.username} creadas")
            return "Generales creadas"

        except psycopg2.Error as exc:
            print(Fore.RED + f"Error creando generales: {exc}")
            return "Error creando generales"
        
    # actualizar
    try:
        with psycopg2.connect(dbname="postgres", user="postgres", password="ofs", host="localhost", port="5432") as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "UPDATE app_generales SET nombre_empresa=%s, dir=%s, mun=%s, prov=%s, email=%s, tel=%s, nombre=%s, apellidos=%s, cargo=%s WHERE usuario_id=%s",
                    (nombre_empresa, dir, mun, prov, email, tel, nombre, apellidos, cargo, user.id)
                )
        print(Fore.BLUE + f"Generales de {user.username} actualizadas")
        return "Generales actualizadas"

    except psycopg2.Error as exc:
        print(Fore.RED + f"Error actualizando generales: {exc}")
        return "Error actualizando generales"


def get_generales_tool(user):
    generales = utils.get_generales(user)
    if not generales:
        return f"El usuario {user.username} no tiene generales asociadas"
        
    try:
        ans = {
            "usuario": user.username,
            "nombre_empresa": generales[1],
            "dir": generales[2],
            "mun": generales[3],
            "prov": generales[4],
            "email": generales[5],
            "tel": generales[6],
            "nombre": generales[7],
            "apellidos": generales[8],
            "cargo": generales[9],
        }
        return json.dumps(ans)
    
    except Exception as exc:
        print(f"Error buscando generales: {exc}")
        return "Error buscando generales. Por favor intente más tarde"


def Energux(cantidad_usuarios: int, entidad_consolidadora: bool, entidad_subordinada: bool,
            monedas_trabajo: list[str], centros_costo: int, tarjetas_combustibles: int, equipos: int, 
            choferes: int, control_hojas_rutas: bool, plan_consumo_vehiculos: bool, modelo_portadores: str, 
            sistema_contable_automatizado: bool, sistema_contable_utilizado: str, portadores: str,
            plan_mensual_portador: bool, registro_contadores_electricos: bool, registro_transformadores_electricos: bool, 
            plan_consumo_electrico: bool, cuentas_control_combustible: str, generales, user):
    
    if not user or not generales:
        msg = "Usuarios sin autenticarse o sin generales asociadas no pueden solicitar servicios"
        print(Fore.YELLOW + msg)
        return msg
    
    datos = {
        "cantidad_usuarios": cantidad_usuarios,
        "entidad_consolidadora": entidad_consolidadora,
        "entidad_subordinada": entidad_subordinada,
        "monedas_trabajo": monedas_trabajo,
        "centros_costo": centros_costo,
        "tarjetas_combustibles": tarjetas_combustibles,
        "equipos": equipos,
        "choferes": choferes,
        "control_hojas_rutas": control_hojas_rutas,
        "plan_consumo_vehiculos": plan_consumo_vehiculos,
        "modelo_portadores": modelo_portadores,
        "sistema_contable_automatizado": sistema_contable_automatizado,
        "sistema_contable_utilizado": sistema_contable_utilizado,
        "portadores": portadores,
        "plan_mensual_portador": plan_mensual_portador,
        "registro_contadores_electricos": registro_contadores_electricos,
        "registro_transformadores_electricos": registro_transformadores_electricos,
        "plan_consumo_electrico": plan_consumo_electrico,
        "cuentas_control_combustible": cuentas_control_combustible
    }
    datos_json = json.dumps(datos, indent=4)

    energux = utils.get_service("Energux")
    if not energux:
        return "Error creando la solicitud. Por favor intente más tarde"

    try:
        with psycopg2.connect(dbname="postgres", user="postgres", password="ofs", host="localhost", port="5432") as conn:
            with conn.cursor() as cur:
                cur.execute (
                    "INSERT INTO app_solicitud (cuestionario, fecha, servicio_id, generales_id) VALUES (%s, %s, %s, %s)",
                    (datos_json, datetime.now(), energux[0], generales[0])
                )
        print(Fore.BLUE + f"Solicitud de Energux creada por {user.username}")

    except psycopg2.Error as exc:
        print(Fore.RED + f"Error creando solicitud de Energux: {exc}")
        return "Error creando solicitud de Energux"
    
    try:
        cuerpo = utils.preparar_email(datos, generales, "Energux", user)
        utils.send_email_list("Solicitud de Energux", cuerpo)
        
    except Exception as exc:
        print(Fore.RED + f"Error notificando lista de correos: {exc}")
        return "Solicitud de Energux creada pero falló la notificación a los supervisores de la empresa"
    
    return "Solicitud enviada correctamente"


def Myros(cantidad_usuarios, cantidad_pc, entidad_consolidadora, monedas_trabajo,
          contratos_a_personas_naturales, registro_contratos_actualizado,
          registro_clientes_proveedores_actualizado, registro_productos_servicios,
          sistema_contable_versat, cuentas_gestion_contractual, generales, user):
    
    if not user or not generales:
        msg = "Usuarios sin autenticarse o sin generales asociadas no pueden solicitar servicios"
        print(Fore.YELLOW + msg)
        return msg
    
    datos = {
        "cantidad_usuarios": cantidad_usuarios,
        "cantidad_pc": cantidad_pc,
        "entidad_consolidadora": entidad_consolidadora,
        "monedas_trabajo": monedas_trabajo,
        "contratos_a_personas_naturales": contratos_a_personas_naturales,
        "registro_contratos_actualizado": registro_contratos_actualizado,
        "registro_clientes_proveedores_actualizado": registro_clientes_proveedores_actualizado,
        "registro_productos_servicios": registro_productos_servicios,
        "sistema_contable_versat": sistema_contable_versat,
        "cuentas_gestion_contractual": cuentas_gestion_contractual,
    }
    
    datos_json = json.dumps(datos, indent=4)
    
    myros = utils.get_service("Myros")
    if not myros:
        return "Error creando la solicitud. Por favor intente más tarde"

    try:
        with psycopg2.connect(dbname="postgres", user="postgres", password="ofs", host="localhost", port="5432") as conn:
            with conn.cursor() as cur:
                cur.execute (
                    "INSERT INTO app_solicitud (cuestionario, fecha, servicio_id, generales_id) VALUES (%s, %s, %s, %s)",
                    (datos_json, datetime.now(), myros[0], generales[0])
                )
        print(Fore.BLUE + f"Solicitud de Myros creada por {user.username}")

    except psycopg2.Error as exc:
        print(Fore.RED + f"Error creando solicitud de Myros: {exc}")
        return "Error creando solicitud de Myros"
    
    try:
        cuerpo = utils.preparar_email(datos, generales, "Myros", user)
        utils.send_email_list("Solicitud de Myros", cuerpo)
        
    except Exception as exc:
        print(Fore.RED + f"Error notificando lista de correos: {exc}")
        return "Solicitud de Myros creada pero falló la notificación a los supervisores de la empresa"
    
    return "Solicitud enviada correctamente"


def Servidores(modo_conexion_red, nivel_conexion, cantidad_host_fisico,cantidad_host_virtuales, 
               servicios_a_instalar, ip_reservadas_dhcp, generales, user):
    
    if not user or not generales:
        msg = "Usuarios sin autenticarse o sin generales asociadas no pueden solicitar servicios"
        print(Fore.YELLOW + msg)
        return msg
    
    datos = {
        "modo_conexion_red": modo_conexion_red,
        "nivel_conexion": nivel_conexion,
        "cantidad_host_fisico": cantidad_host_fisico,
        "cantidad_host_virtuales": cantidad_host_virtuales,
        "servicios_a_instalar": servicios_a_instalar,
        "ip_reservadas_dhcp": ip_reservadas_dhcp,
    }

    datos_json = json.dumps(datos, indent=4)
    
    servidores = utils.get_service("Servidores")[0]
    if not servidores:
        return "Error creando la solicitud. Por favor intente más tarde"
    
    try:
        with psycopg2.connect(dbname="postgres", user="postgres", password="ofs", host="localhost", port="5432") as conn:
            with conn.cursor() as cur:
                cur.execute (
                    "INSERT INTO app_solicitud (cuestionario, fecha, servicio_id, generales_id) VALUES (%s, %s, %s, %s)",
                    (datos_json, datetime.now(), servidores[0], generales[0])
                )
        print(Fore.BLUE + f"Solicitud de Servidores creada por {user.username}")

    except psycopg2.Error as exc:
        print(Fore.RED + f"Error creando solicitud de Servidores: {exc}")
        return "Error creando solicitud de Servidores"
        
    try:
        cuerpo = utils.preparar_email(datos, generales, "Servidores", user)
        utils.send_email_list("Solicitud de Servidores", cuerpo)
        
    except Exception as exc:
        print(Fore.RED + f"Error notificando lista de correos: {exc}")
        return "Solicitud de Servidores creada pero falló la notificación a los supervisores de la empresa"
    
    return "Solicitud enviada correctamente"


def cuestionario(service_name, user):
    if not user:
        msg = "Usuarios sin autenticar no pueden solicitar cuestionarios"
        print(Fore.YELLOW + msg)
        return msg
    
    service = utils.get_service(service_name)

    if not service:
        print(Fore.YELLOW + f"El servicio {service_name} no existe")
        return "El servicio no existe"
    
    try:
        with psycopg2.connect(dbname="postgres", user="postgres", password="ofs", host="localhost", port="5432") as conn:
            with conn.cursor() as cur:
                cur.execute (
                    "INSERT INTO app_cliente_pot (usuario_id, servicio_id, fecha) VALUES (%s, %s, %s)",
                    (user.id, service[0], datetime.now())
                )
        print(Fore.BLUE + f"Cliente potencial {user.username} agregado")
    except psycopg2.Error as exc:
        print(f"Error occurred: {exc}")

    if service[1].lower() == "energux":
        return f'<p>Complete y envíe este <a href="/media/documentos/Cuestionario_Energux_5.0.doc">cuestionario</a> por correo a <a href="mailto:negocios.ssp@desoft.cu">negocios.ssp@desoft.cu</a>.</p> (Las etiquetas html envialas en formato html)'
    
    elif service[1].lower() == "myros":
        return f'Complete y envíe este <a href="/media/documentos/Cuestionario_Myros.doc">cuestionario</a> por correo a negocios.ssp@desoft.cu'
    
    elif service[1].lower() == "servidores":
        return f'Complete y envíe este <a href="/media/documentos/Cuestionario_Servidores.doc">cuestionario</a> por correo a negocios.ssp@desoft.cu'
    
    elif service[1].lower() == "fastos-pagus":
        return f'Complete y envíe este <a href="/media/documentos/Cuestionario_Fastos-Pagus.doc">cuestionario</a> por correo a negocios.ssp@desoft.cu'
    
    else:
        return "Cuestionario no disponible"


def clean_chat(user):
    if not user:
        msg = "No se puede limpiar el chat de un usuario sin autenticar"
        print(Fore.YELLOW + msg)
        return msg
    try:
        chat = utils.pg_fetch("app_conversacion", ("id", user.id), fields="id")

        if not chat:
            return "La conversación no existe"
        
        chat_id = chat[0][0]
        sys_prompt = utils.get_sys_prompt()
        
        with psycopg2.connect(dbname="postgres", user="postgres", password="ofs", host="localhost", port="5432") as conn:
            with conn.cursor() as cur:
                cur.execute("DELETE FROM app_mensaje WHERE conversacion_id = %s", (chat_id,))
                
                # Insert the new system message
                sys_prompt += f" El usuario se llama: {user.username}. Refiérete a él por ese nombre"
                cur.execute("INSERT INTO app_mensaje (conversacion_id, texto, enviado_por, fecha_envio) VALUES (%s, %s, %s, %s)",
                            (chat_id, sys_prompt, "system", datetime.now()))
        
        return "Conversación eliminada. Pídele al usuario que actualice la página para no ver los mensajes anteriores"
    
    except psycopg2.Error as exc:
        print(f"Error interacting with the database: {exc}")
        return "Ocurrió un error al limpiar la conversación"


def redes_sociales(user):
    # Fetch the first active ChatBot
    chatbot_data = utils.pg_fetch('app_chatbot', filter=('activo', True), fields='facebook, instagram, "X", telegram, whatsapp')
    
    if not chatbot_data:
        return "No active chatbots found"
    
    facebook, instagram, x, telegram, whatsapp = chatbot_data[0]
    ans = "A continuación se listan las redes sociales de SOLUCIONES DTEAM: \n"
    ans += f"{facebook} \n"
    ans += f"{instagram} \n"
    ans += f"{x} \n"
    ans += f"{telegram} \n"
    ans += f"{whatsapp} \n"
    
    return ans


def info_contacto(user):
    # Fetch the first active Contact
    contacto_data = utils.pg_fetch('app_contacto', ('activo', True), 'direccion, correo, telefono_fijo, telefono_movil')
    
    if not contacto_data:
        return "No active contacts found"
    
    direccion, correo, telefono_fijo, telefono_movil = contacto_data[0]
    ans = f"Dirección de la empresa: {direccion} \n"
    ans += f"Correo de la empresa: {correo} \n"
    ans += f"Teléfono fijo de la empresa: {telefono_fijo} \n"
    ans += f"Teléfono móvil o celular de la empresa: {telefono_movil} \n"
    
    return ans


def get_datetime(user):
    return datetime.now().strftime('%Y-%m-%d')


if __name__ == "__main__":
    class UserDummy:
        def __init__(self, id, username):
            self.id = id
            self.username = username


    #print(utils2.get_service("Energux"))

    user = UserDummy(1, "usuario1")
    nombre_empresa = "Mi Empresa S.A."
    dir = "Calle Falsa 123"
    mun = "Madrid"
    prov = "Madrid"
    email = "contacto@miempresa.com"
    tel = "123456789"
    nombre = "Juan"
    apellidos = "Pérez"
    cargo = "Gerente"

    resultado = crear_generales(user, nombre_empresa, dir, mun, prov, email, tel, nombre, apellidos, cargo)
    print(resultado)
