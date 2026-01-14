from django.core.mail import send_mail
from django.db.models.signals import post_save, post_delete, post_migrate
from django.dispatch import receiver
from .models import Contact, New, Subscribe
import requests
import datetime
from django.conf import settings


@receiver(post_save, sender=Contact)
def contact_signal(sender, instance, created, **kwargs):
    if created:
        message = f"adminlarga yangi habar\n" \
                  f"yuboruvchi: <b>{instance.name}</b>\n" \
                  f"yuboruvchining raqami: {instance.phone}\n\n" \
                  f"xabar: <b>{instance.message}</b>"

        token = "8469331894:AAGQDaDhUNsPSslujcrUulwuq6YuNph7qdA"
        user_id = 1821219115
        url = f"https://api.telegram.org/bot{token}/sendMessage?chat_id={user_id}&text={message}&parse_mode=HTML"

        requests.get(url)


@receiver(post_save, sender=New)
def news_signal(sender, instance: New, created: bool, **kwargs):
    if created:
        subject = "yangi habar abduvorischikdan"
        message = "Saytimizda siz uchun qiziqarli yangilik qo'shildi\n" \
                  f"Title: <b>{instance.title}</b><br>\n" \
                  f"Categoriya: <b>{instance.ctg.name}</b><br>" \
                  f"qisqacha Mazmuni: {instance.short_desc}\n<br>" \
                  f"qo'shish vaqt: <b>{datetime.datetime.now().strftime('%H:%M / %d.%m.%Y')}</b>"

        qabul_qiluvchilar = [

        ]

        for i in Subscribe.objects.filter(is_active=True):
            qabul_qiluvchilar.append(i.email)

        send_mail(
            subject=subject,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=qabul_qiluvchilar,
            message='',
            html_message=message,
        )
        message = 'barcga'
        token = settings.TG_TOKEN
        user_id = settings.TG_USER_ID
        url = f"https://api.telegram.org/bot{token}/sendMessage?chat_id={user_id}&text={message}&parse_mode=HTML"
        requests.get(url)


