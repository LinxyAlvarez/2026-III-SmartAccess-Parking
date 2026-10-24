from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.db.models import ProtectedError
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from .forms import EstacionamientoForm, SensorForm
from .models import Estacionamiento, Sensor


class ModelPermissionMixin(LoginRequiredMixin, PermissionRequiredMixin):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        app_label = self.model._meta.app_label
        model_name = self.model._meta.model_name
        context.update(
            permissions_enforced=True,
            can_create=self.request.user.has_perm(
                f"{app_label}.add_{model_name}"
            ),
            can_update=self.request.user.has_perm(
                f"{app_label}.change_{model_name}"
            ),
            can_delete=self.request.user.has_perm(
                f"{app_label}.delete_{model_name}"
            ),
        )
        return context


class EliminacionProtegidaView(DeleteView):
    def form_valid(self, form):
        try:
            self.object.delete()
        except ProtectedError:
            messages.error(
                self.request,
                "No se puede eliminar porque hay registros relacionados.",
            )
        else:
            messages.success(self.request, "Registro eliminado correctamente.")

        return HttpResponseRedirect(self.get_success_url())


class EstacionamientoListView(ModelPermissionMixin, ListView):
    model = Estacionamiento
    permission_required = "estacionamientos.view_estacionamiento"
    template_name = "crud/list.html"
    context_object_name = "objects"
    extra_context = {
        "title": "Estacionamientos",
        "create_url": "estacionamientos:estacionamiento_create",
        "update_url": "estacionamientos:estacionamiento_update",
        "delete_url": "estacionamientos:estacionamiento_delete",
    }


class EstacionamientoCreateView(ModelPermissionMixin, CreateView):
    model = Estacionamiento
    permission_required = "estacionamientos.add_estacionamiento"
    form_class = EstacionamientoForm
    template_name = "crud/form.html"
    success_url = reverse_lazy("estacionamientos:estacionamiento_list")
    extra_context = {"title": "Crear estacionamiento"}


class EstacionamientoUpdateView(ModelPermissionMixin, UpdateView):
    model = Estacionamiento
    permission_required = "estacionamientos.change_estacionamiento"
    form_class = EstacionamientoForm
    template_name = "crud/form.html"
    success_url = reverse_lazy("estacionamientos:estacionamiento_list")
    extra_context = {"title": "Editar estacionamiento"}


class EstacionamientoDeleteView(ModelPermissionMixin, EliminacionProtegidaView):
    model = Estacionamiento
    permission_required = "estacionamientos.delete_estacionamiento"
    template_name = "crud/confirm_delete.html"
    success_url = reverse_lazy("estacionamientos:estacionamiento_list")
    extra_context = {"title": "estacionamiento"}


class SensorListView(ModelPermissionMixin, ListView):
    model = Sensor
    permission_required = "estacionamientos.view_sensor"
    template_name = "crud/list.html"
    context_object_name = "objects"
    extra_context = {
        "title": "Sensores",
        "create_url": "estacionamientos:sensor_create",
        "update_url": "estacionamientos:sensor_update",
        "delete_url": "estacionamientos:sensor_delete",
    }


class SensorCreateView(ModelPermissionMixin, CreateView):
    model = Sensor
    permission_required = "estacionamientos.add_sensor"
    form_class = SensorForm
    template_name = "crud/form.html"
    success_url = reverse_lazy("estacionamientos:sensor_list")
    extra_context = {"title": "Crear sensor"}


class SensorUpdateView(ModelPermissionMixin, UpdateView):
    model = Sensor
    permission_required = "estacionamientos.change_sensor"
    form_class = SensorForm
    template_name = "crud/form.html"
    success_url = reverse_lazy("estacionamientos:sensor_list")
    extra_context = {"title": "Editar sensor"}


class SensorDeleteView(ModelPermissionMixin, EliminacionProtegidaView):
    model = Sensor
    permission_required = "estacionamientos.delete_sensor"
    template_name = "crud/confirm_delete.html"
    success_url = reverse_lazy("estacionamientos:sensor_list")
    extra_context = {"title": "sensor"}
