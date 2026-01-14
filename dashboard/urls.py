from django.contrib.auth.decorators import login_required
from django.urls import path
from django.shortcuts import render
from dashboard.services import category, news, user, contact, subs



@login_required(login_url='login')
def index(request):
    return render(request, 'dashboard/pages/index.html', )

# <int:id>/
app_name='dashboard'
urlpatterns = [
    path("", index, name='dashboard-home'),
    path('ctg/', category.list, name='ctg-list'),
    path('contact/', contact.list, name='contact-list'),
    path('subs/', subs.list, name='subs-list'),

    path('ctg/add', category.add_edit, name='add_ctg'),
    path('news/add', news.add, name='news-add'),
    path('subs/add', subs.add_edit, name='add_subs'),
    path('contact/add', contact.add_edit, name='add_contact'),


    path('ctg/edit/<int:id>/', category.add_edit, name='ctg-edit'),
    path('news/edit/<int:id>/', news.add, name='news-edit'),
    path('contact/edit/<int:id>/', contact.add_edit, name='contact-edit'),
    path('subs/edit/<int:id>/', subs.add_edit, name='subs-edit'),


    path('ctg/delete/<int:id>/', category.delete, name='ctg-delete'),
    path('news/delete/<int:id>/', news.delete, name='news-delete'),
    path('subs/delete/<int:id>/', subs.delete, name='subs-delete'),
    path('contact/delete/<int:id>/', contact.delete, name='contact-delete'),


    path('news/<int:id>', news.book, name='news-info'),
    path('news/', news.list, name='news-list'),

]
