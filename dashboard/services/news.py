

from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

from news_project.models import New, Category
from django.shortcuts import render, redirect
from news_project.forma import FormNew


@login_required(login_url='login')
def list(request):
    news = New.objects.all()

    paginator = Paginator(news, per_page=2)

    page = int(request.GET.get('page', 1))

    result = paginator.get_page(page)
    categories = Category.objects.all()  #

    ctx = {
        'new': result,
        'paginator': paginator,
        'page': page,
        'news': 'active',
        'ctg': categories,
        'status': 'list'
    }
    return render(request, 'dashboard/pages/news.html', ctx)


def book(request, id):
    news = New.objects.filter(id=id).first()
    ctx = {
            'news': news,
            'status': 'info'
        }

    return render(request, 'dashboard/pages/news.html', ctx)


def add(request, id=None):
    obj = New.objects.filter(id=id).first()
    form = FormNew(instance=obj)
    if request.POST:
        forms = FormNew(request.POST, request.FILES, instance=obj)
        if forms.is_valid():
            forms.save()
            return redirect('dashboard:news-list')

    ctx = {
        "news": 'active',
        'status': 'form',
        'form': form,
        'obj': obj,

    }
    return render(request, 'dashboard/pages/news.html', ctx)

def delete(request, id):
    New.objects.get(id=id).delete()
    return redirect('dashboard:news-list')





