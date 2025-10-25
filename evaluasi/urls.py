from django.urls import path

from . import views

app_name = 'evaluasi'

urlpatterns = [
    path('', views.evaluasi_view, name='view'),
    path('peringkat/', views.peringkat_view, name='peringkat'),
]