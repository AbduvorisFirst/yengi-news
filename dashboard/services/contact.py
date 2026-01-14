from django.contrib.auth.decorators import login_required
from news_project.models import Contact
from django.shortcuts import render, redirect
from news_project.forma import FormCon

@login_required(login_url='login')
def list(request):
    Con = Contact.objects.all().order_by('-id')
    ctx = {
        'con': Con,
        'contact': 'active'
    }
    return render(request, 'dashboard/pages/contact.html', ctx)



def add_edit(request, id=None):
    one = Contact.objects.filter(id=id).first()

    if request.POST:
        form = FormCon(request.POST, instance=one)
        if form.is_valid():
            form.save()
        else:
            print("\n\n", form.errors, "\n\n")
    return redirect('dashboard:contact-list')


def delete(request, id):
    Contact.objects.get(id=id).delete()
    return redirect('dashboard:contact-list')