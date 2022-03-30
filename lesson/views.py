from turtle import title
from django.views.generic import ListView
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


from . import models
from . import forms



# Create your views here.


class TeamListView(LoginRequiredMixin, ListView):
    queryset = models.Team.objects.all()
    context_object_name = 'teams'
    template_name = "teams/all_teams.html"
#
# def all_teams(request):
#     teams = models.Team.objects.all()
#     return render(request, "teams/all_teams.html",
#                   {"teams": teams})

@login_required
def detailed_team(request, yy, mm, dd, slug):
    team = get_object_or_404(models.Team, publish__year=yy, 
                                publish__month=mm, publish__day=dd, slug=slug)
    if request.method == "POST":
            comment_form = forms.CommentForm(request.POST)
            if comment_form.is_valid():
                new_comment = comment_form.save(commit=False)
                new_comment.team = team
                new_comment.save()
                return redirect(team)
    else:
        comment_form = forms.CommentForm()

    return render(request, "teams/detailed_team.html",
                  {"team": team,
                   "form": comment_form})

def share_team(request, team_id):
    team = get_object_or_404(models.Team, id=team_id)
    if request.method == 'POST':
        form = forms.EmailTeamForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            team_uri = request.build_absolute_uri(
                team.get_absolute_url()
                )
            subject = 'Someone shared with you team ' + team.title
            body_template = ('On our resource someone shared team with'
                             'you. \n\nlink to team: {link}\n\ncomment: '
                             '{comment}')
            body = body_template.format(link=team_uri, comment=cd['comment'])
            send_mail(subject, body, 'admin@my.com', (cd['to_email'],))
    else:
        form = forms.EmailTeamForm()
    return render(request,
                  'teams/share.html',
                  {'team': team, 'form':form})


def create_team(request):
    if request.method == 'POST':
        team_form = forms.TeamForm(request.POST)
        if team_form.is_valid():
            new_team = team_form.save(commit=False)
            new_team.author = User.objects.first()
            new_team.slug = new_team.title.replace(' ', '_')
            new_team.save()
            return render(request,
                          "teams/detailed_team.html",
                          {"team": new_team})

    else:
        team_form = forms.TeamForm()
    return render(request,
                  'teams/create.html',
                  {'form': team_form})


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


def register(request):
    if request.method == "POST":
        user_form = forms.RegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            models.Profile.objects.create(user=new_user, photo="unknown.jpg")
            return render(request, 'registration/registration_complete.html',
                          {'new_user': new_user})
        else:
            return HttpResponse('bad credentials')
    else:
        user_form = forms.RegistrationForm(request.POST)
        return render(request, 'registration/register_user.html', {"form": user_form})


class SearchResultsView(ListView):
    model = models.Team
    template_name = 'teams/search_results.html'

    def get_queryset(self): 
        object_list = models.Team.objects.filter(
            title=self.request.GET.get('q')
            )
        return object_list


def _get_forms(request, post_method):
    user_form = forms.UserEditForm(request.POST, instance=request.user)

    kw = {'instance': request.user.profile}
    if post_method: kw.update({'files': request.FILES})

    profile_form = forms.ProfileEditForm(request.POST, **kw)

    return user_form, profile_form


def edit_profile(request):
    post_method = request.method == "POST"
    user_form, profile_form = _get_forms(request, post_method)

    if post_method:
        if profile_form.is_valid():
            if user_form.is_valid():
                if not profile_form.cleaned_data['photo']:
                    profile_form.cleaned_data['photo'] = request.user.profile.photo
                profile_form.save()
                user_form.save()
                return render(request, 'profile.html')
    else:
        return render(request, 'edit_profile.html',
                      {'user_form': user_form, 'profile_form': profile_form})
