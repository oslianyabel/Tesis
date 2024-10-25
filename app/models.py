from django.db import models
from django.contrib.auth.models import User

class SobreNosotros(models.Model):
    parrafo = models.TextField()
    parrafo2 = models.TextField(null=True, blank=True)
    check1 = models.CharField(max_length=255, null=True, blank=True)
    check2 = models.CharField(max_length=255, null=True, blank=True)
    check3 = models.CharField(max_length=255, null=True, blank=True)
    documento = models.FileField(upload_to='documentos')
    activo = models.BooleanField(default=True)

    def __str__(self):
        return self.parrafo[:50]


class Potencialidad(models.Model):
    nombre = models.CharField(max_length=255)
    descripcion = models.TextField()
    activo = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre


class Skill(models.Model):
    nombre = models.CharField(max_length=255)
    porcentaje = models.IntegerField()
    activo = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre
    

class Categoria(models.Model):
    nombre = models.CharField(max_length=255)
    abreviatura = models.CharField(max_length=255)
    descripcion = models.TextField()
    activo = models.BooleanField(default=True)
    clase = models.CharField(max_length=255, default='fas fa-cloud')
    
    def __str__(self):
        return self.nombre
    

class Servicio(models.Model):
    nombre = models.CharField(max_length=255)
    descripcion = models.TextField()
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    imagen = models.ImageField(upload_to='imagenes/servicios', null=True, blank=True)
    imagen2 = models.ImageField(upload_to='imagenes/servicios', null=True, blank=True)
    imagen3 = models.ImageField(upload_to='imagenes/servicios', null=True, blank=True)
    activo = models.BooleanField(default=True)
    votos = models.IntegerField(default=0)
    puntos_promedio = models.DecimalField(max_digits=3, decimal_places=2, default=0.00)

    def __str__(self):
        return self.nombre
    
    
class Comentario(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    texto = models.TextField()
    fecha = models.DateField(auto_now_add=True)
    aprobado = models.BooleanField(default=False)
    servicio = models.ForeignKey(Servicio, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.usuario} > {self.servicio}"


class Equipo(models.Model):
    imagen = models.ImageField(upload_to='imagenes/equipo')
    nombre = models.CharField(max_length=255)
    apellido = models.CharField(max_length=255, null=True, blank=True)
    cargo = models.CharField(max_length=255, null=True, blank=True)
    evento = models.CharField(max_length=255)
    fecha = models.DateField()
    link = models.URLField(max_length=200, null=True, blank=True)
    fuente = models.CharField(max_length=255, null=True, blank=True)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.nombre}"


class PreguntaFrecuente(models.Model):
    pregunta = models.CharField(max_length=255)
    respuesta = models.TextField()
    activo = models.BooleanField(default=True)

    def __str__(self):
        return self.pregunta
    

class Link(models.Model):
    nombre = models.CharField(max_length=255)
    link = models.URLField()
    clase = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.nombre
    

class Contacto(models.Model):
    direccion = models.CharField(max_length=255)
    correo = models.EmailField()
    telefono_fijo = models.CharField(max_length=20)
    telefono_movil = models.CharField(max_length=20)
    links_de_ayuda = models.ManyToManyField(Link, related_name='ayuda')
    redes_sociales = models.ManyToManyField(Link, related_name='redes')
    activo = models.BooleanField(default=True)

    def __str__(self):
        return self.correo


class Conversacion(models.Model):
    usuario = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    fecha_inicio = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.usuario.username
    
    @property
    def cantidad_mensajes(self):
        return self.mensaje_set.count()


class Mensaje(models.Model):
    ENVIADO_POR_CHOICES = [
        ('assistant', 'Asistente'),
        ('user', 'Usuario'),
        ('system', 'Sistema'),
    ]
    conversacion = models.ForeignKey(Conversacion, on_delete=models.CASCADE)
    texto = models.TextField()
    enviado_por = models.CharField(max_length=255, choices=ENVIADO_POR_CHOICES)
    fecha_envio = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.enviado_por} -> {self.conversacion}'


class Catalogo(models.Model):
    nombre = models.CharField(max_length=255)
    activo = models.BooleanField(default=True)
    hero = models.ImageField(upload_to='imagenes/index')
    why_us = models.ImageField(upload_to='imagenes/index')
    skills = models.ImageField(upload_to='imagenes/index')
    action = models.ImageField(upload_to='imagenes/index')
    logo = models.ImageField(upload_to='imagenes/index', null=True, blank=True)
    fondo_chatbot = models.ImageField(upload_to='imagenes', null=True, blank=True)
    
    def __str__(self):
        return self.nombre
    
    
class ChatBot(models.Model):
    nombre = models.CharField(max_length=255, default="ChatBot")
    facebook = models.CharField(max_length=255, default='<a href="https://www.facebook.com/SolucionesDTeam" class="facebook" target="_blank">Facebook <i class="bx bxl-facebook"></i></a>')
    instagram = models.CharField(max_length=255, default='<a href="https://www.instagram.com/solucionesdteam/" class="instagram" target="_blank">Instagram <i class="bx bxl-instagram"></i></a>')
    X = models.CharField(max_length=255, default='<a href="https://x.com/DesoftSsp" class="twitter">X <i class="bx bxl-twitter" target="_blank"></i></a>')
    telegram = models.CharField(max_length=255, default='<a href="https://t.me/clientesDesoftSSP" class="telegram" target="_blank">Telegram <i class="bx bxl-telegram"></i></a>')
    whatsapp = models.CharField(max_length=255, default='<a href="https://chat.whatsapp.com/GXwpDNRWs1F6NOM1Z2fzbc" target="_blank">Whatsapp <i class="bx bxl-whatsapp"></i></a></a>')
    sys_prompt = models.TextField()
    generales_prompt = models.TextField(default="Almacena las generales de una empresa y las asocia al usuario para poder crear solicitudes de contratos.")
    cuestionarios_prompt = models.TextField(default="Entrega al usuario un enlace de descarga de un modelo de cuestionario para solicitar un servicio dado.")
    energux_prompt = models.TextField()
    myros_prompt = models.TextField()
    servidores_prompt = models.TextField()
    fastos_pagus_prompt = models.TextField()
    activo = models.BooleanField(default=False)
    
    def __str__(self):
        return self.nombre
  
  
class Generales(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    nombre_empresa = models.CharField(max_length=255)
    dir = models.CharField(max_length=255)
    mun = models.CharField(max_length=255)
    prov = models.CharField(max_length=255)
    email = models.EmailField()
    tel = models.CharField(max_length=20)
    nombre = models.CharField(max_length=255)
    apellidos = models.CharField(max_length=255)
    cargo = models.CharField(max_length=255)
    
    def __str__(self):
        return f"{self.usuario.username} -> {self.nombre_empresa}"
    
    
class Solicitud(models.Model):
    ESTADO_CHOICES = [
        ('pending', 'Pendiente'),
        ('accepted', 'Aceptado'),
        ('declined', 'Rechazado'),
    ]
    generales = models.ForeignKey(Generales, on_delete=models.CASCADE)
    servicio = models.ForeignKey(Servicio, on_delete=models.CASCADE)
    cuestionario = models.TextField()
    fecha = models.DateField(auto_now_add=True)
    estado = models.CharField(max_length=255, default = "pending", choices=ESTADO_CHOICES)
    observaciones = models.TextField()
    
    def __str__(self):
        return f"{self.generales.usuario.username} -> {self.servicio.nombre} ({self.estado})"
    

class Cliente_Pot(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    servicio = models.ForeignKey(Servicio, on_delete=models.CASCADE)
    fecha = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.usuario.username} -> {self.servicio.nombre}"