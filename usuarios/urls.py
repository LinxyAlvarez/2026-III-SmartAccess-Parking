from django.contrib.auth import views as auth_views
from django.urls import path

from . import views


app_name = "usuarios"

urlpatterns = [
    path(
        "login/",
        auth_views.LoginView.as_view(template_name="registration/login.html"),
        name="login",
    ),
    path(
        "logout/",
        auth_views.LogoutView.as_view(next_page="usuarios:login"),
        name="logout",
    ),
    path("", views.UsuarioListView.as_view(), name="usuario_list"),
    path("nuevo/", views.UsuarioCreateView.as_view(), name="usuario_create"),
    path("<int:pk>/editar/", views.UsuarioUpdateView.as_view(), name="usuario_update"),
    path("<int:pk>/eliminar/", views.UsuarioDeleteView.as_view(), name="usuario_delete"),

    path("vehiculos/", views.VehiculoListView.as_view(), name="vehiculo_list"),
    path("vehiculos/nuevo/", views.VehiculoCreateView.as_view(), name="vehiculo_create"),
    path("vehiculos/<str:pk>/editar/", views.VehiculoUpdateView.as_view(), name="vehiculo_update"),
    path("vehiculos/<str:pk>/eliminar/", views.VehiculoDeleteView.as_view(), name="vehiculo_delete"),
]
