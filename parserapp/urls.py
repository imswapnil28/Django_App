from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('parse/', views.parse_text, name='parse_text'),
]
