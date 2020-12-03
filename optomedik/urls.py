from django.urls import path,include
from .import views

app_name="optomedik" 
urlpatterns = [    
    path('', views.index, name="index"), 
    path('', views.HomeView.as_view(), name='home'),
    path('', views.index, name="turnos"),         
    path("pacientes",views.listar_pacientes,name="url_listar_pacientes"),           
    path("turnos",views.listar_turnos,name="url_listar_turnos"),
    path("reportes",views.listar_reportes,name="url_listar_reportes"),
    path("rp",views.reporte_gerencia_pacientes,name="url_reporte_gerencia_pacientes"),  
    path("rpe",views.reporte_gerencia_pedidos,name="url_reporte_gerencia_pedidos"),  
    path("rpp",views.reporte_gerencia_productos,name="url_reporte_gerencia_productos"),  
    path("rv",views.reporte_gerencia_vendedor,name="url_reporte_gerencia_vendedor"),           
    path("hc/<int:paciente_id>",views.listar_hc,name="url_listar_hc"),
    path("pedidos",views.listar_pedidos,name="url_listar_pedidos"),
    path("pedido/<int:pedido_id>",views.listar_pedido_detalle,name="url_listar_pedido_detalle"), 
    path('pedido',views.nuevo_pedido, name="url_nuevo_pedido"),  
    path("pedido_detalle/<int:pedido_id>",views.agregar_producto,name="url_agregar_producto"), 
    path("hc",views.listar_hc2,name="url_listar_hc2"),
    path("<int:turno_id>",views.f_asignarturnos,name="url_asignarturnos"),          
    path('reservar',views.reservar, name="url_reservar"),
    path('<int:turno_id>/actualizar', views.actualizar, name="url_actualizar") ,   
    path('registro/<int:pk>/', views.turnoDetailView.as_view(), name='turno_detail'),
    path('registro/update/<int:pk>/', views.TurnoUpdateView.as_view(), name='turno_update'),    
    path('registro/delete/<int:pk>/', views.turnoDeleteView.as_view(), name='turno_delete'),
    path('registro/create/', views.HistoriaClinicaCreateView.as_view(), name='hc_create'),
    path('registrohc/update/<int:pk>/', views.HcUpdateView.as_view(), name='hc_update'),
    path('registrop/create/',views.PacienteCreateView.as_view(), name='paciente_create'),
    path('pedido/estado/<int:pk>/', views.PedidoUpdateView.as_view(), name='url_estado_pedido')
]

