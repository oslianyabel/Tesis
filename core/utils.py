from django.http import JsonResponse
from datetime import datetime
import smtplib, os
from email.message import EmailMessage
from dotenv import load_dotenv
from app.forms import *
from app.models import *
from core import assistant


load_dotenv()

EMAIL = os.getenv('EMAIL')
PASSWORD = os.getenv('PASSWORD')
HOST = os.getenv('HOST')


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
    

def send_mail(to, subject, message):
    email = EmailMessage()
    email["from"] = EMAIL
    email["to"] = to
    email["subject"] = subject
    email.set_content(message)

    try:
        print(f"Enviando notificación a {to}")
        with smtplib.SMTP(HOST, port = 587) as smtp:
            smtp.starttls()
            smtp.login(EMAIL, PASSWORD)
            smtp.sendmail(EMAIL, to, email.as_string())
            print("Correo enviado!")
            
    except Exception as e:
        print('Error al enviar correo:', e)


def preparar_email(cuestionario, generales, servicio):
    ans = "Generales:\n"
    ans += f"Usuario: {generales.usuario.username}\n"
    ans += f"Empresa: {generales.nombre_empresa}\n"
    ans += f"Dirección: {generales.dir}\n"
    ans += f"Municipio: {generales.mun}\n"
    ans += f"Provincia: {generales.prov}\n"
    ans += f"Email: {generales.email}\n"
    ans += f"Teléfono: {generales.tel}\n"
    ans += f"Nombre del representante: {generales.nombre}\n"
    ans += f"Apellidos del representante: {generales.apellidos}\n"
    ans += f"Cargo del representante: {generales.cargo}\n"
    
    ans += "="*50
    ans += f"\nCuestionario de {servicio}:\n"
    for key, value in cuestionario.items():
        ans += f"{key}: {value}\n"
        
    return ans


def send_mail_list(subject, message):
    correos = Correos.objects.filter(activo=True).first()
    
    if correos:
        for i in range(1, 11):
            correo = getattr(correos, f'correo{i}')
            if correo:
                send_mail(correo, subject, message)
        