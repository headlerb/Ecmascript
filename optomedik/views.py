from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse,Http404,HttpResponseRedirect
from django.urls import reverse
from .models import paciente,turnos,medico,historia_clinica,userprofile,pedido,pedido_detalle,tipo_pago,producto,vendedor
from datetime import date,datetime
from django.db.models import Count,Sum

from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

# Create your views here.


def index(request):

    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))    
    
    queryset_perfil = userprofile.objects.filter(user=request.user.id).select_related('id_perfil').all() 
    v_perfil = []
    for perfil in queryset_perfil:               
        #v_perfil.append({'id': perfil.id  , 'user': perfil.user,'user_id': perfil.user_id, 'descripcion':perfil.id_perfil.descripcion })        
        v_perfil.append({'id': perfil.id  , 'user': perfil.user,'user_id': perfil.user_id ,'descripcion': perfil.id_perfil.descripcion,'tipo': perfil.id_perfil.tipo })
    return render(request,"optomedik/index.html",{
        "cxto_profile":v_perfil
    })
def listar_reportes(request):
    return render(request,"optomedik/reportes.html")
def listar_turnos(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))   
    ############### PERFIL 
    queryset_perfil = userprofile.objects.filter(user=request.user.id).select_related('id_perfil').all() 
    es_medico=0
    v_perfil = []
    for perfil in queryset_perfil:                       
        v_perfil.append({'id': perfil.id  , 'user': perfil.user,'user_id': perfil.user_id ,'descripcion': perfil.id_perfil.descripcion,'tipo': perfil.id_perfil.tipo })
        es_medico=perfil.id_perfil.tipo
    ############### PERFIL
    unMedico_id_medico=0
    unMedico_nombre=""
    if es_medico=="M":
        unMedico = medico.objects.get(user=request.user.id)        
        queryset = turnos.objects.filter(fecha=date.today(),id_medico=unMedico.id).select_related('id_paciente').all()
    else:
        queryset = turnos.objects.filter(fecha=date.today()).select_related('id_paciente').all()
        
    v_turnos = []
    v_pacientes = []
    
    if es_medico=="S":
        Crear=True
        Modificar=True
    else:
        Crear=False
        Modificar=False
    for turno in queryset:       
        v_turnos.append({'id': turno.id, 'asistio': turno.asistio,'fecha': turno.fecha, 'paciente':turno.id_paciente.nombre,'medico':turno.id_medico.nombre })
        v_pacientes.append(turno.id_paciente.pk)
    
    lospacientes = paciente.objects.exclude(id__in=v_pacientes)
    return render(request,"optomedik/turnos.html",{                               
        "Ctxto_paciente":lospacientes,
        "Ctxto_medico": medico.objects.all(),
        "Ctxto_turnos_medico":v_turnos,
        "Ctxto_fecha" : date.today(),
        "cxto_profile":v_perfil,
        "es_medico":es_medico,
        "Crear":Crear,
        "Modificar":Modificar
        
        
    })       
def f_asignarturnos(request, turno_id):
    unTurno = turnos.objects.get(id=turno_id) 
    queryset = turnos.objects.filter(fecha=date.today()).select_related('id_paciente').all()
    v_pacientes = []
    for turno in queryset: 
        v_pacientes.append(turno.id_paciente.pk)
    lospacientes = paciente.objects.exclude(id__in=v_pacientes)
    return render(request, "optomedik/turno.html",{
        "Ctxto_paciente":lospacientes,
        "Ctxto_medico": medico.objects.all(),
        "ctxo_turno":unTurno
    })
def listar_pacientes(request): 
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
    if request.method =="POST":
        fecha=request.POST["fecha"]
    #    fecha=date.today        
    else:        
        fecha=date.today()        
    ############### PERFIL                
    queryset_perfil = userprofile.objects.filter(user=request.user.id).select_related('id_perfil').all()   
    es_medico=0  
    v_perfil = []
    for perfil in queryset_perfil:   
        v_perfil.append({'id': perfil.id  , 'user': perfil.user,'user_id': perfil.user_id ,'descripcion': perfil.id_perfil.descripcion,'tipo': perfil.id_perfil.tipo })                            
        es_medico=perfil.id_perfil.tipo
    ############### PERFIL        
    if es_medico=="M":
        unMedico = medico.objects.get(user=request.user.id)        
        queryset = historia_clinica.objects.filter(id_medico=unMedico.id,fecha=fecha).select_related('id_paciente').all()        
    else:
        queryset = historia_clinica.objects.filter(fecha=fecha).select_related('id_paciente').all()        
        #queryset = paciente.objects.all()
    v_pacientes = []
    for unpaciente in queryset:
                
        v_pacientes.append({'id': unpaciente.id_paciente.id,'fecha': unpaciente.fecha ,'nombre': unpaciente.id_paciente.nombre, 'telefono':unpaciente.id_paciente.telefono,'direccion':unpaciente.id_paciente.direccion,'ciudad':unpaciente.id_paciente.ciudad })

            
    return render(request,"optomedik/paciente.html",{        
        "Ctxto_paciente":v_pacientes,
        "cxto_profile":v_perfil,
        "es_medico":es_medico
    }) 
def listar_hc(request,paciente_id):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))  
    queryset_perfil = userprofile.objects.filter(user=request.user.id).select_related('id_perfil').all() 
    es_medico=0
    v_perfil = []
    for perfil in queryset_perfil:                       
        v_perfil.append({'id': perfil.id  , 'user': perfil.user,'user_id': perfil.user_id ,'descripcion': perfil.id_perfil.descripcion,'tipo': perfil.id_perfil.tipo })
        es_medico=perfil.id_perfil.tipo
    ############### PERFIL
    
    
    if es_medico=="M":
        unMedico = medico.objects.get(user=request.user.id) 
        if paciente_id==0:       
            queryset = historia_clinica.objects.filter(id_medico=unMedico.id).select_related('id_paciente').all()
        else:
            queryset = historia_clinica.objects.filter(id_medico=unMedico.id,id_paciente=paciente_id).select_related('id_paciente').all()   
    else:
        if paciente_id==0:   
            queryset = historia_clinica.objects.all().select_related('id_paciente').all()
        else:
           queryset = historia_clinica.objects.filter(id_paciente=paciente_id).select_related('id_paciente').all()
    v_hc = []    
    for hc in queryset:       
        v_hc.append({'id': hc.id, 'fecha': hc.fecha, 'paciente':hc.id_paciente.nombre,'medico':hc.id_medico.nombre,'observaciones':hc.observaciones })
    
    return render(request,"optomedik/hc.html",{        
        "Ctxto_hc": v_hc,
        "cxto_profile":v_perfil,
        "es_medico":es_medico     
    })   
def listar_hc2(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))  
    queryset_perfil = userprofile.objects.filter(user=request.user.id).select_related('id_perfil').all() 
    es_medico=0
    v_perfil = []
    for perfil in queryset_perfil:                       
        v_perfil.append({'id': perfil.id  , 'user': perfil.user,'user_id': perfil.user_id ,'descripcion': perfil.id_perfil.descripcion,'tipo': perfil.id_perfil.tipo })
        es_medico=perfil.id_perfil.tipo
    ############### PERFIL
    
    
    if es_medico=="M":
        unMedico = medico.objects.get(user=request.user.id) 
        queryset = historia_clinica.objects.filter(id_medico=unMedico.id).select_related('id_paciente').all()
    else:
        queryset = historia_clinica.objects.all().select_related('id_paciente').all()
        
    v_hc = []    
    for hc in queryset:       
        v_hc.append({'id': hc.id, 'fecha': hc.fecha, 'paciente':hc.id_paciente.nombre,'medico':hc.id_medico.nombre,'observaciones':hc.observaciones })
    
    return render(request,"optomedik/hc.html",{        
        "Ctxto_hc": v_hc,
        "cxto_profile":v_perfil,
        "es_medico":es_medico     
    })      
def listar_pedidos(request):  
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))   
    ############### PERFIL 
    queryset_perfil = userprofile.objects.filter(user=request.user.id).select_related('id_perfil').all() 
    es_medico=0
    v_perfil = []
    for perfil in queryset_perfil:                       
        v_perfil.append({'id': perfil.id  , 'user': perfil.user,'user_id': perfil.user_id ,'descripcion': perfil.id_perfil.descripcion,'tipo': perfil.id_perfil.tipo })
        es_medico=perfil.id_perfil.tipo
    ############### PERFIL
    if es_medico=="V":
        Crear=True
        Modificar=True
    else:
        Crear=False
        Modificar=False
    queryset = pedido.objects.all().select_related('id_paciente').all()
    v_pedidos = []    
    for pedidos in queryset:       
        v_pedidos.append({'id': pedidos.id, 'fecha': pedidos.fecha, 'paciente':pedidos.id_paciente.nombre,'estado':pedidos.estado,'tipo_pago':pedidos.tipo_pago })
    
    return render(request,"optomedik/pedidos.html",{              
        "Ctxto_pedido": v_pedidos,
        "Ctxto_paciente":paciente.objects.all(),
        "Ctxto_vendedor":vendedor.objects.all(),
        "Ctxto_tipo_pago":tipo_pago.objects.all(),
        "cxto_profile":v_perfil,
        "es_medico":es_medico, 
        "Crear":Crear, 
        "Modificar":Modificar   
    })     
def listar_pedido_detalle(request,pedido_id):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))  
    queryset_perfil = userprofile.objects.filter(user=request.user.id).select_related('id_perfil').all() 
    es_medico=0
    Total_pedido=0
    v_perfil = []
    for perfil in queryset_perfil:                       
        v_perfil.append({'id': perfil.id  , 'user': perfil.user,'user_id': perfil.user_id ,'descripcion': perfil.id_perfil.descripcion,'tipo': perfil.id_perfil.tipo })
        es_medico=perfil.id_perfil.tipo
    ############### PERFIL
    if es_medico=="V":
        Crear=True
        Modificar=True
    else:
        Crear=False
        Modificar=False
    if es_medico=="T":
        ver_precio=False
    else:
        ver_precio=True
    queryset = pedido_detalle.objects.filter(id_pedido=pedido_id).select_related('id_producto').all()

    v_pedido_detalle = []    
    for productos in queryset: 
        Total= productos.cantidad*productos.precio 
        Total_pedido= Total_pedido + Total      
        v_pedido_detalle.append({'id': productos.id, 'producto':productos.id_producto.nombre_producto,'cantidad':productos.cantidad,'precio':productos.precio,'total_item':Total,'armazon':productos.id_producto.armazon,'lente':productos.id_producto.lente })
    unPedido = pedido.objects.get(id=pedido_id)
    return render(request,"optomedik/pedidos_detalle.html",{  
        "unPedido":unPedido,
        "pedido_id":pedido_id,      
        "Ctxto_pedido": v_pedido_detalle,
        "Ctxto_productos": producto.objects.all(),
        "cxto_profile":v_perfil,
        "es_medico":es_medico,
        "Crear":Crear, 
        "Modificar":Modificar,
        "ver_precio":ver_precio,
        "Total_pedido":Total_pedido 
    }) 
def reservar(request):
    if request.method =="POST":
        #unVuelo = Vuelo.objects.get(pk=vuelo_id)  
        paciente_id=int(request.POST["paciente"])
        medico_id=int(request.POST["medico"])        
        unMedico = medico.objects.get(pk=medico_id)          
        unPaciente = paciente.objects.get(pk=paciente_id)          
        today = date.today()
        turno = turnos(fecha=today,id_medico=unMedico,id_paciente=unPaciente)        
        turno.save()        
        return HttpResponseRedirect(reverse("optomedik:url_listar_turnos", args=()))
def nuevo_pedido(request):
    if request.method =="POST":
        paciente_id=int(request.POST["paciente"])
        tipo_pago_id=int(request.POST["tipo_pago"])        
        vendedor_id=int(request.POST["vendedor"])        
        Untipo_pago = tipo_pago.objects.get(pk=tipo_pago_id)          
        unPaciente = paciente.objects.get(pk=paciente_id)
        unVendedor = vendedor.objects.get(pk=vendedor_id)          
        today = date.today()
        pedidos = pedido(fecha=today,tipo_pago=Untipo_pago,id_paciente=unPaciente,estado="PENDIENTE",id_vendedor=unVendedor)        
        pedidos.save()        
        return HttpResponseRedirect(reverse("optomedik:url_listar_pedidos", args=()))
def agregar_producto(request,pedido_id):
    if request.method =="POST":   
        producto_id=int(request.POST["producto"])
        cantidad=int(request.POST["cantidad"])
        precio=int(request.POST["precio"])     
        Unpedido = pedido.objects.get(pk=pedido_id)   
        Unproducto = producto.objects.get(pk=producto_id)          
        
        pedido_detalle_productos = pedido_detalle(id_pedido=Unpedido,id_producto=Unproducto,cantidad=cantidad,precio=precio)        
        pedido_detalle_productos.save()        
        return HttpResponseRedirect(reverse("optomedik:url_listar_pedido_detalle", args=(pedido_id,)))
              
def actualizar(request,turno_id): 
    if request.method =="POST":
      
        turno = turnos.objects.get(pk=turno_id) 
        
        today = date.today()
        
        paciente_id=int(request.POST["paciente"])
        turno.id_paciente=paciente_id
        
        turno.save()        
        return HttpResponseRedirect(reverse("optomedik:url_listar_turnos", args=()))     
##########################
class HomeView(ListView):
    model = turnos
    template_name = 'optomedik/index.html'
    paginate_by = 10
################Actualizando Turnos
class TurnoUpdateView(UpdateView):
    model = turnos    
    success_url = reverse_lazy('optomedik:url_listar_turnos')
    template_name = 'optomedik/turno_create.html'
    fields = ['fecha', 'id_paciente', 'id_medico','asistio']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['edit'] = True
        return context 
class turnoDetailView(DetailView):
    model = turnos    
    template_name = 'optomedik/turno_detail.html'
class turnoDeleteView(DeleteView):
    model = turnos
    success_url = reverse_lazy('optomedik:url_listar_turnos')
    template_name = 'optomedik/confirm_turno_deletion.html'
    
class HistoriaClinicaCreateView(CreateView):
    model = historia_clinica
    success_url = reverse_lazy('optomedik:url_listar_hc2')
    template_name = 'optomedik/hc_create.html'
    fields = ['id_medico', 'id_paciente', 'fecha', 'observaciones']
class HcUpdateView(UpdateView):
    model = historia_clinica    
    success_url = reverse_lazy('optomedik:url_listar_hc2')
    template_name = 'optomedik/hc_create.html'    
    fields = ['id_medico', 'id_paciente', 'fecha', 'observaciones']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['edit'] = True
        return context       
class PacienteCreateView(CreateView):
    model = paciente
    success_url = reverse_lazy('optomedik:url_listar_pacientes')
    template_name = 'optomedik/paciente_create.html'
    fields = ['nombre', 'telefono', 'direccion', 'ciudad']        

class PedidoUpdateView(UpdateView):
    model = pedido
       
    success_url = reverse_lazy('optomedik:url_listar_pedidos')
    template_name = 'optomedik/pedido_create.html'    
    fields = ['estado']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['edit'] = True
        return context

def reporte_gerencia_pacientes(request): 
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
    
    if request.method =="POST":
        fecha=request.POST["fecha"]
        fecha_final=request.POST["fecha_final"]   
        asistio=request.POST["asistio"]
        pedido=request.POST["pedido"]       
    else:        
        fecha=date.today()        
        fecha_final=date.today() 
        asistio="SI"
        pedido="SI"
    
    ############### PERFIL                 
    queryset_perfil = userprofile.objects.filter(user=request.user.id).select_related('id_perfil').all()   
    es_medico=0  
    v_perfil = []
    for perfil in queryset_perfil:   
        v_perfil.append({'id': perfil.id  , 'user': perfil.user,'user_id': perfil.user_id ,'descripcion': perfil.id_perfil.descripcion,'tipo': perfil.id_perfil.tipo })                            
        es_medico=perfil.id_perfil.tipo
    ############### PERFIL        
    
    queryset = turnos.objects.filter(asistio=asistio,fecha__range=(fecha, fecha_final)).select_related('id_paciente').all()        
  
    v_pacientes = []
    for unpaciente in queryset:      
        v_pacientes.append({'id': unpaciente.id_paciente.id,'turno': unpaciente.id,'asistio': unpaciente.asistio,'fecha': unpaciente.fecha ,'nombre': unpaciente.id_paciente.nombre, 'telefono':unpaciente.id_paciente.telefono,'direccion':unpaciente.id_paciente.direccion,'ciudad':unpaciente.id_paciente.ciudad })
        
    return render(request,"optomedik/reporte_paciente.html",{        
        "Ctxto_paciente":v_pacientes,
        "cxto_profile":v_perfil,
        "es_medico":es_medico
    }) 
def reporte_gerencia_pedidos(request): 

    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
    
    if request.method =="POST":
        fecha=request.POST["fecha"]
        fecha_final=request.POST["fecha_final"]  
    else:        
        fecha=date.today()        
        fecha_final=date.today() 
    ############### PERFIL     
   
                
    queryset_perfil = userprofile.objects.filter(user=request.user.id).select_related('id_perfil').all()   
    es_medico=0  
    v_perfil = []
    for perfil in queryset_perfil:   
        v_perfil.append({'id': perfil.id  , 'user': perfil.user,'user_id': perfil.user_id ,'descripcion': perfil.id_perfil.descripcion,'tipo': perfil.id_perfil.tipo })                            
        es_medico=perfil.id_perfil.tipo
    ############### PERFIL        
    
    queryset = pedido.objects.filter(fecha__range=(fecha, fecha_final)).select_related('id_paciente').all()        
  
    v_pedido = []
    for unpedido in queryset:      
        v_pedido.append({'id': unpedido.id,'fecha': unpedido.fecha ,'nombre': unpedido.id_paciente.nombre, 'telefono':unpedido.id_paciente.telefono,'direccion':unpedido.id_paciente.direccion,'ciudad':unpedido.id_paciente.ciudad })
        
    return render(request,"optomedik/reporte_pedidos.html",{        
        "Ctxto_paciente":v_pedido,
        "cxto_profile":v_perfil,
        "es_medico":es_medico
    }) 
def reporte_gerencia_productos(request): 

    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
    
    if request.method =="POST":
        fecha=request.POST["fecha"]
        fecha_final=request.POST["fecha_final"]  
    else:        
        fecha=date.today()        
        fecha_final=date.today() 
        
    
    ############### PERFIL                     
    queryset_perfil = userprofile.objects.filter(user=request.user.id).select_related('id_perfil').all()   
    es_medico=0  
    v_perfil = []
    for perfil in queryset_perfil:   
        v_perfil.append({'id': perfil.id  , 'user': perfil.user,'user_id': perfil.user_id ,'descripcion': perfil.id_perfil.descripcion,'tipo': perfil.id_perfil.tipo })                            
        es_medico=perfil.id_perfil.tipo
    ############### PERFIL        

    queryset = pedido_detalle.objects.values('id_producto').order_by('id_producto').annotate(total=Sum('cantidad'))

    return render(request,"optomedik/reporte_productos.html",{        
        "Ctxto_paciente":queryset,
        "cxto_profile":v_perfil,
        "es_medico":es_medico
    }) 

def reporte_gerencia_vendedor(request): 

    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))    
    
    ############### PERFIL     
    queryset_perfil = userprofile.objects.filter(user=request.user.id).select_related('id_perfil').all()   
    es_medico=0  
    v_perfil = []
    for perfil in queryset_perfil:   
        v_perfil.append({'id': perfil.id  , 'user': perfil.user,'user_id': perfil.user_id ,'descripcion': perfil.id_perfil.descripcion,'tipo': perfil.id_perfil.tipo })                            
        es_medico=perfil.id_perfil.tipo
    ############### PERFIL        
    
      
    
    queryset = pedido.objects.values('id_vendedor').order_by('id_vendedor').annotate(total=Count('id_vendedor'))
    return render(request,"optomedik/reporte_vendedor.html",{        
        "Ctxto_vendedor":queryset,
        "cxto_profile":v_perfil,
        "es_medico":es_medico
    }) 