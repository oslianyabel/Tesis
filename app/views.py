from colorama import Fore, init
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.urls import reverse
from django.contrib import messages
from django.http import Http404, JsonResponse
from datetime import datetime
from core.completions import Completions
from .forms import *
from .models import *
from core import tools, utils

init(autoreset = True)


def index(request):
    sn = SobreNosotros.objects.filter(activo=True)[0]
    pot = Potencialidad.objects.filter(activo=True)[:3]
    skills = Skill.objects.filter(activo=True)[:4]
    cat = Categoria.objects.filter(activo=True)
    all = Servicio.objects.all()
    ej = [servicio for servicio in all if servicio.imagen and servicio.imagen.url != 'imagenes/servicios/nombre.jpg'][:9]
    team = Equipo.objects.filter(activo=True)[:4]
    preguntas = PreguntaFrecuente.objects.filter(activo=True)[:9]
    contacto = Contacto.objects.filter(activo=True)[0]
    catalogo = Catalogo.objects.filter(activo=True)[0]
    
    context = {
        'sobre_nosotros': sn,
        'potencialidades': pot,
        'skills': skills,
        'categorias': cat,
        'ejemplos': ej,
        'team': team,
        'preguntas': preguntas,
        'contacto': contacto,
        'catalogo': catalogo
    }
    
    return render(request, 'index.html', context)


def servicios(request, category_id):
    try:
        categoria = Categoria.objects.get(id = category_id)
        serv = Servicio.objects.filter(categoria = categoria, activo=True).order_by('imagen')
    except Categoria.DoesNotExist:
        serv = Servicio.objects.filter(activo=True).order_by('imagen')
        
    catalogo = Catalogo.objects.filter(activo=True)[0]
    contacto = Contacto.objects.filter(activo=True)[0]
    context = {
        "servicios": serv,
        "contacto": contacto,
        "catalogo": catalogo
    }
    return render(request, "servicios.html", context)


def servicio_detail(request, service_id):
    try:
        serv = Servicio.objects.get(id = service_id)
        if not serv.activo:
            print(f"El servicio con id: {service_id} no está activo.")
            raise Http404(f"El servicio con id: {service_id} no está activo.")
    except Servicio.DoesNotExist:
        print(f"No hay ningún servicio con id: {service_id}")
        raise Http404(f"No hay ningún servicio con id: {service_id}")
        
    contacto = Contacto.objects.filter(activo=True)[0]
    comentarios = Comentario.objects.filter(servicio = serv, aprobado = True)[:10]
    context = {
        "servicio": serv,
        "comentarios": comentarios,
        "contacto": contacto
    }
    return render(request, "servicio-detail.html", context)


def login_opinion(request, service_id):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect(reverse('opinion', args=[service_id]))
        # credenciales incorrectas    
        messages.error(request, "Nombre de usuario o contraseña incorrectos.")
    else:
        form = AuthenticationForm()
    
    catalogo = Catalogo.objects.filter(activo=True)[0]
    context = {
        "form": form,
        "service_id": service_id,
        "catalogo": catalogo
    }
    return render(request, 'accounts/login_opinion.html', context)


def register_opinion(request, service_id):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('login_opinion', args=[service_id]))
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = UserCreationForm()

    catalogo = Catalogo.objects.filter(activo=True)[0]
    context = {
        "form": form,
        "service_id": service_id,
        "catalogo": catalogo
    }
    return render(request, 'accounts/register_opinion.html', context)


def login_chatbot(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect(reverse('chatbot'))
        # credenciales incorrectas    
        messages.error(request, "Nombre de usuario o contraseña incorrectos.")
    else:
        form = AuthenticationForm()
    
    catalogo = Catalogo.objects.filter(activo=True)[0]
    context = {
        "form": form,
        "catalogo": catalogo
    }
    return render(request, 'accounts/login_chatbot.html', context)


def register_chatbot(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('login_chatbot'))
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = UserCreationForm()

    catalogo = Catalogo.objects.filter(activo=True)[0]
    context = {
        "form": form,
        "catalogo": catalogo
    }
    return render(request, 'accounts/register_chatbot.html', context)


def opinion(request, service_id):
    if not request.user.is_authenticated:
        return redirect(reverse('login_opinion', args=[service_id]))
    
    contacto = Contacto.objects.filter(activo=True)[0]
    servicio = Servicio.objects.get(id = service_id)
    if not servicio.activo:
        print(f"El servicio con id: {service_id} no está activo.")
        raise Http404(f"El servicio con id: {service_id} no está activo.")
    
    if request.method == 'POST':
        form = OpinionForm(request.POST)
        if form.is_valid():
            comentario = form.cleaned_data['comentario']
            puntuacion = int(form.cleaned_data['puntuacion'])
            if Puntuacion.objects.filter(usuario=request.user, servicio=servicio).exists():
                opinion = Puntuacion.objects.get(usuario=request.user, servicio=servicio)
                total_puntos = servicio.puntos_promedio * servicio.votos
                total_puntos -= opinion.puntuacion
                total_puntos += puntuacion
                
                servicio.puntos_promedio = total_puntos / servicio.votos
                opinion.puntuacion = puntuacion
                
                opinion.save()
                servicio.save()
            else:
                Puntuacion.objects.create(
                    usuario=request.user,
                    servicio=servicio,
                    puntuacion=puntuacion,
                )
                total_votos = servicio.votos + 1
                total_puntos = (servicio.puntos_promedio * servicio.votos) + puntuacion
                
                servicio.puntos_promedio = total_puntos / total_votos
                servicio.votos = total_votos
                servicio.save()
                
            if comentario != "":
                Comentario.objects.create(
                    usuario=request.user,
                    texto=comentario,
                    servicio=servicio
                )

            return redirect(reverse('servicio-detail', args=[service_id]))
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
                    
    context = {
        "service_id": service_id,
        "servicio": servicio,
        "contacto": contacto,
        'range_1_5': range(1, 6),
        'range_5_1': range(5, 0, -1)
    }
    return render(request, 'opinion.html', context)


def chatbot(request):
    if request.method == 'POST':
        return generar_respuesta(request)
        
    catalogo = Catalogo.objects.filter(activo=True)[0]
    try:
        conv = Conversacion.objects.filter(usuario = request.user)[0]
        mensajes = Mensaje.objects.filter(conversacion = conv).order_by("fecha_envio")
    except Exception as exc:
        mensajes = None
        
    context = {
        "catalogo": catalogo,
        "mensajes": mensajes
    }

    return render(request, 'chatbot.html', context)


def chatbot_service(request, service_id):
    if request.method == 'POST':
        return generar_respuesta(request)
    
    try:
        servicio = Servicio.objects.get(id = service_id)
    except Exception as error:
        print(error)
        return redirect(reverse('chatbot'))
    
    catalogo = Catalogo.objects.filter(activo=True)[0]
    mensajes = None
    
    if request.user.is_authenticated:
        try:
            conv = Conversacion.objects.filter(usuario = request.user)[0]
            mensajes = Mensaje.objects.filter(conversacion = conv).order_by("fecha_envio")
        except Exception as error:
            mensajes = None
        
    context = {
        "catalogo": catalogo,
        "mensajes": mensajes,
        "servicio": servicio
    }
    return render(request, 'chatbot.html', context)


def generar_respuesta(request):
    user_msg = request.POST["Body"]
    print(f"- User: {user_msg}")
    
    if not request.user.is_authenticated:
        ans, tools_calls = generar_respuesta_usuario_no_autenticado(user_msg)
        date_time = datetime.now().strftime("%I:%M:%S %p")
        return JsonResponse({'text': ans, "status": "success", "time": date_time})
        
    conv = Conversacion.objects.filter(usuario = request.user)[0]
    if conv:
        msg_list_obj = Mensaje.objects.filter(conversacion = conv).order_by('fecha_envio')

        if msg_list_obj.exists():
            ans, tools_calls = generar_respuesta_con_historial(request.user, conv, user_msg, msg_list_obj)
            date_time = datetime.now().strftime("%I:%M:%S %p")
            return JsonResponse({'text': ans, "status": "success", "time": date_time})

    ans, tools_calls = generar_respuesta_sin_historial(request.user, user_msg)
    date_time = datetime.now().strftime("%I:%M:%S %p")
    return JsonResponse({'text': ans, "status": "success", "time": date_time})
            
    
def generar_respuesta_usuario_no_autenticado(user_msg):
    print(Fore.YELLOW + "Usuario no autenticado")
    chat = [{"role": "system", "content": utils.get_sys_prompt()}]

    bot = Completions (
        messages = chat, 
        tools = tools.get_tools(None), 
        functions = utils.get_functions()
    )
    ans, tools_calls = bot.submit_message(message = user_msg, user = None)

    print(Fore.BLUE + "- Bot:", ans)
    return ans, tools_calls


def generar_respuesta_sin_historial(user, user_msg):
    print("Generando respuesta sin historial")
    sys_prompt = utils.get_sys_prompt()
    chat = [{"role": "system", "content": sys_prompt}]
    bot = Completions(messages = chat, tools = tools.get_tools(user), functions = utils.get_functions())
    ans, tools_calls = bot.submit_message(message = user_msg, user = None)

    if ans != "Ha ocurrido un error, por favor realice la consulta más tarde":
        print("Guardando mensajes en la base de datos...")
        conv = Conversacion.objects.create(usuario = user)
        sys_prompt += f". El usuario se llama: {user}. Refiérete a él por ese nombre."

        Mensaje.objects.create (
            conversacion=conv,
            texto=sys_prompt,
            enviado_por="system"
        )
        Mensaje.objects.create (
            conversacion=conv,
            texto=user_msg,
            enviado_por="user"
        )
        Mensaje.objects.create (
            conversacion=conv,
            texto=ans,
            enviado_por="assistant"
        )
        
    return ans, tools_calls


def generar_respuesta_con_historial(user, conv, user_msg, msg_list_obj):
    print("Generando respuesta con historial")
    history = []

    for msg_obj in msg_list_obj:
        temp = {
            "role": str(msg_obj.enviado_por),
            "content": str(msg_obj.texto),
        }
        history.append(temp)
    
    bot = Completions(messages = history, tools = tools.get_tools(user), functions = utils.get_functions())
    ans, tools_calls = bot.submit_message(message = user_msg, user = user)
    print(f"- Bot: {ans}")
    
    if ans != "Ha ocurrido un error, por favor realice la consulta más tarde":
        print("Guardando mensajes en la base de datos")
        Mensaje.objects.create (
            conversacion=conv,
            texto=user_msg,
            enviado_por="user"
        )
        Mensaje.objects.create (
            conversacion=conv,
            texto=ans,
            enviado_por="assistant"
        )
        
    return ans, tools_calls
