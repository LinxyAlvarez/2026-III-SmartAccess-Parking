from django.urls import path
from parking.usuarios import views


urlpatterns = [
    path("", views.lista_usuarios, name="lista_usuarios"),
    path("nuevo/", views.nuevo_usuario, name="nuevo_usuario"),
    path("editar/<int:id>/", views.editar_usuario, name="editar_usuario"),
    path("eliminar/<int:id>/", views.eliminar_usuario, name="eliminar_usuario"),

    path("acreditaciones/", views.lista_acreditaciones, name="lista_acreditaciones"),
    path("acreditaciones/nueva/", views.nueva_acreditacion, name="nueva_acreditacion"),
    path("acreditaciones/editar/<int:id>/", views.editar_acreditacion, name="editar_acreditacion"),
    path("acreditaciones/eliminar/<int:id>/", views.eliminar_acreditacion, name="eliminar_acreditacion"),
]
