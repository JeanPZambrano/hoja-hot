from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone  # <-- IMPORTANTE: Necesario para obtener la fecha de hoy

# --- VALIDACIÓN INDEPENDIENTE PARA FECHA DE NACIMIENTO ---
def validar_nacimiento(fecha):
    """ Valida que la fecha de nacimiento no sea en el futuro """
    if fecha:
        hoy = timezone.now().date()
        if fecha > hoy:
            raise ValidationError('⛔ Error: No puedes nacer en el futuro. La fecha máxima permitida es hoy.')

class Perfil(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    
    dni = models.CharField(max_length=10, verbose_name="Cédula/DNI", null=True, blank=True)
    
    # --- AQUI SE APLICA EL VALIDADOR ---
    fecha_nacimiento = models.DateField(
        null=True, 
        blank=True, 
        validators=[validar_nacimiento] # <-- Esto bloquea fechas futuras
    )
    
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

    def clean(self):
        super().clean()
        if self.dni:
            # Validación de DNI único (excluyendo el propio registro al editar)
            existe = Perfil.objects.filter(dni=self.dni).exclude(pk=self.pk).exists()
            if existe:
                raise ValidationError(f"⛔ Error: El DNI {self.dni} ya está registrado en otro perfil.")

class Experiencia(models.Model):
    perfil = models.ForeignKey(Perfil, on_delete=models.CASCADE, related_name='experiencias', verbose_name="Perfil Asociado", null=True, blank=True)
    
    cargo = models.CharField(max_length=100)
    empresa = models.CharField(max_length=100)
    descripcion = models.TextField()
    fecha_inicio = models.DateField(blank=True, null=True)
    fecha_fin = models.DateField(blank=True, null=True)

    logo = models.ImageField(upload_to='experiencia/logos/', null=True, blank=True, verbose_name="Logo Empresa / Imagen")
    archivo = models.FileField(upload_to='experiencia/archivos/', null=True, blank=True, verbose_name="Constancia/Archivo (PDF)")

    class Meta:
        verbose_name = "Experiencia"
        verbose_name_plural = "Experiencia Laboral"

    def __str__(self):
        return f"{self.cargo} en {self.empresa}"

    def clean(self):
        super().clean()
        if self.fecha_inicio and self.fecha_fin:
            if self.fecha_inicio > self.fecha_fin:
                raise ValidationError("⛔ Error: La fecha de inicio no puede ser posterior a la fecha de fin.")

class Educacion(models.Model):
    perfil = models.ForeignKey(Perfil, on_delete=models.CASCADE, related_name='educacion', verbose_name="Perfil Asociado", null=True, blank=True)
    
    titulo = models.CharField(max_length=100)
    institucion = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True, verbose_name="Descripción corta")
    fecha = models.DateField(null=True, blank=True, verbose_name="Fecha de Finalización")

    logo = models.ImageField(upload_to='educacion/logos/', null=True, blank=True, verbose_name="Logo Institución")
    archivo = models.FileField(upload_to='educacion/archivos/', null=True, blank=True, verbose_name="Archivo Adjunto (PDF)")

    class Meta:
        verbose_name = "Producto Académico"
        verbose_name_plural = "Productos Académicos"

    def __str__(self):
        return self.titulo

class Proyecto(models.Model):
    perfil = models.ForeignKey(Perfil, on_delete=models.CASCADE, related_name='proyectos', verbose_name="Perfil Asociado", null=True, blank=True)
    
    titulo = models.CharField(max_length=100)
    subtitulo = models.CharField(max_length=150, blank=True, null=True)
    descripcion = models.TextField()
    fecha = models.DateField(null=True, blank=True, verbose_name="Fecha de Realización")
    tecnologias = models.CharField(max_length=200, blank=True, null=True)
    link = models.URLField(blank=True, null=True)
    
    imagen = models.ImageField(upload_to='proyectos/', blank=True, null=True)
    logo = models.ImageField(upload_to='proyectos/logos/', null=True, blank=True, verbose_name="Logo Proyecto/Cliente")
    archivo = models.FileField(upload_to='proyectos/archivos/', null=True, blank=True, verbose_name="Archivo Adjunto (PDF)")

    class Meta:
        verbose_name = "Proyecto"
        verbose_name_plural = "Proyectos (Portafolio)"

    def __str__(self):
        return self.titulo

class Certificado(models.Model):
    perfil = models.ForeignKey(Perfil, on_delete=models.CASCADE, related_name='certificados', verbose_name="Perfil Asociado", null=True, blank=True)
    
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
    perfil = models.ForeignKey(Perfil, on_delete=models.CASCADE, related_name='productos_venta', verbose_name="Vendedor (Perfil)", null=True, blank=True)
    
    ESTADOS = [
        ('Nuevo', 'Nuevo / Sellado'),
        ('Como Nuevo', 'Como Nuevo (10/10)'),
        ('Buen Estado', 'Usado - Buen Estado'),
        ('Detalles', 'Usado - Con detalles estéticos'),
        ('Reparar', 'Para piezas / A reparar'),
    ]

    titulo = models.CharField(max_length=200)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    estado = models.CharField(max_length=50, choices=ESTADOS, default='Buen Estado', verbose_name="Condición")
    descripcion = models.TextField(blank=True, null=True, verbose_name="Descripción detallada")
    disponible = models.BooleanField(default=True)
    imagen = models.ImageField(upload_to='productos/', blank=True, null=True)

    class Meta:
        verbose_name = "Producto de Venta"
        verbose_name_plural = "Garage (Ventas)"

    def __str__(self):
        return self.titulo
    
    def clean(self):
        super().clean()
        if self.precio < 0:
            raise ValidationError("⛔ Error: El precio no puede ser negativo.")

class Curso(models.Model):
    perfil = models.ForeignKey(Perfil, on_delete=models.CASCADE, related_name='cursos', verbose_name="Perfil Asociado", null=True, blank=True)
    
    titulo = models.CharField(max_length=200, verbose_name="Título del Curso")
    descripcion = models.TextField(verbose_name="Descripción")
    fecha = models.DateField(verbose_name="Fecha de realización")
    
    pdf_archivo = models.FileField(upload_to='cursos/pdfs/', verbose_name="PDF del Curso")
    vista_previa = models.ImageField(upload_to='cursos/previews/', verbose_name="Imagen de Vista Previa", null=True, blank=True)
    archivo_extra = models.FileField(upload_to='cursos/extras/', blank=True, null=True, verbose_name="Archivo Extra")

    class Meta:
        verbose_name = "Curso"
        verbose_name_plural = "Cursos"
        ordering = ['-fecha']

    def __str__(self):
        return self.titulo