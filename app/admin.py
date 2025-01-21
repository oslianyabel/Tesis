from django.contrib import admin
from .models import *
from import_export import resources # type: ignore
from import_export.admin import ImportExportModelAdmin # type: ignore


class CategoriaResource(resources.ModelResource):
    class Meta:
        model = Categoria
        
        
class CorreosResource(resources.ModelResource):
    class Meta:
        model = Correos
        
        
class ConversacionResource(resources.ModelResource):
    class Meta:
        model = Conversacion
        
        
class SolicitudResource(resources.ModelResource):
    class Meta:
        model = Solicitud
        
        
class GeneralesResource(resources.ModelResource):
    class Meta:
        model = Conversacion
        
        
class ChatBotResource(resources.ModelResource):
    class Meta:
        model = ChatBot
        
        
class CatalogoResource(resources.ModelResource):
    class Meta:
        model = Catalogo
        
        
class MensajeResource(resources.ModelResource):
    class Meta:
        model = Mensaje
        
        
class ContactoResource(resources.ModelResource):
    class Meta:
        model = Contacto
        
        
class LinkResource(resources.ModelResource):
    class Meta:
        model = Link
        
        
class PreguntaFrecuenteResource(resources.ModelResource):
    class Meta:
        model = PreguntaFrecuente
        
        
class EquipoResource(resources.ModelResource):
    class Meta:
        model = Equipo
        
        
class ComentarioResource(resources.ModelResource):
    class Meta:
        model = Comentario
        
        
class ContactoResource(resources.ModelResource):
    class Meta:
        model = Contacto
        
        
class ServicioResource(resources.ModelResource):
    class Meta:
        model = Servicio
        
        
class SkillResource(resources.ModelResource):
    class Meta:
        model = Skill
        
        
class PuntuacionResource(resources.ModelResource):
    class Meta:
        model = Puntuacion
        
        
class PotencialidadResource(resources.ModelResource):
    class Meta:
        model = Potencialidad
        
        
class ServicioResource(resources.ModelResource):
    class Meta:
        model = Servicio
        
        
class Cliente_PotResource(resources.ModelResource):
    class Meta:
        model = Cliente_Pot
                

admin.site.register(SobreNosotros)


class MensajeInline(admin.TabularInline):
    model = Mensaje
    extra = 1  # Número de formularios vacíos para agregar nuevos mensajes


@admin.register(Conversacion)
class ConversacionAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('usuario', 'fecha_inicio', 'cantidad_mensajes')
    inlines = [MensajeInline]
    resource_class = ConversacionResource
    

@admin.register(Cliente_Pot)
class Cliente_PotAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('usuario', 'servicio', 'fecha')
    resource_class = Cliente_PotResource
    
    
@admin.register(Potencialidad)
class PotencialidadAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('nombre', 'descripcion', 'activo')
    resource_class = PotencialidadResource
    
    
@admin.register(Puntuacion)
class PuntuacionAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('puntuacion', 'fecha')
    resource_class = PuntuacionResource
    
    
@admin.register(Skill)
class SkillAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('nombre', 'porcentaje', 'activo')
    resource_class = SkillResource
    
    
@admin.register(Categoria)
class CategoriaAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('nombre', 'abreviatura', 'activo')
    resource_class = CategoriaResource
    
    
@admin.register(Correos)
class CorreosAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('correo1', 'correo2', 'correo3')
    resource_class = CorreosResource
    
    
@admin.register(Servicio)
class ServicioAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('nombre', 'categoria', 'activo')
    list_filter = ('activo', 'categoria')
    search_fields = ('nombre',)
    resource_class = ServicioResource
    
    
@admin.register(Comentario)
class ComentarioAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('usuario', 'servicio', 'fecha', 'aprobado')
    list_filter = ('aprobado',)
    resource_class = ComentarioResource


@admin.register(Equipo)
class EquipoAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('nombre', 'evento', 'fecha', 'activo')
    list_filter = ('activo',)
    search_fields = ('nombre',)
    resource_class = EquipoResource
    
    
@admin.register(PreguntaFrecuente)
class PreguntaFrecuenteAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('pregunta', 'activo')
    list_filter = ('activo',)
    search_fields = ('pregunta',)
    resource_class = PreguntaFrecuenteResource
    
    
@admin.register(Link)
class LinkAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('nombre', 'link')
    search_fields = ('nombre',)
    resource_class = LinkResource
    
    
@admin.register(Contacto)
class ContactoAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('correo', 'direccion', 'telefono_movil', 'activo')
    list_filter = ('activo',)
    resource_class = ContactoResource
    
    
@admin.register(Mensaje)
class MensajeAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('conversacion', 'enviado_por', 'fecha_envio')
    resource_class = MensajeResource
    
    
@admin.register(Catalogo)
class CatalogoAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('nombre', 'activo')
    search_fields = ('nombre',)
    list_filter = ('activo',)
    resource_class = CatalogoResource
    
    
@admin.register(ChatBot)
class ChatBotAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('nombre', 'activo')
    search_fields = ('nombre',)
    list_filter = ('activo',)
    resource_class = ChatBotResource
    
    
@admin.register(Generales)
class GeneralesAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('nombre', 'cargo', 'nombre_empresa')
    search_fields = ('nombre_empresa',)
    resource_class = GeneralesResource
    
    
@admin.register(Solicitud)
class SolicitudAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('generales', 'servicio', 'fecha', 'estado')
    list_filter = ('estado', 'fecha', 'servicio__nombre')
    resource_class = SolicitudResource
    