from django.contrib import admin
from django.urls import path, re_path
from app import views
from django.conf import settings
from django.views.static import serve
from django.conf.urls import handler404
from django.shortcuts import render

def custom_page_not_found_view(request, exception):
    return render(request, '404.html', status=404)

handler404 = custom_page_not_found_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('services/<int:category_id>', views.servicios, name='servicios'),
    path('service/<int:service_id>', views.servicio_detail, name='servicio-detail'),
    path('login/<int:service_id>', views.login_opinion, name='login_opinion'),
    path('login/', views.login_chatbot, name='login_chatbot'),
    path('register/<int:service_id>', views.register_opinion, name='register_opinion'),
    path('register/', views.register_chatbot, name='register_chatbot'),
    path('opinion/<int:service_id>', views.opinion, name='opinion'),
    path('chatbot/', views.chatbot, name='chatbot'),
    path('chatbot/<int:service_id>', views.chatbot_service, name='chatbot_service'),
    path('', views.index, name='index'),
]

urlpatterns += [
    re_path(r'^media/(?P<path>.*)$', serve, {
        'document_root': settings.MEDIA_ROOT,
    })
]