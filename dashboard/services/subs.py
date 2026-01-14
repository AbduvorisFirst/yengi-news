from django.contrib.auth.decorators import login_required
from news_project.models import Subscribe
from django.shortcuts import render, redirect
from news_project.forma import FormSubs

@login_required(login_url='login')
def list(request):
    subs = Subscribe.objects.all()
    ctx = {
        'subs': subs,

    }
    return render(request, 'dashboard/pages/subs.html', ctx)



def add_edit(request, id=None):
    one = Subscribe.objects.filter(id=id).first()

    if request.POST:
        form = FormSubs(request.POST, instance=one)
        if form.is_valid():
            form.save()
        else:
            print("\n\n", form.errors, "\n\n")
    return redirect('dashboard:subs-list')

def delete(request, id):
    Subscribe.objects.get(id=id).delete()
    return render(request, 'dashboard/pages/subs.html')