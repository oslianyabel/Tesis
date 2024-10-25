from django.http import JsonResponse
from datetime import datetime
from app.forms import *
from app.models import *
from core import assistant


def get_generales(usuario):
    try:
        generales = Generales.objects.get(usuario = usuario)
        print("Usuario con generales.")
        
        return generales
    
    except Exception as error:
        print(f"Usuario sin generales. {error}")
        
        return None
    

def generar_respuesta_usuario_no_autenticado(user_msg):
    print("Usuario no autenticado.")
    ans, ok = assistant.run_conversation2(user_msg)
    print(f"- Bot: {ans}")
    hora_actual = datetime.now().strftime("%I:%M:%S %p")
    
    return JsonResponse({'text': ans, "status": "success", "time": hora_actual})
        

def buscar_conversacion(usuario):
    try:
        conv = Conversacion.objects.get(usuario = usuario)
        print("Conversacion encontrada.")
        
        return conv
    
    except Conversacion.DoesNotExist:
        conv = Conversacion.objects.create(usuario = usuario)
        print("Conversacion creada.")
        
        return conv
            

def generar_respuesta_sin_historial(usuario, conv, user_msg):
    ans, ok = assistant.run_conversation(usuario, user_msg)
    print(f"- Bot: {ans}")
    if ok:
        print("Guardando mensajes en la base de datos.")
        sys_prompt = assistant.get_sys_prompt()
        sys_prompt += f". El usuario se llama: {usuario}. Refiérete a él por ese nombre."
        Mensaje.objects.create(
            conversacion=conv,
            texto=sys_prompt,
            enviado_por="system"
        )
        Mensaje.objects.create(
            conversacion=conv,
            texto=user_msg,
            enviado_por="user"
        )
        Mensaje.objects.create(
            conversacion=conv,
            texto=ans,
            enviado_por="assistant"
        )
        
    hora_actual = datetime.now().strftime("%I:%M:%S %p")
    
    return JsonResponse({'text': ans, "status": "success", "time": hora_actual})
        
                
def generar_respuesta_con_historial(usuario, conv, user_msg, msg_list_obj):
    print("Cargando historial.")
    history = []
    for msg_obj in msg_list_obj:
        temp = {
            "role": str(msg_obj.enviado_por),
            "content": str(msg_obj.texto),
        }
        history.append(temp)
    
    ans, ok = assistant.run_conversation(usuario, user_msg, history)
    print(f"- Bot: {ans}")
    
    if ok:
        print("Guardando mensajes en la base de datos.")
        Mensaje.objects.create(
            conversacion=conv,
            texto=user_msg,
            enviado_por="user"
        )
        Mensaje.objects.create(
            conversacion=conv,
            texto=ans,
            enviado_por="assistant"
        )
        
    hora_actual = datetime.now().strftime("%I:%M:%S %p")
    
    return JsonResponse({'text': ans, "status": "success", "time": hora_actual})
    
              
def generar_respuesta(request):
    user_msg = request.POST["Body"]
    print(f"- User: {user_msg}")
    
    if not request.user.is_authenticated:
        return generar_respuesta_usuario_no_autenticado(user_msg)            
    
    conv = buscar_conversacion(request.user)
    
    msg_list_obj = Mensaje.objects.filter(conversacion = conv).order_by('fecha_envio')
    if not msg_list_obj.exists():
        return generar_respuesta_sin_historial(request.user, conv, user_msg)
    else:
        return generar_respuesta_con_historial(request.user, conv, user_msg, msg_list_obj)