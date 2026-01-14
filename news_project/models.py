from .auth_models import User
from django.db import models
from django.utils.text import slugify
import datetime
from .auth_models import Otp



class Category(models.Model):
    name = models.CharField(max_length=56)
    slug = models.SlugField(max_length=56, null=True, blank=True)
    is_menu = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)

        return super(Category, self).save()

    def __str__(self):
        return self.name



class New(models.Model):
    title = models.CharField(max_length=56)
    short_desc = models.TextField()
    description = models.TextField()
    image = models.ImageField()

    ctg = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='news')
    date = models.DateTimeField(auto_now_add=True)
    views = models.PositiveIntegerField(default=0, editable=False)
    tags = models.CharField(max_length=256)

    def save(self, *args, **kwargs):
        if "#" not in self.tags:
            self.tags = "#" + " #".join(self.tags.split())
        return super(New, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

    def get_date(self):
        now = datetime.datetime.now()
        minut = int((now-self.date).total_seconds() // 60)

        if minut < 2:
            return 'Hozir'
        elif minut < 60:
            return f'{minut} min'

        return self.date.strftime('%H:%M / %d.%m.%Y')

    def get_first_image(self):
        return self.images.first().image.url()

    def get_tags(self):
        return self.tags.strip("#").split('#')


    def get_short_desc(self):
        return self.short_desc.split("\n")

    def get_desc(self):
        return self.description.split("\n")

class NewImage(models.Model):
    image= models.ImageField(upload_to='news/')
    new = models.ForeignKey(New, on_delete=models.CASCADE, related_name='images')

class Comment(models.Model):
    user = models.CharField(max_length=56)
    comment = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    is_sub = models.BooleanField(default=False)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='atvet')
    new = models.ForeignKey(New, on_delete=models.CASCADE, related_name='comments')

class Contact(models.Model):
    name = models.CharField(max_length=56)
    phone = models.CharField(max_length=15)
    message = models.TextField()
    is_trash = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} | {self.message}"


class Subscribe(models.Model):
    email = models.EmailField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.email}'
