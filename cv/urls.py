from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('experiencia/', views.experiencia, name='experiencia'),
    path('educacion/', views.educacion, name='educacion'),
    path('proyectos/', views.proyectos, name='proyectos'),
    path('certificados/', views.certificados, name='certificados'),
    path('garage/', views.garage, name='garage'),
    path('descargar-pdf/', views.descargar_cv_pdf, name='descargar_cv_pdf'),
]