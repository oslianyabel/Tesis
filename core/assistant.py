from openai import OpenAI
from dotenv import load_dotenv
from colorama import Fore, init
import json, os
from app.models import *
from core import tools, utils

load_dotenv()

init(autoreset=True)

AVANGENIO_API_KEY = os.getenv('AVANGENIO_API_KEY')

client = OpenAI(
    base_url = "https://apigateway.avangenio.net",
    api_key = AVANGENIO_API_KEY,
)

model = "radiance"
    
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
        print("Generando respuesta del modelo")
        response = client.chat.completions.create(
            model=model,
            messages=messages,
        )
        response_message = response.choices[0].message

    except Exception as error:
        print(Fore.RED + error)
        return "Lo sentimos, ha ocurrido un error, realice la consulta más tarde.", False
    
    tool_calls = response_message.tool_calls

    if not tool_calls:
        return response_message.content, True
    
    else:
        return "El usuario debe autenticarse para realizar esta acción.", False
    

def run_conversation(usuario, new_msg, messages=None):
    """ 
    Genera la próxima respuesta del chatbot en una conversación
    @param {django.contrib.auth.models.User} usuario - Usuario que está realizando la consulta
    @param {str} new_msg - Nuevo mensaje del usuario
    @param {List<dict>} messages - Lista de mensajes de la conversación actual
    @returns {(str, bool)} - Tupla con la respuesta del chatbot y una bandera indicando si la operación fue exitosa
    """
    
    if not messages:
        print("Conversación sin mensajes")
        sys_prompt = get_sys_prompt()
        sys_prompt += f". El usuario se llama: {usuario}. Refiérete a él por ese nombre."
        messages = [
            {"role": "system", "content": sys_prompt},
            {"role": "user", "content": new_msg}
        ]

    else:
        messages.append({"role": "user", "content": new_msg})
        
    generales = utils.get_generales(usuario)
    tools_ = utils.get_tools(generales)
        
    try:
        print("Generando respuesta del modelo...")
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            tools=tools_,
            tool_choice="auto",
        )
        response_message = response.choices[0].message

    except Exception as error:
        print(Fore.RED + f"{error}")
        return "Lo sentimos, ha ocurrido un error, realice la consulta más tarde.", False
    
    tool_calls = response_message.tool_calls

    if not tool_calls:
        return response_message.content, True
    
    else:
        ok = True
        print(Fore.BLUE + "Herramenta solicitada!")
        messages.append(response_message)
        
        for tool_call in tool_calls:
            try:
                function_name = tool_call.function.name
                print(Fore.BLUE + function_name)
                function_to_call = available_functions[function_name]
                function_args = json.loads(tool_call.function.arguments)
                print(Fore.BLUE + function_args)
                
                if function_name == 'cuestionario':
                    nombre_serv = function_args["servicio"]
                    try:
                        servicio = Servicio.objects.filter(nombre__iexact = nombre_serv)[0]
                        function_response = function_to_call(servicio=servicio, usuario=usuario)
                        
                    except Exception as error:
                        print(Fore.RED + f"El servicio no existe: {error}")
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
                            print(Fore.YELLOW + "Usuario sin generales")
                            function_response = "Pedirle al usuario que reinicie chat y luego aporte sus generales."
                            
                        function_response = function_to_call(generales=generales, **function_args)
                        
                    except Exception as error:
                        print(Fore.RED + error)
                        function_response = "Error al crear la solicitud."
                        
                elif function_name in ["redes_sociales", "info_contacto"]:
                    function_response = function_to_call()
                        
                else:
                    print(Fore.RED + "Herramienta desconocida")
                    function_response = "Herramienta desconocida."
                    
                messages.append(
                    {
                        "tool_call_id": tool_call.id,
                        "role": "tool",
                        "name": function_name,
                        "content": function_response,
                    }
                )
                print("Respuesta de la herramienta enviada al modelo")
                
            except Exception as error:
                ok = False
                print(Fore.RED + f"Error al ejecutar la herramienta: {error}")
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

            print("Respuesta del modelo generada")
            return second_response.choices[0].message.content, ok
        
        except Exception as error:
            print(Fore.RED + error)
            return "Lo sentimos, ha ocurrido un error, realice la consulta más tarde.", False


if __name__ == "__main__":
    pass