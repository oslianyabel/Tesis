from openai import OpenAI
from dotenv import load_dotenv
import json, os
from app.models import *
from core import tools, utils

load_dotenv()

AVANGENIO_API_KEY = os.getenv('AVANGENIO_API_KEY')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
ENVIRONMENT = os.getenv('ENVIRONMENT')
if ENVIRONMENT == "prod":
    client = OpenAI(
        base_url="https://apigateway.avangenio.net",
        api_key=AVANGENIO_API_KEY
    )
    model = "radiance"
else:
    client = OpenAI(
        api_key=OPENAI_API_KEY
    )
    model = "gpt-4o-mini"
    
available_functions = {
    "crear_generales": tools.crear_generales,
    "get_generales_tool": tools.get_generales_tool,
    "cuestionario": tools.cuestionario,
    "Energux": tools.Energux,
    "Myros": tools.Myros,
    "Servidores": tools.Servidores,
    "clean_chat": tools.clean_chat,
    "redes_sociales": tools.redes_sociales,
    "info_contacto": tools.info_contacto,
}


def get_sys_prompt():
    chatbot = ChatBot.objects.filter(activo = True)[0]
    sys_prompt = chatbot.sys_prompt
    
    sys_prompt += "A continuación se muestra información detallada de la empresa: \n"
    sn = SobreNosotros.objects.filter(activo = True)[0]
    sys_prompt += f"{sn.parrafo} \n {sn.parrafo2} \n"
    
    sys_prompt += "A continuación se listan los nombres, categorías, descripciones, cantidad de votos y puntuación promedio de los servicios que ofrece SOLUCIONES DTEAM:\n"
    servicios = Servicio.objects.filter(activo = True)
    for s in servicios:
        sys_prompt += f"- Nombre:{s.nombre}, Categoria: {s.categoria}, Descripción: {s.descripcion}, Votos: {s.votos}, Rating: {s.puntos_promedio} \n"
        
    sys_prompt += "A continuación se listas las preguntas frecuentes con sus respuestas: \n"
    preguntas = PreguntaFrecuente.objects.filter(activo = True)
    for pf in preguntas:
        sys_prompt += f"Pregunta: {pf.pregunta} Respuesta: {pf.respuesta} \n"
        
    return sys_prompt


def run_conversation2(new_msg: str):
    sys_prompt = get_sys_prompt()
    sys_prompt += " El usuario no se ha autenticado. Pídele en todos tus mensajes que inicie sesión tocando el boton de la derecha de la barra superior para poder gozar de todas las funcionalidades del asistente!"
    messages = [
        {"role": "system", "content": sys_prompt},
        {"role": "user", "content": new_msg}
    ]
    try:
        print("Generando respuesta del modelo.")
        response = client.chat.completions.create(
            model=model,
            messages=messages,
        )
        response_message = response.choices[0].message
    except Exception as error:
        print(error)
        return "Lo sentimos, ha ocurrido un error, realice la consulta más tarde.", False
    
    tool_calls = response_message.tool_calls
    if not tool_calls:
        return response_message.content, True
    else:
        return "El usuario debe autenticarse para realizar esta acción.", False
    

def get_tools(generales = False):
    print("Cargando prompts de herramientas externas.")
    chatbot = ChatBot.objects.filter(activo = True)[0]
    generales_prompt = chatbot.generales_prompt
    cuestionarios_prompt = chatbot.cuestionarios_prompt
    energux_prompt = chatbot.energux_prompt
    myros_prompt = chatbot.myros_prompt
    servidores_prompt = chatbot.servidores_prompt
    fastos_pagus_prompt = chatbot.fastos_pagus_prompt

    print(f"generales_prompt: {generales_prompt}")
    print(f"cuestionarios_prompt: {cuestionarios_prompt}")
    print(f"energux_prompt: {energux_prompt}")
    print(f"myros_prompt: {myros_prompt}")
    print(f"servidores_prompt: {servidores_prompt}")
    print(f"fastos_pagus_prompt: {fastos_pagus_prompt}")
    print("="*150)

    tools_con_generales = [
        {
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
        },
        {
            "type": "function",
            "function": {
                "name": "get_generales_tool",
                "description": "Consulta las generales asociadas a un usuario.",
            },
        },
        {
            "type": "function",
            "function": {
                "name": "redes_sociales",
                "description": "Consulta las redes sociales de la empresa.",
            },
        },
        {
            "type": "function",
            "function": {
                "name": "info_contacto",
                "description": "Consulta la información de contacto de la empresa.",
            },
        },
        {
            "type": "function",
            "function": {
                "name": "cuestionario",
                "description": cuestionarios_prompt,
                "parameters": {
                    "type": "object",
                    "properties": {
                        "servicio": {
                            "type": "string",
                            "description": "Nombre del servicio solicitado por el usuario.",
                        },
                    },
                    "required": ["servicio"],
                },
            },
        },
        {
            "type": "function",
            "function": {
                "name": "clean_chat",
                "description": "Borra la conversación actual. Se limpia el chat.",
            },
        },
        {
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
        },
        {
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
        },
        {
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
                            "description": "Cantidad de host físico"
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
        },
    ]

    tools_sin_generales = [
        {
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
        },
        {
            "type": "function",
            "function": {
                "name": "get_generales_tool",
                "description": "Consulta las generales asociadas a un usuario.",
            },
        },
        {
            "type": "function",
            "function": {
                "name": "cuestionario",
                "description": cuestionarios_prompt,
                "parameters": {
                    "type": "object",
                    "properties": {
                        "servicio": {
                            "type": "string",
                            "description": "Nombre del servicio solicitado por el usuario.",
                        },
                    },
                    "required": ["servicio"],
                },
            },
        },
        {
            "type": "function",
            "function": {
                "name": "clean_chat",
                "description": "Borra la conversación actual. Se limpia el chat.",
            },
        }
    ]
    
    return tools_con_generales if generales else tools_sin_generales


""" 
 * Genera la próxima respuesta del chatbot en una conversación
 * @param {django.contrib.auth.models.User} usuario - Usuario que está realizando la consulta
 * @param {str} new_msg - Nuevo mensaje del usuario
 * @param {List<dict>} messages - Lista de mensajes de la conversación actual
 * @returns {(str, bool)} - Tupla con la respuesta del chatbot y una bandera indicando si la operación fue exitosa
 """
def run_conversation(usuario, new_msg, messages=None):
    if not messages:
        print("Chat sin mensajes.")
        sys_prompt = get_sys_prompt()
        sys_prompt += f". El usuario se llama: {usuario}. Refiérete a él por ese nombre."
        messages = [
            {"role": "system", "content": sys_prompt},
            {"role": "user", "content": new_msg}
        ]
    else:
        messages.append({"role": "user", "content": new_msg})
        
    generales = utils.get_generales(usuario)
    tools_ = get_tools(generales)
        
    try:
        print("Generando respuesta del modelo.")
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            tools=tools_,
            tool_choice="auto",
        )
        response_message = response.choices[0].message
    except Exception as error:
        print(error)
        return "Lo sentimos, ha ocurrido un error, realice la consulta más tarde.", False
    tool_calls = response_message.tool_calls
    if not tool_calls:
        return response_message.content, True
    else:
        ok = True
        print("Llamada a herramenta.")
        messages.append(response_message)
        
        for tool_call in tool_calls:
            try:
                function_name = tool_call.function.name
                print(function_name)
                function_to_call = available_functions[function_name]
                function_args = json.loads(tool_call.function.arguments)
                print(function_args)
                
                if function_name == 'cuestionario':
                    nombre_serv = function_args["servicio"]
                    try:
                        servicio = Servicio.objects.filter(nombre__iexact = nombre_serv)[0]
                        function_response = function_to_call(servicio=servicio, usuario=usuario)
                    except Exception as error:
                        print(f"El servicio no existe: {error}")
                        function_response = "El servicio no existe."
                        
                elif function_name == "crear_generales":
                    function_response = tools.crear_generales(usuario=usuario, **function_args)
                    
                elif function_name == "clean_chat":
                    sys_prompt = get_sys_prompt()
                    function_response = tools.clean_chat(usuario, sys_prompt)
                    
                elif function_name == "get_generales_tool":
                    function_response = tools.get_generales_tool(usuario)
                    
                elif function_name in ["Energux", "Myros", "Servidores"]:
                    try:
                        generales = utils.get_generales(usuario)
                        if not generales:
                            print("Usuario sin generales.")
                            function_response = "Pedirle al usuario que reinicie chat y luego aporte sus generales."
                            
                        function_response = function_to_call(generales=generales, **function_args)
                        
                    except Exception as error:
                        print(error)
                        function_response = "Error al crear la solicitud."
                        
                elif function_name in ["redes_sociales", "info_contacto"]:
                    function_response = function_to_call()
                        
                else:
                    print("Herramienta desconocida.")
                    function_response = "Herramienta desconocida."
                    
                messages.append(
                    {
                        "tool_call_id": tool_call.id,
                        "role": "tool",
                        "name": function_name,
                        "content": function_response,
                    }
                )
                print("Respuesta de la herramienta enviada al modelo.")
                
            except Exception as error:
                ok = False
                print(f"Error al ejecutar la herramienta: {error}")
                messages.append(
                    {
                        "tool_call_id": tool_call.id,
                        "role": "tool",
                        "name": function_name,
                        "content": "Error al ejecutar la herramienta.",
                    }
                )
                
        try:
            second_response = client.chat.completions.create(
                model=model,
                messages=messages,
                tools=tools_,
            )
            print("Respuesta del modelo generada.")
            return second_response.choices[0].message.content, ok
        
        except Exception as error:
            print(error)
            return "Lo sentimos, ha ocurrido un error, realice la consulta más tarde.", False


if __name__ == "__main__":
    pass