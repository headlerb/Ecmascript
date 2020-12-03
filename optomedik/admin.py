from django.contrib import admin
from .models import paciente,medico,turnos,historia_clinica,tipo_pago,producto,pedido,vendedor,pedido_detalle,userprofile,perfil
# Register your models here.
admin.site.register(perfil)
admin.site.register(userprofile)
admin.site.register(paciente)
admin.site.register(medico)
admin.site.register(turnos)
admin.site.register(historia_clinica)
admin.site.register(tipo_pago)
admin.site.register(producto)
admin.site.register(pedido)
admin.site.register(pedido_detalle)
admin.site.register(vendedor)