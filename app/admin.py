from django.contrib import admin
from .models import *

admin.site.register(SobreNosotros)


class MensajeInline(admin.TabularInline):
    model = Mensaje
    extra = 1  # Número de formularios vacíos para agregar nuevos mensajes


@admin.register(Conversacion)
class ConversacionAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'fecha_inicio', 'cantidad_mensajes')
    inlines = [MensajeInline]
    

@admin.register(Cliente_Pot)
class Cliente_PotAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'servicio', 'fecha')
    
    
@admin.register(Potencialidad)
class PotencialidadAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'descripcion', 'activo')
    
    
@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'porcentaje', 'activo')
    
    
@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'abreviatura', 'activo')
    
    
@admin.register(Servicio)
class ServicioAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'categoria', 'activo')
    list_filter = ('activo', 'categoria')
    search_fields = ('nombre',)
    
    
@admin.register(Comentario)
class ComentarioAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'servicio', 'fecha', 'aprobado')
    list_filter = ('aprobado',)


@admin.register(Equipo)
class EquipoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'evento', 'fecha', 'activo')
    list_filter = ('activo',)
    search_fields = ('nombre',)
    
    
@admin.register(PreguntaFrecuente)
class PreguntaFrecuenteAdmin(admin.ModelAdmin):
    list_display = ('pregunta', 'activo')
    list_filter = ('activo',)
    search_fields = ('pregunta',)
    
    
@admin.register(Link)
class LinkAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'link')
    search_fields = ('nombre',)
    
    
@admin.register(Contacto)
class ContactoAdmin(admin.ModelAdmin):
    list_display = ('correo', 'direccion', 'telefono_movil', 'activo')
    list_filter = ('activo',)
    
    
@admin.register(Mensaje)
class MensajeAdmin(admin.ModelAdmin):
    list_display = ('conversacion', 'enviado_por', 'fecha_envio')
    
    
@admin.register(Catalogo)
class CatalogoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'activo')
    search_fields = ('nombre',)
    list_filter = ('activo',)
    
    
@admin.register(ChatBot)
class ChatBotAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'activo')
    search_fields = ('nombre',)
    list_filter = ('activo',)
    
    
@admin.register(Generales)
class GeneralesAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'cargo', 'nombre_empresa')
    search_fields = ('nombre_empresa',)
    
    
@admin.register(Solicitud)
class SolicitudAdmin(admin.ModelAdmin):
    list_display = ('generales', 'servicio', 'fecha', 'estado')
    list_filter = ('estado', 'fecha', 'servicio__nombre')
    