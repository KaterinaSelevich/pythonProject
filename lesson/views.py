from django.shortcuts import render, get_object_or_404
from . import models

# Create your views here.


def all_materials(request):
    materials = models.Material.objects.all()
    return render(request, 'materials/all_materials.html', {'materials': materials})


def detailed_material(request, yy, mm, dd, slug):
    material = get_object_or_404(models.Material, publish__year=yy, 
                                publish__month=mm, publish__day=dd, slug=slug)
    return render(request, 'materials/detailed_material.html',
                {'material': material})
