from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.conf import settings
from django.views.decorators.clickjacking import xframe_options_exempt
import weasyprint 

# Importamos todos tus modelos
from .models import Perfil, Experiencia, Educacion, Proyecto, Certificado, Producto

def get_contexto_comun():
    # Esta función ayuda a no repetir código
    return {
        'perfil': Perfil.objects.first(),
    }

# --- VISTAS NORMALES (WEB) ---

def home(request):
    context = get_contexto_comun()
    context['active_tab'] = 'inicio'
    context['hide_sidebar'] = True 
    
    # Resúmenes para la portada
    context['ultimos_proyectos'] = Proyecto.objects.all().order_by('-id')[:2]
    context['ultima_educacion'] = Educacion.objects.all().order_by('-fecha')[:2]
    context['ultima_experiencia'] = Experiencia.objects.all().order_by('-fecha_inicio')[:2]
    context['ultimos_certificados'] = Certificado.objects.all().order_by('-id')[:4]
    context['ultimos_productos'] = Producto.objects.filter(disponible=True)[:3]
    
    return render(request, 'cv/home.html', context)

def experiencia(request):
    context = get_contexto_comun()
    context['active_tab'] = 'experiencia'
    context['experiencia'] = Experiencia.objects.all().order_by('-fecha_inicio')
    return render(request, 'cv/experiencia.html', context)

def educacion(request):
    context = get_contexto_comun()
    context['active_tab'] = 'educacion'
    # Recuerda que P. Académicos usa el modelo 'Educacion'
    context['productos_academicos'] = Educacion.objects.all().order_by('-fecha')
    return render(request, 'cv/educacion.html', context)

def proyectos(request):
    context = get_contexto_comun()
    context['active_tab'] = 'proyectos'
    context['proyectos'] = Proyecto.objects.all()
    return render(request, 'cv/proyectos.html', context)

def certificados(request):
    context = get_contexto_comun()
    context['active_tab'] = 'certificados'
    context['certificados'] = Certificado.objects.all()
    return render(request, 'cv/certificados.html', context)

def garage(request):
    context = get_contexto_comun()
    context['active_tab'] = 'garage'
    context['productos'] = Producto.objects.all()
    return render(request, 'cv/garage.html', context)

# --- VISTA GENERADOR DE PDF ---

@xframe_options_exempt 
def descargar_cv_pdf(request):
    if request.method == 'POST':
        # 1. Capturamos qué casillas marcó el usuario
        opciones = {
            'incluir_perfil': request.POST.get('incluir_perfil') == 'on',
            'incluir_experiencia': request.POST.get('incluir_experiencia') == 'on',
            'incluir_educacion': request.POST.get('incluir_educacion') == 'on',
            'incluir_proyectos': request.POST.get('incluir_proyectos') == 'on',
            'incluir_academicos': request.POST.get('incluir_academicos') == 'on',
            'incluir_certificados': request.POST.get('incluir_certificados') == 'on',
        }
        
        # 2. Preparamos el contexto
        context = get_contexto_comun()
        context['opciones'] = opciones
        context['MEDIA_ROOT'] = settings.MEDIA_ROOT
        
        # 3. CARGAMOS TODOS LOS DATOS SIEMPRE (El HTML decidirá si mostrarlos u ocultarlos)
        #    Esto soluciona el error de "si lo marco no aparece".
        context['experiencia'] = Experiencia.objects.all().order_by('-fecha_inicio')
        context['educacion'] = Educacion.objects.all().order_by('-fecha')
        context['proyectos'] = Proyecto.objects.all()
        context['certificados'] = Certificado.objects.all()
        
        # Truco: Duplicamos educación para la variable 'productos_academicos'
        context['productos_academicos'] = context['educacion']

        # 4. Renderizamos el HTML del PDF
        html = render_to_string('cv/pdf_template.html', context)
        response = HttpResponse(content_type='application/pdf')
        
        # 5. Configuración para Vista Previa vs Descarga
        accion = request.POST.get('action', 'download') 
        tipo_visualizacion = 'inline' if accion == 'preview' else 'attachment'
        
        response['Content-Disposition'] = f'{tipo_visualizacion}; filename="mi_cv.pdf"'
        
        # 6. Generar PDF
        weasyprint.HTML(string=html, base_url=request.build_absolute_uri()).write_pdf(response)
        return response
    
    return redirect('home')