from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404

from .forms import ContactForm
from .models import Category, Comment, Contact, New, Subscribe
import requests as re
from django.db.models import Q
def valyuta():
    url = 'https://cbu.uz/uz/arkhiv-kursov-valyut/json/'
    natija = re .get(url).json()
    return natija


def index(request):
    news = New.objects.all().order_by('-id')
    aktual = news.filter(
        Q(title__icontains='tramp') |
        Q(short_desc__icontains='tramp')
    )[:3]



    ctx = {
        "news": news,
        "aktual": aktual,
        "populyar": news.order_by('-views')[:4],
        "kegan": news.filter(
            Q(title__icontains='m')
        ),
        'kolumst': news.filter(
            Q(title__icontains='a')
        ),
        'president': news.filter(
            Q(title__icontains='p') |
            Q(short_desc__icontains='p')
        ),
        'sport': news.filter(
            Q(title__icontains='sport') |
            Q(short_desc__icontains='sport') |
            Q(description__icontains='sport'),
        )
    }
    return render(request,'index.html', ctx)

def category(request, slug):
    ctg = get_object_or_404(Category, slug=slug)
    news_list = New.objects.filter(ctg=ctg).order_by('-id')

    paginator = Paginator(news_list, 2)  # 5 новостей на страницу
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    ctx = {
        "ctg": ctg,
        "news": page_obj,     # ✅ теперь здесь page_obj
        "page_obj": page_obj,
        "page": int(page_number),
        'count': len(news_list)
    }
    return render(request, 'category.html', ctx)


def contact(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            request.session['success'] = "habaringiz adminga yuborildi orada siz bilan bog'lanashandi"
        else:
            request.session['error'] = f'{form.errors}'
        return redirect( 'contact')

    success = request.session.get('success')
    error = request.session.get('error')

    try: del request.session['success']
    except: ...
    try: del request.session['error']
    except: ...
    ctx = {
        'success': success,
        'error': error,
    }
    return render(request,'contact.html', ctx)

def search(request):
    news = New.objects.all().order_by("-id")
    savol = request.GET.get('q', None)
    if not savol:
        return redirect('index')

    news = New.objects.filter(
        Q(title__icontains=savol) | Q(short_desc__icontains=savol) |
        Q(description__icontains=savol) | Q(ctg__name__icontains=savol))

    # if len(news) == 0:
    #     return render(request, 'category,html', {"error": 404})

    paginator = Paginator(news, per_page=2)
    page = request.GET.get("page", 1)
    result = paginator.get_page(page)
    ctx = {
        "savol": savol,
        "news": result,     # ✅ теперь здесь page_obj
        "page_obj": result,
        "page": int(page),
        'count': len(news),
        'new': news,
    }
    return render(request,'search.html', ctx)

def view(request, pk):
    new = New.objects.filter(pk=pk).first()
    new_1 = New.objects.all()
    if not new:
        return redirect(request, 'category.html', {'error': 404})

    new.views +=1
    new.save()

    if request.method == "POST":
        user = request.POST['user']
        comment = request.POST['comment']
        parent_id = request.POST.get('parent_id', None)
        Comment.objects.create(
            user=user,
            comment=comment,
            parent_id=parent_id,
            is_sub=parent_id is not None,
            new=new,
        )

    comment = Comment.objects.filter(new=new, is_sub=False).order_by('-id')

    ctx = {
        "new": new,
        'new_1': new_1,
        'comments': comment,
    }
    return render(request,'view.html', ctx)





def obuna(request):
    if request.method == 'POST':
        Subscribe.objects.get_or_create(email=request.POST['email'])
    path = request.GET.get('path', "/")
    return redirect(path)




                                                            




