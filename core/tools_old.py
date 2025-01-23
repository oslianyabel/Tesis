from datetime import datetime
import json
from core.utils_old import preparar_email, send_mail_list
from app.models import *


def crear_generales(usuario, nombre_empresa, dir, mun, prov, email, tel, nombre, apellidos, cargo):
    try:
        generales = Generales.objects.get(usuario = usuario)

        Generales.objects.update(
            usuario=usuario,
            nombre_empresa=nombre_empresa,
            dir=dir,
            mun=mun,
            prov=prov,
            email=email,
            tel=tel,
            nombre=nombre,
            apellidos=apellidos,
            cargo=cargo
        )
        print("Generales actualizadas")
        
        return "Generales actualizadas"
    
    except Exception as error:
        try:
            Generales.objects.create(
                usuario=usuario,
                nombre_empresa=nombre_empresa,
                dir=dir,
                mun=mun,
                prov=prov,
                email=email,
                tel=tel,
                nombre=nombre,
                apellidos=apellidos,
                cargo=cargo
            )
            print("Generales creadas.")
            
            return "Generales creadas."
        
        except Exception as error:
            print(error)
            
            return "Error creando las generales."
            
        
def get_generales_tool(usuario):
    try:
        generales = Generales.objects.get(usuario = usuario)
        print("Usuario con generales.")
        ans = {
            "usuario": generales.usuario.username,
            "nombre_empresa": generales.nombre_empresa,
            "dir": generales.dir,
            "mun": generales.mun,
            "prov": generales.prov,
            "email": generales.email,
            "tel": generales.tel,
            "nombre": generales.nombre,
            "apellidos": generales.apellidos,
            "cargo": generales.cargo
        }
        
        return json.dumps(ans)
    
    except Exception as error:
        print(f"Usuario sin generales. {error}")
        
        return "No hay generales asociadas al usuario."
    
    
def Energux(cantidad_usuarios: int, entidad_consolidadora: bool, entidad_subordinada: bool,
            monedas_trabajo: list[str], centros_costo: int, tarjetas_combustibles: int, equipos: int, 
            choferes: int, control_hojas_rutas: bool, plan_consumo_vehiculos: bool, modelo_portadores: str, 
            sistema_contable_automatizado: bool, sistema_contable_utilizado: str, portadores: str,
            plan_mensual_portador: bool, registro_contadores_electricos: bool, registro_transformadores_electricos: bool, 
            plan_consumo_electrico: bool, cuentas_control_combustible: str, generales):
    
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
    
    try:
        energux = Servicio.objects.filter(nombre = "EnerguX")[0]
        
    except Exception as error:
        print(f"No se encontró el servicio EnerguX. {error}")
        
        return "No se encontró el servicio EnerguX."
    
    Solicitud.objects.create(
        generales = generales,
        servicio = energux,
        cuestionario = datos_json,
    )
    print("Solicitud de Energux creada!")
    
    try:
        cuerpo = preparar_email(datos, generales, "Energux")
        send_mail_list("Solicitud de Contrato", cuerpo)
    except Exception as error:
        print(f"Error notificando lista de correos: {error}")
    
    return "Solicitud enviada correctamente."


def Myros(cantidad_usuarios, cantidad_pc, entidad_consolidadora, monedas_trabajo,
          contratos_a_personas_naturales, registro_contratos_actualizado,
          registro_clientes_proveedores_actualizado, registro_productos_servicios,
          sistema_contable_versat, cuentas_gestion_contractual, generales):
    
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
    
    try:
        myros = Servicio.objects.filter(nombre = "MyRos")[0]
        
    except Exception as error:
        print(f"No se encontró el servicio Myros. {error}")
        
        return "No se encontró el servicio Myros."
    
    Solicitud.objects.create (
        generales = generales,
        servicio = myros,
        cuestionario = datos_json,
    )
    print("Solicitud de Myros creada!")
    
    try:
        cuerpo = preparar_email(datos, generales, "Myros")
        send_mail_list("Solicitud de Contrato", cuerpo)
    except Exception as error:
        print(f"Error notificando lista de correos: {error}")
    
    return "Solicitud enviada correctamente."


def Servidores(modo_conexion_red, nivel_conexion, cantidad_host_fisico,cantidad_host_virtuales, 
               servicios_a_instalar, ip_reservadas_dhcp, generales):
    
    datos = {
        "modo_conexion_red": modo_conexion_red,
        "nivel_conexion": nivel_conexion,
        "cantidad_host_fisico": cantidad_host_fisico,
        "cantidad_host_virtuales": cantidad_host_virtuales,
        "servicios_a_instalar": servicios_a_instalar,
        "ip_reservadas_dhcp": ip_reservadas_dhcp,
    }
    datos_json = json.dumps(datos, indent=4)
    
    try:
        servidores = Servicio.objects.filter(nombre = "Servidores")[0]
        
    except Exception as error:
        print(f"No se encontró el servicio Servidores. {error}")
        
        return "No se encontró el servicio Servidores."
    
    Solicitud.objects.create(
        generales = generales,
        servicio = servidores,
        cuestionario = datos_json,
    )
    print("Solicitud de Servidores creada!")
    
    try:
        cuerpo = preparar_email(datos, generales, "Servidores")
        send_mail_list("Solicitud de Contrato", cuerpo)
    except Exception as error:
        print(f"Error notificando lista de correos: {error}")
    
    return "Solicitud enviada correctamente."


def cuestionario(servicio, usuario):
    Cliente_Pot.objects.create(
        usuario = usuario,
        servicio = servicio
    )
    if servicio.nombre.lower() == "energux":
        return f'<p>Complete y envíe este <a href="/media/documentos/Cuestionario_Energux_5.0.doc">cuestionario</a> por correo a <a href="mailto:negocios.ssp@desoft.cu">negocios.ssp@desoft.cu</a>.</p> (Las etiquetas html envialas en formato html)'
    
    elif servicio.nombre.lower() == "myros":
        return f'Complete y envíe este <a href="/media/documentos/Cuestionario_Myros.doc">cuestionario</a> por correo a negocios.ssp@desoft.cu'
    
    elif servicio.nombre.lower() == "servidores":
        return f'Complete y envíe este <a href="/media/documentos/Cuestionario_Servidores.doc">cuestionario</a> por correo a negocios.ssp@desoft.cu'
    
    elif servicio.nombre.lower() == "fastos-pagus":
        return f'Complete y envíe este <a href="/media/documentos/Cuestionario_Fastos-Pagus.doc">cuestionario</a> por correo a negocios.ssp@desoft.cu'
    
    else:
        return "Cuestionario no disponible."
    
    
def clean_chat(usuario, sys_prompt):
    try:
        chat = Conversacion.objects.get(usuario=usuario)
        
    except Conversacion.DoesNotExist:
        return "La conversación no existe."
    
    chat.mensaje_set.all().delete()
    sys_prompt += f" El usuario se llama: {usuario.username}. Refiérete a él por ese nombre."
    Mensaje.objects.create(
        conversacion=chat,
        texto=sys_prompt,
        enviado_por="system"
    )
    
    return "Conversación eliminada. Pídele al usuario que actualice la página para no ver los mensajes anteriores."


def redes_sociales():
    chatbot = ChatBot.objects.filter(activo = True)[0]
    ans = "A continuación se listan las redes sociales de SOLUCIONES DTEAM: \n"
    ans += f"{chatbot.facebook} \n"
    ans += f"{chatbot.instagram} \n"
    ans += f"{chatbot.X} \n"
    ans += f"{chatbot.telegram} \n"
    ans += f"{chatbot.whatsapp} \n"
    
    return ans


def info_contacto():
    contacto = Contacto.objects.filter(activo = True)[0]
    ans = f"Dirección de la empresa: {contacto.direccion} \n"
    ans += f"Correo de la empresa: {contacto.correo} \n"
    ans += f"Teléfono fijo de la empresa: {contacto.telefono_fijo} \n"
    ans += f"Teléfono móvil o celular de la empresa: {contacto.telefono_movil} \n"
    
    return ans
