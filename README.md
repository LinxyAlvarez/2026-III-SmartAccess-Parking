# 2026-III-SmartAccess-Parking

## Entregable 3: estacionamientos y sensores

El acceso a las pantallas de estacionamientos y sensores requiere una cuenta autenticada. Inicia sesión en `/usuarios/login/`; la opción para cerrar sesión envía una solicitud POST protegida con CSRF.

Las vistas aplican los permisos estándar de Django por operación:

| Módulo | Consultar | Crear | Editar | Eliminar |
| --- | --- | --- | --- | --- |
| Estacionamientos | `estacionamientos.view_estacionamiento` | `estacionamientos.add_estacionamiento` | `estacionamientos.change_estacionamiento` | `estacionamientos.delete_estacionamiento` |
| Sensores | `estacionamientos.view_sensor` | `estacionamientos.add_sensor` | `estacionamientos.change_sensor` | `estacionamientos.delete_sensor` |

Asigna estos permisos a usuarios o grupos desde `/admin/` (sección **Autenticación y autorización**). Django crea los permisos al ejecutar las migraciones. Las cuentas de acceso son las cuentas de Django; el modelo de negocio `usuarios.Usuario` es independiente.

Una persona sin iniciar sesión será enviada al formulario de acceso. Si inició sesión pero no tiene el permiso solicitado, recibirá una respuesta de acceso denegado. Las acciones que no puede realizar tampoco aparecen en las listas.
