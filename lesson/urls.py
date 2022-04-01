from django.contrib import admin
from django.urls import path, include
from django.urls import reverse_lazy
from .views import SearchResultsView, AboutPageView

from django.contrib.auth import views as auth_views
from . import views


app_name = 'lesson'


class MyHack(auth_views.PasswordResetView):
    success_url = reverse_lazy("lesson:password_reset_done")


urlpatterns = [
    # path('', views.all_teams, name='all_teams'),
    path('', views.TeamListView.as_view(), name='all_teams'),
    path('<int:yy>/<int:mm>/<int:dd>/<slug:slug>/', 
         views.detailed_team, name = 'detailed_team'),
    path('<int:team_id>/share/', views.share_team,
         name='share_team'),
    path('create/', views.create_team,
         name='create_form'),
#     path('login/', views.custom_login, name='login'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
path('logout/', auth_views.LogoutView.as_view(), name='logout'),

 path("password_reset/", MyHack.as_view(), name="password_reset"),
    path(
        "password_reset/done/",
        auth_views.PasswordResetDoneView.as_view(),
        name="password_reset_done",
    ),
    path(
        "reset/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            success_url=reverse_lazy("lesson:password_reset_complete"),
        ),
        name="password_reset_confirm",
    ),
    path(
        "reset/done/",
        auth_views.PasswordResetCompleteView.as_view(),
        name="password_reset_complete",
    ),
    path('profile/', views.view_profile, name='profile'),
    path('register/', views.register, name='register'),
    path('search/', SearchResultsView.as_view(), name='search_results'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('about/', AboutPageView.as_view(), name='about'),
    
]
