from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='productos_index'),
    path('crear/', views.crear, name='productos_crear'),
    path('editar/<int:id>/', views.editar, name='productos_editar'),
    path('eliminar/<int:id>/', views.eliminar, name='productos_eliminar'),
]