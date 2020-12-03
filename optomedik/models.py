# Create your models here.
from django.db import models
from django.urls import reverse

from django.contrib.auth.models import User,Group

class perfil(models.Model):
    #user = models.ForeignKey(User, unique=True)
    perfil = models.OneToOneField(Group, on_delete=models.CASCADE)
    descripcion = models.TextField()   
    tipo=models.CharField(max_length=3)     
    
# Create your models here.
class userprofile(models.Model):
    #user = models.ForeignKey(User, unique=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    id_perfil = models.ForeignKey(perfil, on_delete=models.CASCADE ,null=False, related_name="fk_perfil")
    
class paciente(models.Model):
    nombre = models.CharField(max_length=64)
    telefono = models.IntegerField()
    direccion = models.CharField(max_length=64,null=True)
    ciudad = models.CharField(max_length=64,null = True)
    
    class Meta:
        verbose_name = 'registrop'
        verbose_name_plural = 'optomedik'

    def __str__(self):
        return self.nombre

    def get_absolute_url(self):
        return reverse('optomedik:url_listar_pacientes', kwargs={"pk": self.pk})

class medico(models.Model):
    nombre = models.CharField(max_length=64)
    telefono = models.IntegerField()
    #user = models.ForeignKey(User, null=True, blank=True, default = None)
    #ssigned_to = models.ForeignKey('auth.User', related_name='missions_assigned', blank = True)
    user = models.ForeignKey(User,models.SET_NULL, blank=True, null=True,)
    
    def __str__(self):
        return self.nombre
class historia_clinica(models.Model):
    id_medico = models.ForeignKey(medico, on_delete=models.CASCADE, related_name="fk_medico_hc")
    id_paciente = models.ForeignKey(paciente, on_delete=models.CASCADE, related_name="fk_paciente_hc")   
    fecha = models.DateField(null = True)     
    observaciones = models.TextField()

    class Meta:
        verbose_name = 'registrohc'
        #verbose_name_plural = 'optomedik'

    def __str__(self):
        return self.id_medico
        #return '%s %s' % (self.id_paciente, self.id_medico)

    def get_absolute_url(self):
        return reverse('optomedik:url_listar_hc', kwargs={"pk": self.pk})
        
class tipo_pago(models.Model):
    descripcion = models.CharField(max_length=64)

class vendedor(models.Model):
    nombre = models.CharField(max_length=64)
class pedido(models.Model):
    fecha = models.DateField(null = True)
    id_paciente = models.ForeignKey(paciente, on_delete=models.CASCADE, related_name="fk_paciente_p")
    tipo_pago = models.ForeignKey(tipo_pago, on_delete=models.CASCADE, related_name="fk_tipo_pago")
    estado=models.TextField() 
    id_vendedor = models.ForeignKey(vendedor, on_delete=models.CASCADE, null=True,related_name="fk_vendedor")
     
    PEDIDO = 'PEDIDO' 
    TALLER = 'TALLER' 
    FINALIZADO = 'FINALIZADO'     
    PARADIGM_CHOICES = (
        
        (PEDIDO, 'PEDIDO'),
        (TALLER, 'TALLER'),
        (FINALIZADO, 'FINALIZADO'),        
    )
    estado = models.CharField(
        choices=PARADIGM_CHOICES, 
        default=PEDIDO, 
        blank=False, 
        max_length=20
    )

class producto(models.Model):
    nombre_producto = models.CharField(max_length=64)
    #armazon = models.BooleanField(default=False, help_text='SI or NO')
    #lente = models.BooleanField(default=False, help_text='SI or NO')

    SI = 'SI' 
    NO = 'NO'     
    PARADIGM_CHOICES = ( (SI, 'SI'), (NO, 'NO') )
    armazon = models.CharField(
        choices=PARADIGM_CHOICES, 
        default=NO, 
        blank=False, 
        max_length=20
    )

    NA = 'NO ES LENTE' 
    LI = 'LEJOS/IZQUIERDA'
    LD =  'LEJOS/DERECHA'
    CI= 'CERCA/IZQUIERDA'
    CD= 'CERCA/DERECHA'  
    PARADIGM_CHOICES = (
        (NA, 'NO ES LENTE'),
        (LI, 'LEJOS/IZQUIERDA'),
        (LD, 'LEJOS/DERECHA'),
        (CI, 'CERCA/IZQUIERDA'),
        (CD, 'CERCA/DERECHA'),
    )
    lente = models.CharField(
        choices=PARADIGM_CHOICES, 
        default=NA, 
        blank=False, 
        max_length=20
    )

class pedido_detalle(models.Model):
    id_pedido = models.ForeignKey(pedido, on_delete=models.CASCADE, related_name="fk_pedido_id")
    id_producto = models.ForeignKey(producto, on_delete=models.CASCADE, related_name="fk_producto_id")    
    cantidad = models.IntegerField()
    precio = models.FloatField()

class turnos(models.Model):    
    fecha = models.DateField(null = True)
    id_medico = models.ForeignKey(medico, on_delete=models.CASCADE,related_name="fk_medico")
    id_paciente = models.ForeignKey(paciente, on_delete=models.CASCADE, related_name="fk_paciente")        

    SI = 'SI' 
    NO = 'NO'     
    PARADIGM_CHOICES = ( (SI, 'SI'), (NO, 'NO') )
    asistio = models.CharField(
        choices=PARADIGM_CHOICES, 
        default=NO, 
        blank=False, 
        max_length=20
    )
    class Meta:
        verbose_name = 'registro'
        verbose_name_plural = 'optomedik'

    def __str__(self):
        return self.id_medico
        #return self.id_paciente, self.id_medico
        #return '%s %s' % (self.id_paciente, self.id_medico)
        

    def get_absolute_url(self):
        return reverse('optomedik:turno_detail', kwargs={"pk": self.pk})