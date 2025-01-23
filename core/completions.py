from openai import OpenAI
from dotenv import load_dotenv
from colorama import Fore, init
from datetime import datetime
from pydantic import BaseModel
import json, os
from core import functions, utils

load_dotenv()

init(autoreset=True)


class Completions:
    def __init__(self, messages, model = "radiance", base_url = "https://apigateway.avangenio.net", tools = [], functions = {}, tool_choice = "auto", response_format = False):
        self.client = OpenAI(
            api_key = os.getenv('AVANGENIO_API_KEY'),
            base_url = base_url,
        )
        self.model = model
        self.base_url = base_url
        self.messages = messages
        self.tools = tools
        self.tool_choice = tool_choice
        self.functions = functions
        self.response_format = response_format
        self.error_msg = "Ha ocurrido un error, por favor realice la consulta más tarde"
        
        
    def submit_message(self, message, user, tools_called = []):
        print(Fore.BLUE + "- User:", message)

        self.messages.append({
            'role': 'user',
            "content": message, 
            "date": datetime.now().strftime('%Y-%m-%d'),
        })

        while True:
            try:
                # Processing model response
                if self.tools and self.response_format:
                    print(Fore.BLUE + f"Procesando respuesta con el modelo {self.model}, {len(self.tools)} herramientas y la estructura {self.response_format}")
                    response = self.client.beta.chat.completions.parse (
                        model = self.model,
                        messages = self.messages,
                        tools = self.tools,
                        tool_choice = self.tool_choice,
                        response_format = self.response_format,
                    ) 
                elif self.tools and not self.response_format:
                    print(Fore.BLUE + f"Procesando respuesta con el modelo {self.model} y {len(self.tools)} herramientas en texto plano")
                    response = self.client.chat.completions.create (
                        model = self.model,
                        messages = self.messages,
                        tools = self.tools,
                        tool_choice = self.tool_choice,
                    )
                elif not self.tools and self.response_format:
                    print(Fore.BLUE + f"Procesando respuesta con el modelo {self.model} sin herramientas y la estructura {self.response_format}")
                    response = self.client.beta.chat.completions.parse (
                        model = self.model,
                        messages = self.messages,
                        response_format = self.response_format,
                    )
                else:
                    print(Fore.BLUE + f"Procesando respuesta con el modelo {self.model} sin herramientas en texto plano")
                    response = self.client.chat.completions.create (
                        model = self.model,
                        messages = self.messages,
                    )
                
            except Exception as exc:
                msg = f"Falló la respuesta del modelo: {exc}"
                print(Fore.RED + msg)
                #utils2.send_email("oslianyabel@gmail.com", "Completions error in Soluciones DTeam", msg)
                return self.error_msg, ["ERROR"]
                
            if not response.choices[0].message.tool_calls:
                # No tools calls, break while loop
                if self.response_format:
                    ans = response.choices[0].message.parsed
                else:
                    ans = response.choices[0].message.content
                    
                self.messages.append({
                    'role': 'assistant',
                    "content": ans, 
                    "date": datetime.now().strftime('%Y-%m-%d'),
                })    

                print(Fore.BLUE + "- Bot:", ans)
                return ans, tools_called
            
            else:
                # Tools calls, continue while loop
                print((Fore.BLUE + "=")*25 + " Tool calls! " + (Fore.BLUE + "=")*25)
                self.messages.append(response.choices[0].message)
                
                for tool_call in response.choices[0].message.tool_calls:
                    function_name = tool_call.function.name
                    function_args = json.loads(tool_call.function.arguments)
                    function_args["user"] = user
                    function_response = False
                    print(function_name)
                    print(function_args)
                    
                    if function_name in ["Energux", "Myros", "Servidores"]:
                        generales = utils.get_generales(user)

                        if generales:
                            function_args['generales'] = generales
                        else:
                            print(Fore.YELLOW + "Usuario sin generales")
                            function_response = "Pedirle al usuario que reinicie chat y luego aporte sus generales"

                    if not function_response:
                        try:
                            function_to_call = self.functions[function_name]
                            function_response = function_to_call(**function_args)
                            tools_called.append(function_name)
                        
                        except Exception as exc:
                            print(Fore.RED + f"Error ejecutando la herramienta {function_name}: {exc}")
                            function_response = self.error_msg
                            tools_called.append(f"{function_name}_ERROR")
                    
                    self.messages.append ({
                        "tool_call_id": tool_call.id,
                        "role": "tool",
                        "name": function_name,
                        "content": function_response,
                    })
                    print(f"Respuesta de la herramienta:{self.messages}")
                    # End of for loop

                # End of while loop

    
if __name__ == "__main__":
    messages = [
        {
            'role': 'system',
            "content": "Eres un asistente útil", 
            "date": datetime.now().strftime('%Y-%m-%d'),
        },
    ]

    available_functions = {
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

    tools = utils.get_tools(True)

    bot = Completions(messages = messages, tools = tools, functions = available_functions)
    ans, tools_called = bot.submit_message("Hola", None)
    print(ans)
    print(tools_called)
