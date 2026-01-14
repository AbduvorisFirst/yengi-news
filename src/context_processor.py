import requests as re
from news_project.models import Category, New






def main(request):
    # url = 'https://cbu.uz/uz/arkhiv-kursov-valyut/json/'
    # valyuta = re.get(url).json()
    ctgs = Category.objects.filter(is_menu=True)
    fresh = New.objects.all().order_by('-id')[:8]

    return {
        'valyuta': None,
        'ctgs': ctgs,
        'fresh': fresh,
    }