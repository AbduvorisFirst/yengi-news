from django.contrib import admin
from django.utils.html import format_html
import datetime
from .models import Category, New, NewImage, Comment, Contact, Subscribe
# Register your models here.



@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'slug', 'name', 'menu']
    list_display_links = [ 'slug', 'name']


    @admin.display(description='mavjudmi', empty_value='???', ordering='is_menu')
    def menu(self, obj):
        if obj.is_menu:
            return format_html(
                "span style='color: green;'> ☑️ bizada bor" ,
            )
        else:
            return format_html(
                "span style='color: red;'> Bazada yoq"
            )

class ImageInline(admin.StackedInline):
    model = NewImage
    extra = 1

class CommentInline(admin.StackedInline):
    model = Comment
    Extra = 1



@admin.register(New)
class NewAdmin(admin.ModelAdmin):
    list_display = ['id', 'sarlavha', 'get_date', 'tags',  'get_image', 'ctg']
    list_display_links = ['id', 'sarlavha']
    search_fields = ['title', 'short_desc', 'description']
    list_filter = ['ctg',  'title', 'tags']
    readonly_fields = ['id', 'views', 'date']
    Inlines = [ImageInline, CommentInline]

    fieldsets = [
        ("General", {
            "fields": ['title', 'short_desc', 'description'],
        }),
        (
            "Extra", {
            'fields': ['image', 'ctg', 'tags']
             }
        ),
        (
            "ReadOnly", {
            'fields': ['id', 'views', 'date'],
            }
        )
    ]



    @admin.display(description='sana', empty_value='???', ordering='date')
    def get_date(self, obj):
        now = datetime.datetime.now()
        minut = int((now-obj.date).total_seconds() // 60)

        if minut < 2:
            return 'Hozir'
        elif minut < 60:
            return f'{minut} min'

        return obj.date.strftime('%H:%M / %d.%m.%Y')




    @admin.display(description='mavjudmi', empty_value='???', ordering='image')
    def get_image(self, obj):
        if obj.image:
            return format_html(
                f"<img src='{obj.image.url}' width='75px'>"
            )

    @admin.display(description='Title', empty_value='???', ordering='title')
    def sarlavha(self, obj):
        return f"{obj.title[:15]}..."
@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ['name', 'phone', 'date', 'message']
admin.site.register(Subscribe)
