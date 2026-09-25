
from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('mostrar/',listar),
    path('saludar/',saludar),
    path('saludar/<str:nombre>',saludar_nombre),
    path('factorial/<int:numero>',factorial),
    path('ver/',inicio_render)
]
