from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.test import TestCase
from django.urls import reverse

from .models import Estacionamiento, Sensor


class EstacionamientosAccessTests(TestCase):
    def setUp(self):
        self.estacionamiento = Estacionamiento.objects.create(numero_cajon="A-01")
        self.sensor = Sensor.objects.create(
            estacionamiento=self.estacionamiento,
            tipo_sensor="Ultrasonico",
        )

    def permission(self, codename):
        return Permission.objects.get(
            content_type__app_label="estacionamientos",
            codename=codename,
        )

    def make_user(self, *permissions):
        user_model = get_user_model()
        user = user_model.objects.create_user(
            username=f"testuser{user_model.objects.count()}",
            password="Parking-test-123",
        )
        if permissions:
            user.user_permissions.add(
                *(self.permission(codename) for codename in permissions)
            )
        return user

    def protected_urls(self):
        return [
            reverse("estacionamientos:estacionamiento_list"),
            reverse("estacionamientos:estacionamiento_create"),
            reverse(
                "estacionamientos:estacionamiento_update",
                args=[self.estacionamiento.pk],
            ),
            reverse(
                "estacionamientos:estacionamiento_delete",
                args=[self.estacionamiento.pk],
            ),
            reverse("estacionamientos:sensor_list"),
            reverse("estacionamientos:sensor_create"),
            reverse("estacionamientos:sensor_update", args=[self.sensor.pk]),
            reverse("estacionamientos:sensor_delete", args=[self.sensor.pk]),
        ]

    def test_anonymous_users_are_redirected_to_login_for_all_crud_views(self):
        for url in self.protected_urls():
            with self.subTest(url=url):
                response = self.client.get(url)
                self.assertEqual(response.status_code, 302)
                login_url = reverse("usuarios:login")
                self.assertTrue(response.url.startswith(f"{login_url}?next="))

    def test_authenticated_users_without_permission_receive_forbidden(self):
        self.client.force_login(self.make_user())

        for url in self.protected_urls():
            with self.subTest(url=url):
                self.assertEqual(self.client.get(url).status_code, 403)

    def test_view_permission_shows_lists_but_hides_ungranted_actions(self):
        user = self.make_user("view_estacionamiento", "view_sensor")
        self.client.force_login(user)

        for name in (
            "estacionamientos:estacionamiento_list",
            "estacionamientos:sensor_list",
        ):
            with self.subTest(name=name):
                response = self.client.get(reverse(name))
                self.assertEqual(response.status_code, 200)
                self.assertNotContains(response, "Crear registro")
                self.assertNotContains(response, "Editar")
                self.assertNotContains(response, "Eliminar")

    def test_add_change_and_delete_permissions_are_checked_independently(self):
        user = self.make_user()
        self.client.force_login(user)

        operations = [
            (
                "estacionamientos:estacionamiento_create",
                "add_estacionamiento",
                {},
            ),
            (
                "estacionamientos:estacionamiento_update",
                "change_estacionamiento",
                {"args": [self.estacionamiento.pk]},
            ),
            (
                "estacionamientos:estacionamiento_delete",
                "delete_estacionamiento",
                {"args": [self.estacionamiento.pk]},
            ),
            (
                "estacionamientos:sensor_create",
                "add_sensor",
                {},
            ),
            (
                "estacionamientos:sensor_update",
                "change_sensor",
                {"args": [self.sensor.pk]},
            ),
            (
                "estacionamientos:sensor_delete",
                "delete_sensor",
                {"args": [self.sensor.pk]},
            ),
        ]
        for route_name, codename, route_kwargs in operations:
            with self.subTest(route=route_name, permission=codename):
                url = reverse(route_name, **route_kwargs)
                denied_response = self.client.get(url)
                self.assertEqual(denied_response.status_code, 403)

                if codename.startswith("delete_"):
                    form_data = {}
                elif "_estacionamiento" in codename:
                    form_data = {"numero_cajon": "FORBIDDEN", "estado": "on"}
                else:
                    form_data = {
                        "estacionamiento": self.estacionamiento.pk,
                        "tipo_sensor": "Infrarrojo",
                        "estado": "on",
                    }
                denied_post = self.client.post(url, form_data)
                self.assertEqual(denied_post.status_code, 403)

                user.user_permissions.add(self.permission(codename))
                allowed_response = self.client.get(url)
                self.assertEqual(allowed_response.status_code, 200)

    def test_login_and_logout_use_django_authentication(self):
        user = self.make_user("view_estacionamiento")
        login_page = self.client.get(reverse("usuarios:login"))
        self.assertEqual(login_page.status_code, 200)
        self.assertContains(login_page, 'name="username"')

        response = self.client.post(
            reverse("usuarios:login"),
            {"username": user.username, "password": "Parking-test-123"},
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            response.url,
            reverse("estacionamientos:estacionamiento_list"),
        )

        response = self.client.post(reverse("usuarios:logout"))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse("usuarios:login"))

    def test_users_with_crud_permissions_can_create_update_and_delete(self):
        user = self.make_user(
            "add_estacionamiento",
            "change_estacionamiento",
            "delete_estacionamiento",
            "add_sensor",
            "change_sensor",
            "delete_sensor",
        )
        self.client.force_login(user)

        response = self.client.post(
            reverse("estacionamientos:estacionamiento_create"),
            {"numero_cajon": "B-02", "estado": "on"},
        )
        self.assertEqual(response.status_code, 302)
        estacionamiento = Estacionamiento.objects.get(numero_cajon="B-02")

        response = self.client.post(
            reverse(
                "estacionamientos:estacionamiento_update",
                args=[estacionamiento.pk],
            ),
            {"numero_cajon": "B-03", "estado": "on"},
        )
        self.assertEqual(response.status_code, 302)
        estacionamiento.refresh_from_db()
        self.assertEqual(estacionamiento.numero_cajon, "B-03")

        response = self.client.post(
            reverse("estacionamientos:sensor_create"),
            {
                "estacionamiento": estacionamiento.pk,
                "tipo_sensor": "Infrarrojo",
                "estado": "on",
                "estado_ocupacion": "on",
            },
        )
        self.assertEqual(response.status_code, 302)
        sensor = Sensor.objects.get(estacionamiento=estacionamiento)

        response = self.client.post(
            reverse("estacionamientos:sensor_update", args=[sensor.pk]),
            {
                "estacionamiento": estacionamiento.pk,
                "tipo_sensor": "Ultrasonico",
                "estado": "on",
                "estado_ocupacion": "",
            },
        )
        self.assertEqual(response.status_code, 302)
        sensor.refresh_from_db()
        self.assertEqual(sensor.tipo_sensor, "Ultrasonico")
        self.assertFalse(sensor.estado_ocupacion)

        response = self.client.post(
            reverse("estacionamientos:sensor_delete", args=[sensor.pk]),
        )
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Sensor.objects.filter(pk=sensor.pk).exists())

        response = self.client.post(
            reverse(
                "estacionamientos:estacionamiento_delete",
                args=[estacionamiento.pk],
            ),
        )
        self.assertEqual(response.status_code, 302)
        self.assertFalse(
            Estacionamiento.objects.filter(pk=estacionamiento.pk).exists()
        )
