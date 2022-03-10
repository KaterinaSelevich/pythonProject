from django.contrib import admin
from django.urls import path, include
from . import views

app_name = 'lesson'
urlpatterns = [
    path('', views.all_materials, name = 'all_materials'),
    path('<int:yy>/<int:mm>/<int:dd>/<slug:slug>', 
         views.detailed_material, name = 'detailed_material'),
    path('<int:material_id>/share/', views.share_material,
         name='share_material'),
    path('create/', views.create_material,
         name='create_form'),

] 
