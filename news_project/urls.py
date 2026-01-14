from django.urls import path
from .views import index, category, contact, search, view, obuna
from . import auth_views
urlpatterns = [
    path('',index, name='index'),
    path('ctg/<slug>/',category, name='ctg'),
    path('contact',contact, name='contact'),
    path('search',search, name='search'),
    path('view/<int:pk>/',view, name='view'),
    path('obuna/', obuna, name='obuna'),


    # auth
    path('login', auth_views.login, name='login'),
    path('register', auth_views.register, name='regis'),
    path('logout', auth_views.logout, name='logout'),
    path('otp/', auth_views.step_two, name='otp'),
]
