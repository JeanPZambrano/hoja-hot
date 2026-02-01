from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.conf import settings
import weasyprint 

# IMPORTAMOS SOLO LOS NOMBRES REALES DE TUS MODELOS
from .models import Perfil, Experiencia, Educacion, Proyecto, Certificado, Producto

def get_contexto_comun():
    return {
        'perfil': Perfil.objects.first(),
    }

def home(request):
    context = get_contexto_comun()
    context['active_tab'] = 'inicio'
    context['hide_sidebar'] = True 
    
    # Usamos Educacion porque es el nombre real de tu clase
    context['proyectos_destacados'] = Proyecto.objects.all()[:2]
    context['educacion_destacada'] = Educacion.objects.all().order_by('-fecha')[:2]
    context['ultimos_proyectos'] = Proyecto.objects.all()[:2] 
    context['ultima_educacion'] = Educacion.objects.all().order_by('-fecha')[:2]
    
    return render(request, 'cv/home.html', context)

def experiencia(request):
    context = get_contexto_comun()
    context['active_tab'] = 'experiencia'
    context['experiencia'] = Experiencia.objects.all().order_by('-fecha_inicio')
    return render(request, 'cv/experiencia.html', context)

def educacion(request):
    context = get_contexto_comun()
    context['active_tab'] = 'educacion'
    # AQUÍ ESTÁ EL TRUCO: Sacamos datos de 'Educacion' pero los llamamos 'productos_academicos'
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

def descargar_cv_pdf(request):
    if request.method == 'POST':
        opciones = {
            'incluir_perfil': request.POST.get('incluir_perfil') == 'on',
            'incluir_experiencia': request.POST.get('incluir_experiencia') == 'on',
            'incluir_educacion': request.POST.get('incluir_educacion') == 'on',
            'incluir_proyectos': request.POST.get('incluir_proyectos') == 'on',
            'incluir_academicos': request.POST.get('incluir_academicos') == 'on',
            'incluir_certificados': request.POST.get('incluir_certificados') == 'on',
        }
        context = get_contexto_comun()
        context['opciones'] = opciones
        context['MEDIA_ROOT'] = settings.MEDIA_ROOT

        if opciones['incluir_experiencia']: 
            context['experiencia'] = Experiencia.objects.all().order_by('-fecha_inicio')
        
        # Si marcan Educación o P. Académicos, usamos el modelo Educacion
        if opciones['incluir_educacion'] or opciones['incluir_academicos']: 
            context['educacion'] = Educacion.objects.all().order_by('-fecha')
            context['productos_academicos'] = context['educacion']
            
        if opciones['incluir_proyectos']: 
            context['proyectos'] = Proyecto.objects.all()
        if opciones['incluir_certificados']: 
            context['certificados'] = Certificado.objects.all()

        html = render_to_string('cv/pdf_template.html', context)
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="mi_cv.pdf"'
        weasyprint.HTML(string=html, base_url=request.build_absolute_uri()).write_pdf(response)
        return response
    return redirect('home')