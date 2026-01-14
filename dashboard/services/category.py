from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

from news_project.models import Category
from django.shortcuts import render, redirect, get_object_or_404
from news_project.forma import Form

@login_required(login_url='login')
def list(request):
    ctgs = Category.objects.all().order_by('-id')

    paginator = Paginator(ctgs, per_page=4)
    page = int(request.GET.get('page', 1))
    result = paginator.get_page(page)

    ctx = {
        'ctgs': result,
        'category': 'active',
        'paginator': paginator,
        'page': page,
        'result': result,
        "count": len(ctgs),
    }

    return render(request, 'dashboard/pages/category.html', ctx)





def add_edit(request, id=None):
    one = Category.objects.filter(id=id).first()

    if request.POST:
        form = Form(request.POST, instance=one)
        if form.is_valid():
            form.save()
        else:
            print("\n\n", form.errors, "\n\n")
    return redirect('dashboard:ctg-list')

def delete(request, id):
    Category.objects.get(id=id).delete()
    return redirect('dashboard:ctg-list')


