from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from parking.models import Acreditacion
from parking.usuarios.forms import UsuarioForm, AcreditacionForm


def lista_usuarios(request):
    usuarios = User.objects.all()
    return render(request, "usuarios/lista.html", {
        "usuarios": usuarios
    })


def nuevo_usuario(request):
    if request.method == "POST":
        formulario = UsuarioForm(request.POST)
        if formulario.is_valid():
            formulario.save()
            return redirect("lista_usuarios")
    else:
        formulario = UsuarioForm()

    return render(request, "usuarios/formulario.html", {
        "formulario": formulario
    })


def editar_usuario(request, id):
    usuario = get_object_or_404(User, id=id)

    if request.method == "POST":
        formulario = UsuarioForm(request.POST, instance=usuario)
        if formulario.is_valid():
            formulario.save()
            return redirect("lista_usuarios")
    else:
        formulario = UsuarioForm(instance=usuario)

    return render(request, "usuarios/formulario.html", {
        "formulario": formulario
    })


def eliminar_usuario(request, id):
    usuario = get_object_or_404(User, id=id)

    if request.method == "POST":
        usuario.delete()
        return redirect("lista_usuarios")

    return render(request, "usuarios/confirmar_eliminacion.html", {
        "usuario": usuario
    })


def lista_acreditaciones(request):
    acreditaciones = Acreditacion.objects.select_related("usuario").all()
    return render(request, "acreditaciones/lista.html", {
        "acreditaciones": acreditaciones
    })


def nueva_acreditacion(request):
    if request.method == "POST":
        formulario = AcreditacionForm(request.POST)
        if formulario.is_valid():
            formulario.save()
            return redirect("lista_acreditaciones")
    else:
        formulario = AcreditacionForm()

    return render(request, "acreditaciones/formulario.html", {
        "formulario": formulario
    })


def editar_acreditacion(request, id):
    acreditacion = get_object_or_404(Acreditacion, id=id)

    if request.method == "POST":
        formulario = AcreditacionForm(
            request.POST,
            instance=acreditacion
        )
        if formulario.is_valid():
            formulario.save()
            return redirect("lista_acreditaciones")
    else:
        formulario = AcreditacionForm(instance=acreditacion)

    return render(request, "acreditaciones/formulario.html", {
        "formulario": formulario
    })


def eliminar_acreditacion(request, id):
    acreditacion = get_object_or_404(Acreditacion, id=id)

    if request.method == "POST":
        acreditacion.delete()
        return redirect("lista_acreditaciones")

    return render(
        request,
        "acreditaciones/confirmar_eliminacion.html",
        {"acreditacion": acreditacion}
    )