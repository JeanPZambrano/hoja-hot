from django.db import models
from django.core.exceptions import ValidationError  # <--- AGREGA ESTA LÍNEA

class Perfil(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    dni = models.CharField(max_length=10, verbose_name="Cédula/DNI", null=True, blank=True)
    fecha_nacimiento = models.DateField(null=True, blank=True)
    telefono = models.CharField(max_length=15)
    email = models.EmailField()
    profesion = models.CharField(max_length=100)
    ubicacion = models.CharField(max_length=200)
    sector = models.CharField(max_length=100, verbose_name="Barrio/Sector", null=True, blank=True)
    resumen = models.TextField()
    foto = models.ImageField(upload_to='perfil/', null=True, blank=True)

    class Meta:
        verbose_name = "Perfil"
        verbose_name_plural = "Perfil (Información Personal)"

    def __str__(self):
        return f"{self.nombre} {self.apellido}"

class Experiencia(models.Model):
    cargo = models.CharField(max_length=100)
    empresa = models.CharField(max_length=100)
    descripcion = models.TextField()
    fecha_inicio = models.DateField(blank=True, null=True)
    fecha_fin = models.DateField(blank=True, null=True)

    class Meta:
        verbose_name = "Experiencia"
        verbose_name_plural = "Experiencia Laboral"

    def __str__(self):
        return f"{self.cargo} en {self.empresa}"

    # --- AQUÍ ESTÁ LA VALIDACIÓN MÁGICA ---
    def clean(self):
        super().clean()
        
        # 1. Validar que la Fecha de Inicio no sea mayor que la Fecha de Fin
        if self.fecha_inicio and self.fecha_fin:
            if self.fecha_inicio > self.fecha_fin:
                raise ValidationError("⛔ Error: La fecha de inicio no puede ser posterior a la fecha de fin.")

class Educacion(models.Model):
    titulo = models.CharField(max_length=100)
    institucion = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True, verbose_name="Descripción corta")
    
    # --- CAMBIO: Agregamos el campo FECHA ---
    fecha = models.DateField(null=True, blank=True, verbose_name="Fecha de Finalización")

    class Meta:
        verbose_name = "Producto Académico"
        verbose_name_plural = "Productos Académicos"

    def __str__(self):
        return self.titulo

    class Meta:
        # Aquí se mantiene el nombre que pediste para el Admin
        verbose_name = "Producto Académico"
        verbose_name_plural = "Productos Académicos"

    def __str__(self):
        return self.titulo

class Proyecto(models.Model):
    titulo = models.CharField(max_length=100)
    subtitulo = models.CharField(max_length=150, blank=True, null=True)
    descripcion = models.TextField()
    
    # --- CAMBIO IMPORTANTE: Campo fecha agregado ---
    fecha = models.DateField(null=True, blank=True, verbose_name="Fecha de Realización")
    
    tecnologias = models.CharField(max_length=200, blank=True, null=True)
    link = models.URLField(blank=True, null=True)
    imagen = models.ImageField(upload_to='proyectos/', blank=True, null=True)

    class Meta:
        verbose_name = "Proyecto"
        verbose_name_plural = "Proyectos (Portafolio)"

    def __str__(self):
        return self.titulo

class Certificado(models.Model):
    titulo = models.CharField(max_length=100)
    institucion = models.CharField(max_length=100)
    fecha = models.DateField(blank=True, null=True)
    archivo = models.FileField(upload_to='certificados/', blank=True, null=True)

    class Meta:
        verbose_name = "Certificado"
        verbose_name_plural = "Certificados"

    def __str__(self):
        return self.titulo

class Producto(models.Model):
    # Opciones para el estado del producto
    ESTADOS = [
        ('Nuevo', 'Nuevo / Sellado'),
        ('Como Nuevo', 'Como Nuevo (10/10)'),
        ('Buen Estado', 'Usado - Buen Estado'),
        ('Detalles', 'Usado - Con detalles estéticos'),
        ('Reparar', 'Para piezas / A reparar'),
    ]

    titulo = models.CharField(max_length=200)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    
    # --- NUEVOS CAMPOS ---
    estado = models.CharField(max_length=50, choices=ESTADOS, default='Buen Estado', verbose_name="Condición")
    descripcion = models.TextField(blank=True, null=True, verbose_name="Descripción detallada")
    
    disponible = models.BooleanField(default=True)
    imagen = models.ImageField(upload_to='productos/', blank=True, null=True)

    class Meta:
        verbose_name = "Producto de Venta"
        verbose_name_plural = "Garage (Ventas)"

    def __str__(self):
        return self.titulo