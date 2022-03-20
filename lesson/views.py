
from django.core.mail import send_mail
from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect

from django.views.generic import ListView

from . import models
from . import forms



# Create your views here.


class MaterialListView(LoginRequiredMixin, ListView):
    queryset = models.Material.objects.all()
    context_object_name = 'materials'
    template_name = "materials/all_materials.html"
#
# def all_materials(request):
#     materials = models.Material.objects.all()
#     return render(request, "materials/all_materials.html",
#                   {"materials": materials})

@login_required
def detailed_material(request, yy, mm, dd, slug):
    material = get_object_or_404(models.Material, publish__year=yy, 
                                publish__month=mm, publish__day=dd, slug=slug)
    if request.method == "POST":
            comment_form = forms.CommentForm(request.POST)
            if comment_form.is_valid():
                new_comment = comment_form.save(commit=False)
                new_comment.material = material
                new_comment.save()
                return redirect(material)
    else:
        comment_form = forms.CommentForm()

    return render(request, "materials/detailed_material.html",
                  {"material": material,
                   "form": comment_form})

def share_material(request, material_id):
    material = get_object_or_404(models.Material, id=material_id)
    if request.method == 'POST':
        form = forms.EmailMaterialForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            material_uri = request.build_absolute_uri(
                material.get_absolute_url()
                )
            subject = 'Someone shared with you material ' + material.title
            body_template = ('On our resource someone shared material with'
                             'you. \n\nlink to material: {link}\n\ncomment: '
                             '{comment}')
            body = body_template.format(link=material_uri, comment=cd['comment'])
            send_mail(subject, body, 'admin@my.com', (cd['to_email'],))
    else:
        form = forms.EmailMaterialForm()
    return render(request,
                  'materials/share.html',
                  {'material': material, 'form':form})


def create_material(request):
    if request.method == 'POST':
        material_form = forms.MaterialForm(request.POST)
        if material_form.is_valid():
            new_material = material_form.save(commit=False)
            new_material.author = User.objects.first()
            new_material.slug = new_material.title.replace(' ', '_')
            new_material.save()
            return render(request,
                          "materials/detailed_material.html",
                          {"material": new_material})

    else:
        material_form = forms.MaterialForm()
    return render(request,
                  'materials/create.html',
                  {'form': material_form})


def custom_login(request):
    if request.method == 'POST':
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(
                username=cd['username'],
                password=cd['password'],
            )
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponse('user was logged in')
                else:
                    return HttpResponse('user account is not activated')
            else:
                return HttpResponse('Incorrect User/Password')
    else:
        form = forms.LoginForm()
        return render(request, 'login.html', {'form': form})


def view_profile(request):
    return render(request, 'profile.html')